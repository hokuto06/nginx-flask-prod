from django.urls import path
from django.contrib import admin
from projects import views
from django.conf import settings


urlpatterns = [
    path('',  views.home, name="projects"),
    path('email-parser/', views.project_email, name='email-parser'),
    path('template/', views.project_template, name='template'),
    path('iot-cctv/', views.project_iot_cctv, name='iot-cctv'),
    path('docker-project/', views.docker_project, name='docker-project'),]

