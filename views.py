from application import *
from functions import get_user_db, format_did, \
    get_sm_number_db, add_sm_number_registration_db, get_all_sm_numbers_db, get_google_auth_db, add_google_calendar_db, \
    delete_number_db, add_google_auth_db

from form import LoginForm, SetupForm

from nexmo_class import answer_ncco, update_nx_app_id
from pprint import pprint

from oauth2client import client
from google_oauth import get_google_calendar_list


title = f'Call Scheduler'


def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text}  - {error}")
            print(f"User Input Error - {getattr(form, field).label.text} field - {error}")


@login.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return get_user_db(user_id)


@app.route("/")
def index():
    return redirect(f"{base_url}/setup")


@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        print(form.username.data)
        user_db = get_user_db(form.username.data)
        pprint(f'Database User: {user_db}')

        if user_db:
            user = user_db.username
            pswd = user_db.password
            if pswd == form.password.data:

                user_db.authenticated = True

                try:
                    db.session.add(user_db)
                    db.session.commit()

                    login_user(user_db, remember=form.remember_me.data)

                    print(f'USER AUTHENTICATED - {user_db.username}')
                    db.session.close()

                    return redirect(f"{base_url}/setup")
                except:
                    print(f'AUTHENTICATION FAILED - {user_db.username}')
                    db.session.rollback()
                    flash('Login Failed. Try again...')
                    print(f'AUTHENTICATION FAILED - {form.username.data}')
                    return render_template("login.html", form=form)
            else:
                flash('Invalid username or password')
                print(f'AUTHENTICATION FAILED - {form.username.data}')
                return render_template("login.html", form=form)

        else:
            flash('Invalid username or password')
            print(f'AUTHENTICATION FAILED - {form.username.data}')
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    username = current_user.username
    print(f'Logout User {username}')
    logout_user()
    # return redirect(url_for("index"))
    return redirect(f"{base_url}/")


@app.route("/setup", methods=['GET', 'POST'])
@login_required
def setup():
    global answer_url, base_url, title

    form = SetupForm()

    user_name = current_user.username
    print(f'/setup User {user_name}')

    get_all_registered_numbers = get_all_sm_numbers_db()

    nx_key = nexmo_api_key
    nx_secret = nexmo_api_secret

    if request.method == 'POST':
        # Validate User Inputs
        if form.validate():
            print('VALIDATED FORM')
        else:
            flash_errors(form)
            return render_template(
                'setup.html',
                title=title,
                registered_data=get_all_registered_numbers,
                user=current_user.username,
                nx_key=nx_key,
                form=form
            )

        smart_did = request.values.get('smart_did')
        nx_app_id = request.values.get('nx_app_id')
        destination_ext = request.values.get('destination_ext')

        print(f'smart_did, nx_app_id, destination_ext: {smart_did, nx_app_id, destination_ext}')

        # Verify Smart Number String

        smart_did = format_did(smart_did)

        if len(destination_ext) > 9:
            destination_ext = format_did(destination_ext)

        if smart_did:

            # Verify if sm number already in db
            get_sm_number = get_sm_number_db(smart_did)

            if not get_sm_number:
                print(f'Smart Number {smart_did} not in db')

                # Do Nexmo App provisioning
                nx_app_id_update = update_nx_app_id(smart_did, nx_app_id, nx_key, nx_secret, answer_url, qa7_fix)
                if nx_app_id_update:
                    # Save to db
                    add_sm_number_registration_db(
                        smart_number=smart_did,
                        destination_ext=destination_ext,
                        nx_app_id=nx_app_id
                    )
                else:
                    print(f'---- Failed to update Nexmo App ID {nx_app_id}----')
                    flash(f'Failed to update Nexmo App ID {nx_app_id}')
                    return render_template(
                        'setup.html',
                        title=title,
                        registered_data=get_all_registered_numbers,
                        user=current_user.username,
                        nx_key=nx_key,
                        form=form
                    )

            else:
                print('---- Smart Number is already in the database ----')
                flash('Smart Number already in use')
                return render_template(
                    'setup.html',
                    title=title,
                    registered_data=get_all_registered_numbers,
                    user=current_user.username,
                    nx_key=nx_key,
                    form=form
                )

        # registered_data = f"Smart DID {smart_did} registered"
        return redirect(f'{base_url}/calendar_link?smart_number={smart_did}')

    return render_template(
        'setup.html',
        title=title,
        registered_data=get_all_registered_numbers,
        user=current_user.username,
        nx_key=nx_key,
        form=form
    )


@app.route("/calendar_link", methods=['GET', 'POST'])
@login_required
def calendar_link():
    global title

    smart_number = request.args['smart_number']
    username = current_user.username

    get_all_registered_numbers = get_all_sm_numbers_db()

    if request.method == 'POST':
        return redirect(f"{base_url}/select_calendar?smart_number={smart_number}")

    return render_template(
        'calendar_link.html',
        title=title,
        registered_data=get_all_registered_numbers,
        user=current_user.username,
        smart_number=smart_number,
        google_client_id=google_client_id,
        answer_url=base_url
    )


@app.route("/select_calendar", methods=['GET', 'POST'])
@login_required
def select_calendar():
    global title

    smart_number = request.args['smart_number']
    username = current_user.username

    get_all_registered_numbers = get_all_sm_numbers_db()

    get_sm_number = get_sm_number_db(smart_number)
    gg_creds = get_google_auth_db(get_sm_number.google_id)
    calendar_list = get_google_calendar_list(gg_creds.credentials)

    if request.method == 'POST':
        # Save calendar
        calendar_id = request.form['calendars']

        # Get Calendar Name
        calendar_name = ''
        for idxCal in calendar_list:
            if calendar_id == idxCal['id']:
                calendar_name = idxCal['summary']

        print(f'Selected Calendar: {calendar_id}')

        update_db = add_google_calendar_db(get_sm_number.google_id, calendar_id, calendar_name)

        return redirect(f"{base_url}/calendar_instructions?smart_number={smart_number}&calendar_name={calendar_name}")

    return render_template(
        'select_calendar.html',
        title=title,
        user=current_user.username,
        smart_number=smart_number,
        registered_data=get_all_registered_numbers,
        calendar_list=calendar_list
    )


@app.route("/calendar_instructions", methods=['GET', 'POST'])
@login_required
def calendar_instructions():
    global title

    # TODO Update Calendar Instructions

    smart_number = request.args['smart_number']
    calendar_name = request.args['calendar_name']

    username = current_user.username

    get_all_registered_numbers = get_all_sm_numbers_db()

    if request.method == 'POST':

        return redirect(f"{base_url}/setup")

    return render_template(
        'calendar_instructions.html',
        title=title,
        user=current_user.username,
        smart_number=smart_number,
        registered_data=get_all_registered_numbers,
        calendar_name=calendar_name
    )


@app.route("/delete_number")
@login_required
def delete_number():
    number = request.args.get('number')
    if number:
        print(f'Deleting {number}')
        db_delete = delete_number_db(number)

    return redirect(f"{base_url}/setup")


@app.route("/answer")
def answer_call():

    number_to = request.args.get('to')
    number_from = request.args.get('from')
    number_conversation_uuid = request.args.get('conversation_uuid')
    number_uuid = request.args.get('uuid')

    print(f'Answering call from {number_from} to {number_to}')

    print(f'Lookup Smart Number {number_to}')
    get_sm_number = get_sm_number_db(number_to)
    get_google_auth = get_google_auth_db(get_sm_number.google_id)
    print(get_sm_number)

    return jsonify(answer_ncco(number_from, number_to, get_sm_number, get_google_auth))


@app.route("/event", methods=['POST'])
def events():
    content = request.json
    print()
    print(f'Event - {content}')
    return jsonify(content)


@app.route("/test")
def google_test():
    return '', 200


@app.route("/storeauthcode", methods=['POST'])
def google_storeauthcode():
    # Google Oauth Callback URL
    auth_code = request.json.get('data')
    sm_nmbr = request.json.get('smart_did')
    print('storeauthcode:')
    pprint(auth_code)
    pprint(sm_nmbr)

    # verify DID

    sm_nmbr = format_did(str(sm_nmbr))

    if not request.headers.get('X-Requested-With'):
        return ('', 403)

    CLIENT_SECRET_FILE = 'instance/google_secret.json'

    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE,
        ['https://www.googleapis.com/auth/calendar.readonly', 'profile', 'email'],
        auth_code)

    # Get profile info from ID token
    userid = credentials.id_token['sub']
    email = credentials.id_token['email']

    save_to_db = add_google_auth_db(credentials, sm_nmbr)
    if save_to_db:
        return '', 204
    else:
        return '', 500




