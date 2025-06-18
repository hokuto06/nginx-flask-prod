from django.shortcuts import render

def home(request):
    return render(request, 'projects/home.html')

def project_email(request):
    return render(request, 'projects/email-project.html')

def project_template(request):
    return render(request, 'projects/template-project.html')

def docker_project(request):
    return render(request, 'projects/docker-project.html')