import re
import traceback
from application import db
from database.smart_numbers import SmartNumber
from database.google_auth import GoogleAuth
from database.user import User


def format_did(number):
    number = re.sub('\ |\(|\)|\-', '', number)

    if number.isdigit():

        if len(number) == 11:
            return number
        elif len(number) == 10:
            number = '1' + number
            return number
        else:
            return False
    else:
        return False


def add_sm_number_registration_db(smart_number, destination_ext, nx_app_id):

    sm_number = SmartNumber()
    sm_number.smart_number = smart_number
    sm_number.destination_extension = destination_ext
    sm_number.nx_app_id = nx_app_id

    try:
        db.session.add(sm_number)
        db.session.commit()
        db.session.close()
        print(f'---- SM NB {smart_number} RECORD SAVED ----')
        return True

    except Exception:
        db.session.rollback()
        print(f'---- SM NB {smart_number} ERROR SAVING RECORD ----')
        traceback.print_exc()
        return False


def get_sm_number_db(smart_number):

    sm_number = db.session.query(SmartNumber).filter(SmartNumber.smart_number == smart_number).first()
    db.session.close()

    return sm_number


def get_all_sm_numbers_db():

    try:
        get_data = db.session.query(SmartNumber).all()

        data_list = []
        for number in get_data:
            get_gg = db.session.query(GoogleAuth).filter(GoogleAuth.id == number.google_id).first()
            if get_gg:
                gg_email = get_gg.email
                cal_name = get_gg.calendar_name
            else:
                gg_email = ''
                cal_name = ''
            data_list.append(
                {'number': number.smart_number,
                 'destination': number.destination_extension,
                 'calendar': gg_email,
                 'calendar_name': cal_name}
            )

        db.session.close()
    except Exception:
        db.session.rollback()
        print('---- ERROR getting account numbers data ----')
        traceback.print_exc()
        return False

    print(data_list)

    return data_list


def add_google_auth_db(credentials, smart_number):

    gg = GoogleAuth()
    gg.credentials = credentials
    gg.email = credentials.id_token['email']

    try:
        db.session.add(gg)
        db.session.flush()

        print(f'gg.id {gg.id}')
        # Link to Smart Number
        sm_number = db.session.query(SmartNumber).filter(SmartNumber.smart_number == smart_number).first()
        sm_number.google_id = gg.id

        db.session.commit()
        db.session.close()
        print('---- GOOGLE Auth RECORD SAVED ----')
        return True
    except Exception:
        db.session.rollback()
        print('---- ERROR SAVING GOOGLE Auth RECORD ----')
        traceback.print_exc()
        return False


def add_google_calendar_db(google_id, calendar_id, calendar_name):

    try:
        gg = db.session.query(GoogleAuth).filter(GoogleAuth.id == google_id).first()
        gg.calendar = calendar_id
        gg.calendar_name = calendar_name
        db.session.commit()
        db.session.close()
        print('---- GOOGLE CALENDAR ID RECORD SAVED ----')
        return True
    except Exception:
        db.session.rollback()
        print('---- ERROR SAVING GOOGLE CALENDAR ID RECORD ----')
        traceback.print_exc()
        return False


def get_google_auth_db(google_id):

    auth = db.session.query(GoogleAuth).filter(GoogleAuth.id == google_id).first()
    db.session.close()

    return auth


def get_user_db(username):

    user = db.session.query(User).filter(User.username == username).first()
    db.session.close()

    return user


def delete_number_db(number):

    try:
        db_number = SmartNumber.query.filter_by(smart_number=number).one()

        if db_number.google_id:
            db_gg = GoogleAuth.query.filter_by(id=db_number.google_id).one()

        db.session.delete(db_number)
        db.session.commit()
        if db_number.google_id:
            db.session.delete(db_gg)
            db.session.commit()
        db.session.close()
        print(f'---- SMART NUMBER AND GOOGLE CREDS DELETED FOR {number} ----')

        return True
    except Exception:
        db.session.rollback()
        print(f'---- ERROR DELETING RECORDS FOR {number} ----')
        traceback.print_exc()
        return False





