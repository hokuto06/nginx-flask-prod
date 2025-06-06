from django.urls import path
from django.contrib import admin
from blog import views
from django.conf import settings


urlpatterns = [
    path('',  views.home, name="Home"),
    path('post/<str:slug>', views.post_detail, name='Post' ),
    path("crear/", views.create_post, name="create_post"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("login_modal/", views.login_modal, name="login_modal"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("post/<slug:slug>/eliminar/", views.delete_post, name="delete_post"),
]

