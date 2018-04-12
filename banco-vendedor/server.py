import socket
import pickle
import ssl
import json
import requests
import bdBancoVendedor
from pony.orm import *
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR

KEYFILE = '/etc/nginx/certificados/banco-vendedor.key'
CERTFILE = '/etc/nginx/certificados/banco-vendedor.crt'
URL_VENDEDOR = 'https://a4.ac.labf.usb.ve/crearFactura/'



@db_session
def check_message(mensaje):

    # Se verifica si existe la cuenta del vendedor en la base
    # de datos
    cuenta_vendedor = select(c for c in bdBancoVendedor.Cuenta if c.idVendedor == mensaje["idVendedor"])[:]

    if (len(cuenta_vendedor) == 0):

        # Se retorna un mensaje de error
        return {"id":401, "mensaje":"Error: No existe la cuenta del vendedor"}

    else:
        cuenta = cuenta_vendedor[0]
        # Se ajusta el saldo del vendedor
        cuenta.monto = cuenta.monto + mensaje["monto"]
        print("Se acaban de sumar: "+str(mensaje["monto"])+
            " en la cuenta de "+ mensaje["idVendedor"]+
            ". Su saldo ahora es de: "+str(cuenta.monto))
        commit()

        # Se retorna un mensaje de exito
        return {"id":200, "mensaje":"Exito"}

# Función que se encarga de informarle al la pagina del vendedor que la
# compra fue efectuara de forma satisfactoria
def inform_vendor_page(mensaje):
    response = requests.post(URL_VENDEDOR, data = mensaje)


def echo_client(s):

    # Se recibe la informacion del cliente
    data = s.recv(8192)
    data = pickle.loads(data)

    # Se verifica la cuenta del vendedor
    response_message = check_message(data)

    # Se envia el mensaje de respuesta al cliente
    s.send(pickle.dumps(response_message))
    print('Se cierra la conexión con el banco del cliente...')

    # Se le informa al vendedor que la compra fue realizada de
    # manera exitosa
    if (response_message["id"] == 200):
        inform_vendor_page(data)
        print("Se le informa al vendedor "+data["idVendedor"]+" que la compra"+
            " del usuario "+data["idComprador"]+" ,por el monto de "+str(data["monto"])
            +" ya fué realizada.")


def echo_server(address):
    s = socket.socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    s_ssl = ssl.wrap_socket(s, keyfile=KEYFILE, certfile=CERTFILE, server_side=True)
    print("El banco del vendedor está funcionando...")
    while True:
        try:
            (c,a) = s_ssl.accept()
            # Se realiza la conexión con el banco del cliente
            # y el vendedor
            echo_client(c)

        except socket.error as e:
            print('Error: {0}'.format(e))
            c.close()

# echo_server((socket.gethostbyname('www.r3bancovendedor.tk'), 8082))
echo_server((socket.gethostbyname('a2.ac.labf.usb.ve'), 443))
