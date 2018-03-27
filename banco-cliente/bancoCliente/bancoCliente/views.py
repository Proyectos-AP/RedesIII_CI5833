from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
from django.template import loader
from bancoCliente.models import *
import crypt
import hashlib
import requests
import json

MONTO = 1000
ID_VENDEDOR = "J-1234"

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

def verificarSaldo(cuenta,monto):

	if (cuenta.saldo>=monto):

		cuenta.saldo = cuenta.saldo - monto
		cuenta.save()
		return True

	return False

# Se muestra el index de la pagina.
def index(request):
    return render(request, 'bancoCliente/index.html')


# Se muestran las preguntas secretas.
def preguntaSecreta(request):

	respuesta = request.POST

	# Se busca la cuenta dentro de la base de datos
	cuenta = Cuentas.objects.filter(ci=respuesta['ci'])

	# Se verifica el Captcha
	session = requests.Session()
	params = {
	    'secret': settings.CAPTCHA_SECRET_KEY,
	    'response': request.POST['g-recaptcha-response'],
	}

	response = session.post("https://www.google.com/recaptcha/api/siteverify", data=params)
	json_data = json.loads(response.text)

	print("Este es el json de respuesta: ",json_data)

	# Si no existe la cuenta se lanza un mensaje de error
	if (len(cuenta)<=0):
		print("Mostrar mensaje de error")
		return render(request, 'bancoCliente/index.html',
					{'mensaje':"No existe una cuenta asociada a dicha cédula."})
	
	elif (not(json_data['success'])):
		# Si el Captcha no paso la prueba, se lanza un mensaje de error.
		return render(request, 'bancoCliente/index.html',
					{'mensaje':"Problemas con el Captcha."})

	else:
		cuenta    = cuenta[0]

		# Se verifica la tarjeta de crédito
		if (comparador(respuesta['tdc'],cuenta.tdc_number)):

			preguntas = Preguntas.objects.filter(cuenta=cuenta)
			preguntas = preguntas[0]

			# Se muestra la pregunta secreta
			return render(request, 
						'bancoCliente/preguntas.html',
						{'pregunta':preguntas.pregunta,
						'idCuenta' :cuenta.id})

		return render(request, 'bancoCliente/index.html',
					{'mensaje':"El número de la tarjeta de crédito es incorrecto."})

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
		print(comparador(respuesta['respuesta'],preguntas.respuesta))

		if (comparador(respuesta['respuesta'],preguntas.respuesta)):
			# Se verifica si el comprador tiene el dinero necesario para
			# realizar la compra.
			if (verificarSaldo(cuenta,MONTO)):

				# Aquí se hace la comunicación con el banco del vendedor
				return render(request, 'bancoCliente/notificacion.html',
							{'mensaje':"Se está procesando el pago."})

			else:
				# Mensaje de error.
				return render(request, 'bancoCliente/notificacion.html',
							{'mensaje':"Su saldo no es suficiente."})


		return render(request, 'bancoCliente/notificacion.html',
					{'mensaje':"La respuesta a la pregunta secreta es incorrecta."})

# Se muestra el form para crear una nueva cuenta.
def crearCuenta(request):
    return render(request, 'bancoCliente/formCrearCuenta.html')

# Se almacenan los datos de la nueva cuenta.
def procesarDatosCuenta(request):
    print("Este es el post del form: ",request.POST)
    respuesta = request.POST

    tdc                 = encriptar(respuesta['tdc'])
    numero_secreto      = encriptar(respuesta['numero_secreto'])
    fecha_vencimiento   = encriptar(respuesta['fecha_vencimiento'])
    respuesta_seguridad = encriptar(respuesta['respuesta_seguridad'])

    print("TDC: ",tdc)
    print("Número secreto: ",encriptar(respuesta['numero_secreto']))
    print("Fecha vencimiento: ",encriptar(respuesta['fecha_vencimiento']))

    print(comparador(respuesta['tdc'], tdc))

    cuenta   = Cuentas(	ci                = respuesta['ci'],
    					tdc_number        = tdc,
    					secret_number     = numero_secreto,
    					fecha_vencimiento = fecha_vencimiento,
    					saldo             = 1000000 )

    cuenta.save()
    pregunta = Preguntas(pregunta=respuesta['pregunta_seguridad'],
    					respuesta=respuesta_seguridad,
    					cuenta = cuenta)

    # Se almacena la información de la base de datos
    pregunta.save()

    return render(request, 'bancoCliente/cuentaCreada.html')

