import ssl
import pickle 
from mensaje import *

port = 8082

import socket, ssl

while True:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Require a certificate from the server. We used a self-signed certificate
    # so here ca_certs must be the server certificate itself.
    ssl_sock = ssl.wrap_socket(s,cert_reqs=ssl.CERT_REQUIRED, ca_certs='./certificados/server.crt')

    ssl_sock.connect(('www.r3bancovendedor.tk', 8082))

    mensaje = str(input("Enter Something: "))

    # Se contruye el mensaje que se va a enviar al cliente
    paquete = Mensaje(10,"R1234","23695172",150,mensaje)

    ssl_sock.write(pickle.dumps(paquete))
    # Se envia el mensaje
    data = ssl_sock.recv(8192)

    # Se recibe el mensaje de respuesta del servidor
    data = pickle.loads(data)
    print("El mensaje es:",data.mensaje)

    ssl_sock.close()