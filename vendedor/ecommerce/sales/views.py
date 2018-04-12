from axes.utils import reset
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template import loader
from sales.models import Product, Receipt, Preguntas
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import requests
import json
import crypt
import hashlib

URL_BANCO_CLIENTE = "http://127.0.0.1:8080/"
USERS_ATTEMPT = dict()


def encriptar(mensaje):

    algo = "sha512".encode('utf-8')

    mensaje = str(mensaje).encode('utf-8')

    # Se crea el bit de salt
    salt = crypt.mksalt(crypt.METHOD_SHA512).split("$")[-1].encode('utf-8')

    # Se encripta el mensaje
    hash_object = hashlib.sha512(salt+mensaje)

    return '%s$%s$%s' % (algo.decode('utf-8'), salt.decode('utf-8'), hash_object.hexdigest())


def comparador(raw_password, enc_password):

    algo, salt, hsh = enc_password.split('$')
    raw_password = str(raw_password).encode('utf-8')

    return hsh == hashlib.sha512(salt.encode('utf-8')+raw_password).hexdigest()


# Create your views here.
def index(request):

    p = Product(description="Audifonos",amount=15550.50,vendor="R1234")
    p.save()
    return render(request, 'sales/index.html')

def register(request):
    if request.method == 'POST':
        try:
            username  = request.POST['username']
            password  = request.POST['password']
            pregunta  = request.POST['pregunta_seguridad']
            respuesta = request.POST['respuesta']

            user = User.objects.create_user(username=username,password=password)
            user.save()

            # Se encripta la respuesta
            respuesta_secreta = encriptar(respuesta)

            # Se almacena la pregunta secreta
            pregunta = Preguntas(usuario=user,pregunta=pregunta,
                                respuesta=respuesta_secreta)
            pregunta.save()


            return render(request,'sales/index.html',
                        {'mensaje_positivo':"El registro se ha realizado de manera satisfatoria"})
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

                return render(request,'sales/login.html',{'mensaje': "Usuario o clave incorrecta"})
        else:
            return render(request,'sales/login.html',{'mensaje': "Problemas con el Captcha"})

        # Verify if the user is blocked
        # Verify number of login attempts
    else:
        return render(request,'sales/login.html')

def logout_view(request):
    logout(request)
    return render(request,'sales/index.html')

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

    body = "Usted ha adquirido el producto con descripción: "+\
            producto.description+" . El monto a pagar fué: "+\
            str(producto.amount)+" y el ID de la factura es: "+\
            str(factura.id)
    # Se envia un correo al usuario con su factura
    email = EmailMessage('Factura de comercio', 
                        body, to=['alejandra.corderogarcia21@gmail.com'])
    email.send()
    
    return HttpResponse('200')


def unlock(request):
    if request.method == 'POST':
        print("Entre aqui!!")

        username = request.POST['username']
        user    = User.objects.get(username=username)

        # Se busca la pregunta perteneciente al usuario
        pregunta = Preguntas.objects.get(usuario=user)

        context = {'pregunta': pregunta.pregunta,
                    'id_pregunta':pregunta.id,
                    'username': username
                    }

        # Redirigimos al form en donde se realizara
        # la pregunta de seguridad
        return(render(request,'sales/preguntas.html',context))

    else:
        return(render(request,'sales/unlock.html'))


def verificarPreguntaSeguridad(request):

    respuesta   = request.POST['respuesta']
    id_pregunta = request.POST['id_pregunta']
    username    = request.POST['username']

    pregunta = Preguntas.objects.get(pk=id_pregunta)

    # Se verifica que la respuesta sea correcta
    if (comparador(respuesta,pregunta.respuesta)):

        reset(username=username)
        USERS_ATTEMPT[username] = 0
        return(render(request,'sales/index.html',
                        {'mensaje_positivo':"Su usuario ha sido desbloqueado"}))
    else:
        context = {'pregunta': pregunta.pregunta,
                    'id_pregunta':pregunta.id,
                    'mensaje': "La respuesta en incorrecta"
                    }

        return(render(request,'sales/preguntas.html',context))
    