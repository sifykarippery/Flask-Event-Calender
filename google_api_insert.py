from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import dateutil.parser as parser
import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def insert_service():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('tokenmod.pickle'):
        with open('tokenmod.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('tokenmod.pickle', 'wb') as token:
            pickle.dump(creds, token)
    insertservice = build('calendar', 'v3', credentials=creds)
    return insertservice
def create_event(eventTitle, eventDate, eventTime):
    dateTimePart = "{} {}:00 +0530".format(eventDate, eventTime)
    startDate = parser.parse(dateTimePart)
    endDate = startDate + datetime.timedelta(days=2)

    event = {
        'summary': eventTitle,
        'location': '800 Howard St., San Francisco, CA 94103',
        'description': eventTitle,
        'title': eventTitle,
        'start': {
            'dateTime': startDate.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': endDate.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
            ],
            },
        }

    new_event = insert_service().events().insert(calendarId='primary', body=event).execute()
    return new_event
def delete_event(eventId):
    del_event=insert_service().events().delete(calendarId='primary', eventId=eventId).execute()
    return del_event
