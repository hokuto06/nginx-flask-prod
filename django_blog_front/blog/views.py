from django.shortcuts import render, redirect
import requests
from .forms import LoginForm
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils.timezone import make_aware
import dateutil.parser
from pprint import pprint


API_LOGIN_URL = "http://django-api:8000/api/auth/login"
API_USER_ME_URL = "http://django-api:8000/api/auth/me"

API_CATEGORIES_URL = "http://django-api:8000/api/categories/"
API_CREATE_POST_URL = "http://django-api:8000/api/posts/"

COMMENTS_URL = "http://django-api:8000/api/comments/"


def home(request):
    return render(request, "home.html")

def blog(request):
    try:
        response = requests.get("http://django-api:8000/api/posts/")
        posts = response.json() if response.status_code == 200 else []
    except Exception as e:
        print("Error al conectarse con la API:", e)
        posts = []

    return render(request, "index.html", {"posts": posts})


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def post_detail(request, slug):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    response = requests.get(f"http://django-api:8000/api/posts/{slug}/", headers=headers)
    print("POST DETAIL RESPONSE:", response.status_code, response.text)
    
    post = response.json() if response.status_code == 200 else None

    if request.method == "POST" and token:
        comment_data = {
            "content": request.POST.get("content"),
            "post": post["slug"], 
        }
        requests.post(COMMENTS_URL, json=comment_data, headers=headers)
    print(post)
    comments_response = requests.get(f"{COMMENTS_URL}?post={post['id']}", headers=headers)
    comments = comments_response.json() if comments_response.status_code == 200 else []
    return render(request, "post.html", {
        "post": post,
        "comments": comments,
    })


def edit_post(request, slug):
    API_EDIT_POST_URL = f"http://django-api:8000/api/posts/{slug}/"
    token = request.session.get("token")
    if not token:
        return redirect("login")

    headers = {"Authorization": f"Bearer {token}"}
    
    post_response = requests.get(API_EDIT_POST_URL, headers=headers)
    print(post_response)
    if post_response.status_code != 200:
        return redirect("Home")
    post = post_response.json()

    if post["user"]["email"] != request.session.get("email"):
        return redirect("Home")

    categories = requests.get(API_CATEGORIES_URL).json()
    if request.method == "POST":
        data = {
            "title": request.POST.get("title"),
            "description": request.POST.get("description"),
            "content": request.POST.get("content"),
            "published": request.POST.get("published") == "on",
            "category": request.POST.get("category"),
            "slug": request.POST.get("slug"),
        }
        files = {}
        new_file = request.FILES.get("miniature")
        if new_file:
            files["miniature"] = new_file        

        if files:
            response = requests.put(API_EDIT_POST_URL, data=data, files=files, headers=headers)
            print("miniatureeeeeeeeeeeeeeeeeeeeee")
        else:
            response = requests.put(API_EDIT_POST_URL, json=data, headers=headers)
            print("Nooo miniatureeeeeeeeeeeeeeeeeeeeee")

        print("PUT status:", response.status_code)
        print("PUT test:", response.text)

        if response.status_code == 200:
            return redirect("Post", slug=slug)

    return render(request, "edit-post.html", {"post": post, "categories": categories})


def delete_post(request, slug):
    token = request.session.get("token")
    if not token:
        return redirect("login")

    headers = {"Authorization": f"Bearer {token}"}

    if request.method == "POST":
        delete_url = f"http://django-api:8000/api/posts/{slug}/"
        response = requests.delete(delete_url, headers=headers)

        if response.status_code == 204:
            return redirect("Home")
        else:
            print("Error al eliminar post:", response.status_code, response.text)
            return redirect("Post", slug=slug)

    return redirect("Home")


# @csrf_exempt
def create_post(request):
    token = request.session.get("token")
    # print(token)
    if not token:
        return redirect("login")
    # print("Token actual:", request.session.get("token"))

    headers = {"Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
    }
    # print(headers)

    if request.method == "POST":
        data = {
            "title": request.POST.get("title"),
            "description": request.POST.get("description"),
            "content": request.POST.get("content"),
            "slug": request.POST.get("slug"),
            "published": request.POST.get("published") == "on",
            "category": request.POST.get("category"),
        }

        files = {"miniature": request.FILES.get("miniature")}
        print(files)
        headers = {
            "Authorization": f"Bearer {token}"
            # NO pongas "Content-Type", requests lo agrega automáticamente para multipart
        }

        response = requests.post(API_CREATE_POST_URL, data=data, files=files, headers=headers)
        print("Respuesta POST:", response.status_code, response.text)

        if response.status_code == 201:
            post_data = response.json()
            return redirect(f"/post/{post_data['slug']}")

        else:
            return render(request, "create-post.html", {
                "error": "No se pudo crear el post.",
                "form_data": data,
                "categories": [],
            })

    # print("Respuesta POST:", response.status_code, response.text)
    categories_response = requests.get(API_CATEGORIES_URL)
    categories = categories_response.json() if categories_response.status_code == 200 else []
    print(categories)
    return render(request, "create-post.html", {
        "categories": categories,
    })


def logout_view(request):
    request.session.flush()
    return redirect("Home")


def login_view(request):
    error = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                response = requests.post(API_LOGIN_URL, json=data)
                if response.status_code == 200:
                    token = response.json().get("access")
                    if token:
                        request.session["token"] = token
                        request.session["email"] = data["email"]
############################# probando redirección con datos de usuario
                        headers = {"Authorization": f"Bearer {token}"}
                        me_response = requests.get(API_USER_ME_URL, headers=headers)
                        if me_response.status_code == 200:
                            user = me_response.json()
                            print(user)
                            request.session["email"] = user.get("email")
                            request.session["user_name"] = user.get("username") or user.get("email")
##################################################
                        return redirect("Home")
                error = "Credenciales inválidas"
            except Exception:
                error = "No se pudo conectar con la API"
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form, "error": error})


def login_modal(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        next_url = request.POST.get("next", "/")
        if form.is_valid():
            data = form.cleaned_data
            try:
                response = requests.post(API_LOGIN_URL, json=data)
                if response.status_code == 200:
                    token = response.json().get("access")
                    if token:
                        request.session["token"] = token
                        headers = {"Authorization": f"Bearer {token}"}
                        me_response = requests.get(API_USER_ME_URL, headers=headers)
                        if me_response.status_code == 200:
                            user = me_response.json()
                            print(user)
                            request.session["email"] = user.get("email")
                            request.session["user_name"] = user.get("username") or user.get("email")
                        return redirect(next_url)
            except Exception as e:
                print("Error al intentar loguear:", e)
        return redirect(f"{next_url}?login_error=1")
    return redirect("/")


def register_view(request):
    API_REGISTER_URL = "http://django-api:8000/api/auth/register"
    error = None

    if request.method == "POST":
        data = {
            "email": request.POST.get("email"),
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
            "password2": request.POST.get("password2"),
        }

        try:
            response = requests.post(API_REGISTER_URL, json=data)
            print("Registro:", response.status_code, response.text)

            if response.status_code == 201:
                return redirect("login")
            else:
                error = response.json()
                if isinstance(error, dict):
                    error = "; ".join([f"{k}: {v[0]}" for k, v in error.items()])
        except Exception as e:
            error = "Error al conectar con la API"

    return render(request, "register.html", {"error": error})


def perfil_view(request):
    token = request.session.get("token")
    if not token:
        return redirect("login")

    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(API_USER_ME_URL, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            return render(request, "perfil.html", {"user": user_data})
    except Exception:
        pass

    return redirect("login")
