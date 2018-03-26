from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from bancoCliente.models import *

# Create your views here.
def index(request):
    return render(request, 'bancoCliente/index.html')

# Create your views here.
def crearCuenta(request):
    return render(request, 'bancoCliente/formCrearCuenta.html')

# Create your views here.
def procesarDatosCuenta(request):
    print("Este es el post del form: ",request.POST)
    respuesta = request.POST

    cuenta   = Cuentas(tdc_number=respuesta['tdc'],
    				   saldo =1000000 )

    cuenta.save()
    pregunta = Preguntas(pregunta=respuesta['pregunta_seguridad'],
    					respuesta=respuesta['respuesta_seguridad'],
    					cuenta = cuenta)

    pregunta.save() 
    # Se almacena la información de la base de datos
    return render(request, 'bancoCliente/formCrearCuenta.html')

