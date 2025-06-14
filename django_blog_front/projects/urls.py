from django.urls import path
from django.contrib import admin
from projects import views
from django.conf import settings


urlpatterns = [
    path('',  views.home, name="projects"),
]

