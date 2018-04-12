# script de instalación en las máquinas.
# Asegurarse de que esté nginx instalado: sudo apt install nginx -y

# Permitir los paquetes en backports
echo "deb http://ftp.debian.org/debian stretch-backports main" | sudo tee -a /etc/apt/sources.list.d/certbot-nginx.list
sudo apt-get update

# Instalar certbot para la certificación.
sudo apt-get install python-certbot-nginx -t stretch-backports -y

# Correr CertBot para que nos de los certificados
sudo certbot --authenticator webroot --installer nginx

# Ahora pasamos a instalar el repo en las máquinas.
cd /var/www/
sudo git clone https://github.com/Proyectos-AP/RedesIII_CI5833.git
sudo apt-get install python3-venv -y

# Configuración del vendedor
cd RedesIII_CI5833/vendedor
sudo python3 -m venv env

# Activar sudo su aquí
sudo su
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Crear la BD de sqlite.
python manage.py migrate

# Copiar la config de Nginx.

# Gunicorn para servir la app.
gunicorn -c config/gunicorn/conf.py --bind :8080 --chdir ecommerce ecommerce.wsgi:application
