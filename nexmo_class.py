import google_oauth
# import os
# import pickle
import nexmo
import functions


def answer_ncco (number_from, number_to, get_sm_number, get_google_auth):

    creds = get_google_auth.credentials
    calendar_id = get_google_auth.calendar

    print(f'Google creds for {number_to}: {creds}')
    print(f'Using calendar for {number_to}: {calendar_id}')

    get_calendar_event = google_oauth.google_get_calendar_events(creds, calendar_id)

    print(f'Calendar Events for {number_to}: {get_calendar_event}')

    # get DID or extension from the Calendar Event

    # Create NCCO

    if get_calendar_event:
        if ' ' in get_calendar_event:
            event_ext = get_calendar_event.split(' ')[0]
        else:
            event_ext = get_calendar_event

        # Check if numbers
        event_ext = functions.format_did(event_ext)

        if event_ext:
            if len(event_ext) < 10:
                endpoint = [{
                            "type": "vbc",
                            "extension": event_ext
                        }]
            else:
                endpoint = [{
                    "type": "phone",
                    "number": event_ext
                }]

            ncco = [
                {
                    "action": "connect",
                    "from": number_from,
                    "endpoint": endpoint
                }
            ]
            print(f'Event destination is Number or Extension. NCCO for call from {number_from} to {number_to} {ncco}')

        else:
            # Event destination is not extension or number
            destination_call_number = get_sm_number.destination_extension
            if len(destination_call_number) < 10:
                endpoint = [{
                    "type": "vbc",
                    "extension": destination_call_number
                }]
            else:
                endpoint = [{
                    "type": "phone",
                    "number": destination_call_number
                }]

            ncco = [
                {
                    "action": "connect",
                    "from": number_from,
                    "endpoint": endpoint
                }
            ]
            print(f'Destination is NOT Number or Extension. NCCO for call from {number_from} to {number_to} {ncco}')
    else:  # Default Destination
        destination_call_number = get_sm_number.destination_extension
        if len(destination_call_number) < 10:
            endpoint = [{
                "type": "vbc",
                "extension": destination_call_number
            }]
        else:
            endpoint = [{
                "type": "phone",
                "number": destination_call_number
            }]

        ncco = [
              {
                "action": "connect",
                "from": number_from,
                "endpoint": endpoint
              }
            ]
        print(f'No Event NCCO for call from {number_from} to {number_to} {ncco}')

    return ncco


def nx_acc_update_application(answer_url, application_id, application_name, nexmo_api_key, nexmo_api_secret):

    client = nexmo.Client(key=nexmo_api_key, secret=nexmo_api_secret)

    response = client.application_v2.update_application(application_id, {'name': application_name,
                                                                         'capabilities':
                                                                             {'voice':
                                                                                  {'webhooks':
                                                                                       {'answer_url':
                                                                                            {'address': f'{answer_url}/answer',
                                                                                             "http_method": "GET"
                                                                                             },
                                                                                       "event_url": {
                                                                                                 "address": f"{answer_url}/event",
                                                                                                  "http_method": "POST"
                                                                                               }
                                                                                       }
                                                                                   }
                                                                              }
                                                                         })
    return response


def nx_acc_get_applications(nexmo_api_key, nexmo_api_secret, page_size=None):
    """

    :param nexmo_api_key:
    :param nexmo_api_secret:
    :param page_size:
    :return:
    """

    client = nexmo.Client(key=nexmo_api_key, secret=nexmo_api_secret)
    # url = 'https://api.nexmo.com/v2/applications'

    print('Getting NX app list...')
    response = client.application_v2.list_applications(page_size=page_size)

    # check how many pages:
    if response:
        if response['total_pages'] > 1:
            print(f'More than one app list page found ({response["total_pages"]})')
            all_apps = []
            total_pages = response['total_pages']

            for idx in range(1, int(total_pages) + 1):
                response = client.application_v2.list_applications(page=idx, page_size=page_size)
                print(f'Getting NX app list page {idx}')
                if response:
                    all_apps += response['_embedded']['applications']

            return all_apps

        else:
            return response['_embedded']['applications']
    else:
        return False


def update_nx_app_id(smart_did, nx_app_id, nx_key, nx_secret, answer_url, qa7_fix):
    # Get all Nexmo Apps
    all_nx_apps = nx_acc_get_applications(nx_key, nx_secret)

    # Check if Application exist for the provided Smart Number
    nx_app_id_verified = False
    for idxApp in all_nx_apps:
        if nx_app_id == idxApp.get('id'):
            print(f'Nexmo Application found for the Smart Number {smart_did}')
            nx_app_id_verified = True
            break
    # Update Nexmo App
    if nx_app_id_verified:
        application_name = f'Call_scheduler-{smart_did}'
        app_update = nx_acc_update_application(
            answer_url=answer_url,
            application_id=nx_app_id,
            application_name=application_name,
            nexmo_api_key=nx_key,
            nexmo_api_secret=nx_secret
        )

        if qa7_fix:
            nx_did_update(nx_key, nx_secret, smart_did, nx_app_id)
        if app_update:
            print(f'Nexmo Application updated for the Smart Number {smart_did}')
            return True
        else:
            print(f'Nexmo Application updated FAILED for the Smart Number {smart_did}')
            return False
    else:
        print(f'Provided Nexmo App not found {nx_app_id}')
        return False


def nx_did_update(nexmo_api_key, nexmo_api_secret, number, app_id):
    '''

    :param nexmo_api_key:
    :param nexmo_api_secret:
    :param number:
    :param app_id:
    :return:
    '''

    client = nexmo.Client(key=nexmo_api_key, secret=nexmo_api_secret)

    print(f'QA7 FIX. Updating NX Number {number} with App ID {app_id}')

    data = {'country': 'US',
            'msisdn': number,
            'voiceCallbackType': 'app',
            'voiceCallbackValue': app_id
            }

    response = client.update_number(data)

    print(f'NX Update Number response: {response}')

    return response


