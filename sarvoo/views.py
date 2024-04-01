from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

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
