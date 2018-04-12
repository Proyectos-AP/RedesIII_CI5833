from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from bancoCliente.models import *
from decimal import Decimal
import crypt
import hashlib
import requests
import json
import pickle 
import socket, ssl

MONTO = 0
ID_VENDEDOR = ""
COMPRADOR = ""
ID_PRODUCTO = ""


def comunicacion_banco_vendedor(idVendedor,idComprador,monto,idProducto):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(s,cert_reqs=ssl.CERT_REQUIRED, ca_certs=settings.PATH_CERTIFICATE)
    ssl_sock.connect((settings.URL_BANCO_VENDEDOR, int(settings.PUERTO_BANCO_VENDEDOR) ))

    print("Se esta realizando la comunicación con el banco del vendedor...")
    # Se contruye el mensaje que se va a enviar al banco del vendedor
    paquete = {"id": 10, "idVendedor":idVendedor,
                "idComprador":idComprador, "monto": monto,
                "idProducto" : idProducto,
                "mensaje": "Batch al banco del vendedor"}

    ssl_sock.write(pickle.dumps(paquete))
    # Se envia el mensaje
    data = ssl_sock.recv(8192)

    # Se recibe el mensaje de respuesta del servidor
    data = pickle.loads(data)

    ssl_sock.close()

    if (data["id"] == 200):
        return True
    else:
        return False

@csrf_exempt
def encriptar(mensaje):

    algo = "sha512".encode('utf-8')

    mensaje = str(mensaje).encode('utf-8')

    # Se crea el bit de salt
    salt = crypt.mksalt(crypt.METHOD_SHA512).split("$")[-1].encode('utf-8')

    # Se encripta el mensaje
    hash_object = hashlib.sha512(salt+mensaje)

    return '%s$%s$%s' % (algo.decode('utf-8'), salt.decode('utf-8'), hash_object.hexdigest())

@csrf_exempt
def comparador(raw_password, enc_password):

    algo, salt, hsh = enc_password.split('$')
    raw_password = str(raw_password).encode('utf-8')

    return hsh == hashlib.sha512(salt.encode('utf-8')+raw_password).hexdigest()

# Se muestra el index de la pagina.
@csrf_exempt
def index(request):
    respuesta = request.POST
    global ID_VENDEDOR 
    global MONTO
    global COMPRADOR
    global ID_PRODUCTO

    ID_VENDEDOR = respuesta['vendor']
    MONTO       = Decimal(respuesta['price'].strip(' "'))
    COMPRADOR   = respuesta['comprador']
    ID_PRODUCTO = respuesta['idProducto']

    print("El usuario "+COMPRADOR+" ha realizado conexión con el banco"+
        " para pagar el producto con ID "+ID_PRODUCTO +" perteneciente"+
        " al vendedor "+ID_VENDEDOR)

    return render(request, 'bancoCliente/index.html')


# Se muestran las preguntas secretas.
@csrf_exempt
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

@csrf_exempt
def confirmarPregunta(request):

    respuesta = request.POST
    cuenta = Cuentas.objects.get(pk=respuesta['id_cuenta'])

    if (not(cuenta)):
        return render(request, 'bancoCliente/index.html',
                    {'mensaje':"El número de la tarjeta de crédito es incorrecto."})


    preguntas = Preguntas.objects.filter(cuenta=cuenta)
    preguntas = preguntas[0]

    if (comparador(respuesta['respuesta'],preguntas.respuesta)):
        # Se verifica si el comprador tiene el dinero necesario para
        # realizar la compra.
        if (cuenta.saldo>=MONTO):

            # Aquí se hace la comunicación con el banco del vendedor
            exito = comunicacion_banco_vendedor(ID_VENDEDOR,COMPRADOR,MONTO,ID_PRODUCTO)

            # Caso en el que la transaccion con el vendedor se hizo de manera
            # exitosa
            if (exito):

                print("Se realizó con exito la comunicación con el banco del vendedor...")

                saldo_anterior = cuenta.saldo
                # Se modifica el saldo del comprador
                cuenta.saldo = cuenta.saldo - MONTO
                cuenta.save()

                print("El usuario "+str(cuenta.ci)+" ,antes tenía en su cuenta: "+str(saldo_anterior)+
                        " ,pero se le descontaron "+str(MONTO)+" debido a un compra realizada."+
                    " Ahora, su saldo total es: "+str(cuenta.saldo))

                # Se muestra un mensaje de exito
                return render(request, 'bancoCliente/notificacion.html',
                            {'mensaje':"Se procesó el pago."})

            else:

                # Caso en el que la transaccion con el vendedor no se hizo de manera
                # exitosa
                return render(request, 'bancoCliente/notificacion.html',
                            {'mensaje':"Hubo problemas en la transacción."})


        else:
            # Caso en el que el comprador no tiene saldo suficiente para
            # realizar la compra.
            return render(request, 'bancoCliente/notificacion.html',
                        {'mensaje':"Su saldo no es suficiente."})

    else:
        # Caso en el que la respuesta de seguridad se contestó de manera
        # incorrecta
        return render(request, 
                    'bancoCliente/preguntas.html',
                    {'pregunta':preguntas.pregunta,
                    'idCuenta' :cuenta.id,
                    'mensaje':"La respuesta a la pregunta secreta es incorrecta."})

# Se muestra el form para crear una nueva cuenta.
@csrf_exempt
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

    cuenta   = Cuentas(    ci                = respuesta['ci'],
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

