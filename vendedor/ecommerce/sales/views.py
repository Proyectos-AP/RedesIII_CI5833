from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from sales.models import Client, Product
import requests
import json

# Create your views here.

def index(request):
    return render(request, 'sales/index.html')

def register(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['psw']
            user = Client(username=username,password=password)
            user.save()
            return render(request,'sales/index.html')
        except:
            return render(request,'sales/error.html')

    else:
        return render(request,'sales/register.html')

def login(request):
    if request.method == 'POST':

        # Verify Captcha
        session = requests.Session()
        params = {
            'secret': settings.CAPTCHA_SECRET_KEY,
            'response': request.POST['g-recaptcha-response'],
            }
        response = session.post("https://www.google.com/recaptcha/api/siteverify", data=params)
        json_data = json.loads(response.text)

        if json_data['success']:
            return render(request,'sales/platform.html')
        else:
            return render(request,'sales/login.html')

        # Verify if the user is blocked

        # Verify number of login attempts

        # Verify user credentials


        # Redirect to sales platform
        return render(request,'sales/platform.html')
    else:
        return render(request,'sales/login.html')

def logout(request):
    return HttpResponse("Logout")

def platform(request):
    if request.method == 'POST':
        # Process a transaction
        print("Process a transaction")
    else:

        products_list = Product.objects.all()
        context = {
            'products_list': products_list,
            }
        return render(request,'sales/platform.html',context)
