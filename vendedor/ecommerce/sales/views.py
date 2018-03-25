from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

# Create your views here.

def index(request):
    return render(request, 'sales/index.html')

def register(request):


    if request.method == 'POST':

        username = request.POST['username']
        name = request.POST['name']
        last_name = request.POST['lastName']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username,email,password)

        user.first_name = name
        user.last_name = last_name
        user.save()

        return render(request,'sales/index.html')

    else:
        return render(request,'sales/register.html')

def login(request):
    return render(request,'sales/login.html')

def logout(request):
    return HttpResponse("Logout")

def platform(request):
    return render(request,'sales/platform.html')
