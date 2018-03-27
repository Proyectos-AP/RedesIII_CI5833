from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from bancoCliente.models import *

# Se muestra el index de la pagina.
def index(request):
    return render(request, 'bancoCliente/index.html')


# Se muestran las preguntas secretas.
def preguntaSecreta(request):

	respuesta = request.POST
	cuenta = Cuentas.objects.filter(tdc_number=respuesta['tdc'])
	
	if (len(cuenta)<=0):
		print("Mostrar mensaje de error")
		return render(request, 'bancoCliente/index.html',
					{'mensaje':"El número de la tarjeta de crédito es incorrecto."})
		
	else:
		cuenta    = cuenta[0]
		preguntas = Preguntas.objects.filter(cuenta=cuenta)
		preguntas = preguntas[0]

	return render(request, 
				'bancoCliente/preguntas.html',
				{'pregunta':preguntas.pregunta,
				'idCuenta' :cuenta.id})

def confirmarPregunta(request):

	respuesta = request.POST
	cuenta = Cuentas.objects.get(pk=respuesta['id_cuenta'])

	if (not(cuenta)):
		print("Mostrar mensaje de error")
		return render(request, 'bancoCliente/index.html',
					{'mensaje':"El número de la tarjeta de crédito es incorrecto."})

	else:
		preguntas = Preguntas.objects.filter(cuenta=cuenta)
		preguntas = preguntas[0]

		if (preguntas.respuesta == respuesta['respuesta']):

			# Aqui se hace la comunicación con el banco del vendedor
			return render(request, 'bancoCliente/notificacion.html',
						{'mensaje':"Se está procesando el pago."})

	return render(request, 'bancoCliente/notificacion.html',
				{'mensaje':"La respuesta a la pregunta secreta es incorrecta."})

# Se muestra el form para crear una nueva cuenta.
def crearCuenta(request):
    return render(request, 'bancoCliente/formCrearCuenta.html')

# Se almacenan los datos de la nueva cuenta.
def procesarDatosCuenta(request):
    print("Este es el post del form: ",request.POST)
    respuesta = request.POST

    cuenta   = Cuentas(tdc_number=respuesta['tdc'],
    				   saldo = 1000000 )

    cuenta.save()
    pregunta = Preguntas(pregunta=respuesta['pregunta_seguridad'],
    					respuesta=respuesta['respuesta_seguridad'],
    					cuenta = cuenta)

    # Se almacena la información de la base de datos
    pregunta.save()

    return render(request, 'bancoCliente/cuentaCreada.html')

