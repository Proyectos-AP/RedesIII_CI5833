from axes.utils import reset
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from sales.models import Product, Receipt
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import requests
import json

URL_BANCO_CLIENTE = "http://127.0.0.1:8080/"
USERS_ATTEMPT = dict()
# Create your views here.
def index(request):

    p = Product(description="Audifonos",amount=15550.50,vendor="R1234")
    p.save()
    return render(request, 'sales/index.html')

def register(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']

            user = User.objects.create_user(username=username,password=password)
            user.save()


            return render(request,'sales/index.html')
        except:
            return render(request,'sales/error.html')

    else:
        return render(request,'sales/register.html')

def login_view(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        # Verify Captcha
        session = requests.Session()
        params = {
            'secret': settings.CAPTCHA_SECRET_KEY,
            'response': request.POST['g-recaptcha-response'],
            }
        response = session.post("https://www.google.com/recaptcha/api/siteverify", data=params)
        json_data = json.loads(response.text)

        if json_data['success']:
            # Verify user credentials.
            # First take into account if the user is locked.
            if (username in USERS_ATTEMPT.keys() and USERS_ATTEMPT[username] > 3):
                return render(request,'sales/locked.html')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                USERS_ATTEMPT[username] = 0

                user    = User.objects.get(username=username)
                previous_purchases = Receipt.objects.filter(client=user)


                # Redirect to sales platform
                products_list = Product.objects.all()
                print("Productos", products_list)
                print("TOKEN", get_token(request))
                context = {
                    'products_list': products_list,
                    'url': URL_BANCO_CLIENTE,
                    'username': username,
                    'previous_purchases': previous_purchases
                    }
                return render(request,'sales/platform.html',context)
            else:
                # Authentication failhere, we must count
                if username in USERS_ATTEMPT.keys():
                    USERS_ATTEMPT[username] += 1
                else:
                    USERS_ATTEMPT[username] = 1

                return render(request,'sales/login.html')
        else:
            return render(request,'sales/login.html')

        # Verify if the user is blocked
        # Verify number of login attempts
    else:
        return render(request,'sales/login.html')

def logout_view(request):
    logout(request)
    return render(request,'sales/index.html')

@login_required(login_url='/login/')
def platform(request):
    if request.method == 'POST':
        # Process a transaction
        print("Process a transaction")
    else:
        products_list = Product.objects.all()
        previous_purchases = Receipt.objects.filter(client=request.user)
        print("Productos", products_list)
        context = {
            'products_list': products_list,
            'url': URL_BANCO_CLIENTE
            }
        return render(request,'sales/platform.html',context)

def locked(request):
    return render(request,'sales/locked.html')

@csrf_exempt
def create_bill(request):
    print("Se esta creando la factura")
    print(request.POST)
    respuesta = request.POST

    # Se crea la factura del usuario
    user    = User.objects.get(username=respuesta['idComprador'])
    producto = Product.objects.get(pk=respuesta['idProducto'])
    factura = Receipt(client=user,product=producto)
    factura.save()
    
    return HttpResponse('200')


def unlock(request):
    if request.method == 'POST':
        username = request.POST['username']
        reset(username=username)
        USERS_ATTEMPT[username] = 0
        return(render(request,'sales/index.html'))

    else:
        return(render(request,'sales/unlock.html'))
