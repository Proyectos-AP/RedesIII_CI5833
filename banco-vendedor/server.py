import socket
import pickle
import ssl
import bdBancoVendedor 
from pony.orm import *
from mensaje import *
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR

KEYFILE = './certificados/server.key'
CERTFILE = './certificados/server.crt'



@db_session
def check_message(mensaje):

    # Se verifica si existe la cuenta del vendedor en la base 
    # de datos
    cuenta_vendedor = select(c for c in bdBancoVendedor.Cuenta if c.idVendedor == mensaje.idVendedor)[:]

    if (len(cuenta_vendedor) == 0):

        # Se retorna un mensaje de error
        return ResponseMessage(401,"Error: No existe la cuenta del vendedor")

    else:
        cuenta = cuenta_vendedor[0]
        # Se ajusta el saldo del vendedor
        print("Monto de antes: ",cuenta.monto)
        cuenta.monto = cuenta.monto + mensaje.monto
        commit()

        # Se retorna un mensaje de exito
        return ResponseMessage(200,"Exito")

def echo_client(s):

    # Se recibe la informacion del cliente
    data = s.recv(8192)
    data = pickle.loads(data)
    print("El mensaje es:",data.mensaje)

    # Se verifica la cuenta del vendedor
    response_message = check_message(data)

    # Se envia el mensaje de respuesta al cliente
    s.send(pickle.dumps(response_message))
    print('Connection closed')


def echo_server(address):
    s = socket.socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    s_ssl = ssl.wrap_socket(s, keyfile=KEYFILE, certfile=CERTFILE, server_side=True)

    while True:
        try:
            (c,a) = s_ssl.accept()
            echo_client(c)
        except socket.error as e:
            print('Error: {0}'.format(e))
            c.close()

echo_server((socket.gethostbyname('www.r3bancovendedor.tk'), 8082))