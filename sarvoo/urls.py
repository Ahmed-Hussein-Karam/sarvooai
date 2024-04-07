from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('interview/', views.interview_view, name='interview'),
    path('create_and_launch_meeting/', views.create_and_launch_meeting, name='create_and_launch_meeting'),
]