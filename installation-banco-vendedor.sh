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
cd RedesIII_CI5833/banco-vendedor
python3 -m venv env

# Activar sudo su aquí
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Crear la BD de sqlite.
python bdBancoVendedor.py
python add.py
cd ..

# Copiar la config de Nginx.
# cd ../nginx
# rm /etc/nginx/sites-available/default
# cp conf.d/default-banco-vendedor.conf /etc/nginx/sites-available/default
# service nginx stop
# service nginx start

# Gunicorn para servir la app.
cd ../banco-cliente/bancoCliente
python server.py
