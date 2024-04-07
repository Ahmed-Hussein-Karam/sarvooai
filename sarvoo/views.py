import os
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from django.urls import reverse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import meet_v2

CREDENTIALS_FILE = 'json/creds_webapp.json'

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
    print ("I am coming.........")
    return render(request, 'sarvoo/interview.html')

def get_creds():
    creds = None
    creds_file= os.path.join(os.path.dirname(__file__), 'json/creds_desktop.json')
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/meetings.space.created']

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
    return redirect(reverse('interview') + f'?id={meeting_id}')
