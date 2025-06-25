from django.urls import path
from django.contrib import admin
from blog import views
from django.conf import settings
from django.shortcuts import redirect


urlpatterns = [
    # path('', lambda request: redirect('Home', permanent=True)),
    path('', views.home_redirect_or_bot),
    path('home/',  views.home, name="Home"),
    path('blog/',  views.blog, name="blog"),
    path('post/<str:slug>', views.post_detail, name='Post' ),
    path("crear/", views.create_post, name="create_post"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("login_modal/", views.login_modal, name="login_modal"),
    path("me/", views.about, name="me"),
    path("contact/", views.contact, name="contact"),
    path("post/<slug:slug>/eliminar/", views.delete_post, name="delete_post"),
    path("registro/", views.register_view, name="register"),
    path("post/<slug:slug>/editar/", views.edit_post, name="edit_post"),
    path("create_category/", views.create_category, name="create_category"),
    path("api/contact/", views.contact_form_s3, name="contact_from_portfolio"),
]

