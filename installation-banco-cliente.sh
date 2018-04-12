# script de instalación en las máquinas.
# Asegurarse de que esté nginx instalado: sudo apt install nginx -y

# Permitir los paquetes en backports
sudo su
echo "deb http://ftp.debian.org/debian stretch-backports main" | tee -a /etc/apt/sources.list.d/certbot-nginx.list
apt-get update

# Instalar certbot para la certificación.
apt-get install python-certbot-nginx -t stretch-backports -y

# Correr CertBot para que nos de los certificados
certbot --authenticator webroot --installer nginx

# Ahora pasamos a instalar el repo en las máquinas.
cd /var/www/
git clone https://github.com/Proyectos-AP/RedesIII_CI5833.git
apt-get install python3-venv -y

# Configuración del vendedor
cd RedesIII_CI5833/banco-cliente
python3 -m venv env

# Activar sudo su aquí
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Crear la BD de sqlite.
cd bancoCliente
python manage.py migrate

# Copiar la config de Nginx.
cd ../nginx
rm /etc/nginx/sites-avaiable/default
cp conf.d/default-banco-cliente.conf /etc/nginx/sites-avaiable/default
service nginx stop
service nginx start

# Gunicorn para servir la app.
cd ../banco-cliente
gunicorn --bind 127.0.0.1:8080 bancoCliente.wsgi
