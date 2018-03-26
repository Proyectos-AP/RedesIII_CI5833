from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from sales.models import Client

# Create your views here.

def index(request):
    return render(request, 'sales/index.html')

def register(request):


    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['psw']

            #Debe tener una longitud mínima, al menos un carácter no alfa numérico y una letra mayúscula
            user = Client(username=username,password=password)
            user.save()
            return render(request,'sales/index.html')
        except:
            print("Error registrando al usuario")
            return HttpResponse("Error")

    else:
        return render(request,'sales/register.html')

def login(request):
    return render(request,'sales/login.html')

def logout(request):
    return HttpResponse("Logout")

def platform(request):
    return render(request,'sales/platform.html')
