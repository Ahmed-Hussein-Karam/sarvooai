import os
import uuid
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from django.urls import reverse
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import meet_v2
from googleapiclient.discovery import build

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/home/')
    return render(request, 'sarvoo/login.html')

def home_view(request):
    return render(request, 'sarvoo/home.html')

def interview_view(request):
    return render(request, 'sarvoo/interview.html')

def get_creds():
    creds = None
    creds_file= os.path.join(os.path.dirname(__file__), 'json/creds_desktop.json')
    SCOPES = ['https://www.googleapis.com/auth/meetings.space.created']

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # If modifying these scopes, delete the file token.json. 
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds


def get_calendar_service():
    SCOPES=['https://www.googleapis.com/auth/calendar']
    service_account_file = os.path.join(os.path.dirname(__file__), 'json/sarvooai-service-account-key.json')

    credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=SCOPES)

    return build('calendar', 'v3', credentials=credentials)

def get_sarvoo_joining_url(meeting_id):
    
    # Create a Google Calendar API client
    calendar_service = get_calendar_service()
    sarvoo_joining_url = None

    try:
        unique_id = str(uuid.uuid4())
        conference_data = {
            'createRequest': {
                'requestId': unique_id  # Provide a unique ID for the conference request
            }
        }

        # Generate the meeting details from the meeting ID
        meeting_details = calendar_service.events().quickAdd(
            calendarId='primary',
            text=f'Start a Google Meet: https://meet.google.com/{meeting_id}'
        ).execute()

        # Get the updated details
        updated_meeting = calendar_service.events().patch(
            calendarId='primary',
            eventId=meeting_details['id'],
            body={
                'conferenceData': conference_data
            }
        ).execute()

        print (updated_meeting)
        entryPoints = updated_meeting.get('conferenceData', {}).get('entryPoints', [])
        sarvoo_joining_url = next((entry['uri'] for entry in entryPoints if entry['entryPointType'] == 'video'), None)

    except Exception as e:
        print(f"Error joining Google Meet: {e}")
    
    return sarvoo_joining_url

def create_and_launch_meeting(request):
    """Creates a Google Meet event and launches it"""
    creds = get_creds()
    client = meet_v2.SpacesServiceClient(credentials=creds)

    request = meet_v2.CreateSpaceRequest()
    response = client.create_space(request=request)
    meeting_id = response.meeting_uri.split("/")[-1]

    print(f'Space created: {response}')
    client = meet_v2.SpacesServiceClient(credentials=creds)

    request = meet_v2.CreateSpaceRequest()
    response = client.create_space(request=request)
    meeting_id = response.meeting_uri.split("/")[-1]

    print(f'Space created: {response}')
    sarvoo_joining_url = get_sarvoo_joining_url(meeting_id)
    print(sarvoo_joining_url)
    return redirect(reverse('interview') + f'?id={meeting_id}')
