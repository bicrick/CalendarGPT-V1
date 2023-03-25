import openai
import pinecone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



import dotenv
import datetime
import os.path
import json
import dateutil.parser


SCOPES = ['https://www.googleapis.com/auth/calendar']

class Calendar:
    def init():
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

    #Function that gets events from the events.json file
    def get_events_from_file(file_path):
        with open(file_path) as json_file:
            events = json.load(json_file)
        return events

    #Function that returns a list object of the events currently on the calendar
    def get_events(token_file_path):
        creds = Credentials.from_authorized_user_file(token_file_path, SCOPES)
        service = build('calendar', 'v3', credentials=creds)
        # Call the Calendar API to list upcoming events
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 50 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=50, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
        return events

    #Function that given an event id will return the event object from the calendar.
    def get_event_by_id(event_id,token_file_path):
        creds = Credentials.from_authorized_user_file(token_file_path, SCOPES)
        service = build('calendar', 'v3', credentials=creds)
        # Call the Calendar API to list upcoming events
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        print('Getting the event with id: ' + event_id)
        event = service.events().get(calendarId='primary', eventId=event_id).execute()
        return event
    
    #Function that given an event id will delete the event from the calendar.
    def delete_event_by_id(event_id,token_file_path):
        creds = Credentials.from_authorized_user_file(token_file_path, SCOPES)
        service = build('calendar', 'v3', credentials=creds)
        # Call the Calendar API to list upcoming events
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Deleting the event with id: ' + event_id)
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        return

    #Function that given an event object will add the event to the calendar.
    def add_event(event,token_file_path):
        creds = Credentials.from_authorized_user_file(token_file_path, SCOPES)
        service = build('calendar', 'v3', credentials=creds)
        # Call the Calendar API to list upcoming events
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Adding the event: ' + event['summary'])
        service.events().insert(calendarId='primary', body=event).execute()
        return

    #Function that given an event object will update the event on the calendar.
    def update_event(event,token_file_path):
        creds = Credentials.from_authorized_user_file(token_file_path, SCOPES)
        service = build('calendar', 'v3', credentials=creds)
        # Call the Calendar API to list upcoming events
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Updating the event: ' + event['summary'])
        service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()

    
    #Function that given an event object will delete the event from the calendar.
    def delete_event(event,token_file_path):
        creds = Credentials.from_authorized_user_file(token_file_path, SCOPES)
        service = build('calendar', 'v3', credentials=creds)
        # Call the Calendar API to list upcoming events
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        print('Deleting the event: ' + event['summary'])
        service.events().delete(calendarId='primary', eventId=event['id']).execute()
        return
    
    
    

    