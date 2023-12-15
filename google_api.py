from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import dateutil.parser as parser
import datetime
import google_api_insert  as googleModEndpoint

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_api_service():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service
    # Call the Calendar API
def get_events():
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = get_api_service().events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events
def get_event_by_id(event_id):
    event = get_api_service().events().get(calendarId='primary',eventId=event_id).execute()
    return event

def update_event(event_id, title, date, time):
    original_event = get_event_by_id(event_id)
    dateTimePart = "{} {}:00 +0530".format(date, time)
    startDate = parser.parse(dateTimePart)
    endDate = startDate + datetime.timedelta(days=2)
    original_event["summary"] = title
    original_event["start"]["dateTime"] = startDate.isoformat()
    original_event["end"]["dateTime"] = startDate.isoformat()
    googleModEndpoint.insert_service().events().update(calendarId='primary',eventId=event_id, body=original_event).execute()