import datetime
import os.path
from googleapiclient.discovery import build
from pprint import pprint
import configparser


config = configparser.ConfigParser()
config.read('instance/config.ini')

platform = os.getenv('MY_ENV')
print(f'MY_ENV - {platform}')

if platform == 'development':
    devel = True
    conf = config['DEVEL']
else:
    devel = False
    conf = config['PRODUCTION']

CLIENT_SECRETS_FILE = conf['GG_CLIENT_SECRETS_FILE']

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_google_calendar_list(creds):
    print('Get Calendar List')
    service = build('calendar', 'v3', credentials=creds)

    calendar_list_result = service.calendarList().list().execute()

    # pprint(calendar_list_result)

    calendar_list = []

    for calIdx in calendar_list_result['items']:
        print(calIdx['summary'])
        calendar_list.append(
            {
                'id': calIdx['id'],
                'summary': calIdx['summary']
            }
        )

    return calendar_list


def google_get_calendar_events(creds, calendarId='primary'):
    # print(f'creds - {creds}')
    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow()
    timeMin = now.isoformat() + 'Z'  # 'Z' indicates UTC time
    # Add 1 minute for timeMax
    add_min = now + datetime.timedelta(0, 60)
    date_time_obj = datetime.datetime.strptime(str(add_min), '%Y-%m-%d %H:%M:%S.%f')
    timeMax = date_time_obj.isoformat() + 'Z'

    print('Time being used:')
    print(timeMin)
    print(timeMax)

    print()
    print('Getting current event')
    events_result = service.events().list(calendarId=calendarId, timeMin=timeMin, timeMax=timeMax,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    pprint(events_result)
    events = events_result.get('items', [])

    if not events:
        print('No current events found.')
        return False
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

        return events[0]['summary']


