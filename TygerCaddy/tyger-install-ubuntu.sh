#!/bin/sh bash
set -eu -o pipefail # fail on error , debug all lines

sudo -n true
test $? -eq 0 || exit 1 "you should have sudo priveledge to run this script"
add-apt-repository ppa:jonathonf/python-3.6
apt update
apt upgrade -y

echo Installing the app pre-requisites
echo you have 5 seconds to proceed ...
echo or
echo hit Ctrl+C to quit
echo -e "\n"
sleep 6
echo Updating system,
while read -r p ; do sudo apt-get install -y $p ; done < <(cat << "EOF"
    zip unzip
    python-pip
    python-dev
    python3.6
    python3-pip
    build-essential
EOF
)



apt-get update && apt-get upgrade -y

echo Installing some handy extras...
sleep 3
apt-get install wget git -y
pip3 install --upgrade pip
pip3 install uwsgi

echo Making the app directories...
sleep 3
mkdir /apps


echo Cloning repository....
sleep 3

cd /apps
git clone https://github.com/morph1904/TygerCaddy.git
mkdir /apps/TygerCaddy/sites


echo Installing and setting up CaddyServer
sleep 3
apt install curl
curl https://getcaddy.com | bash -s personal hook.service,http.filemanager,http.jwt,http.mailout,http.minify,http.proxyprotocol,http.upload,net,tls.dns.godaddy
chown root:root /usr/local/bin/caddy
chmod 755 /usr/local/bin/caddy
setcap 'cap_net_bind_service=+eip' /usr/local/bin/caddy
mkdir -p /etc/caddy
chown -R root:www-data /etc/caddy
mkdir -p /etc/ssl/caddy
chown -R www-data:root /etc/ssl/caddy
chmod 770 /etc/ssl/caddy
touch /etc/caddy/Caddyfile
mkdir -p /var/www
chown www-data:www-data /var/www
chmod 755 /var/www
echo Setting up services to run on boot...
sleep 3

cp /apps/TygerCaddy/caddy.service /etc/systemd/system/caddy.service
chown root:root /etc/systemd/system/caddy.service
chmod 744 /etc/systemd/system/caddy.service
cp /apps/TygerCaddy/uwsgi.service /etc/systemd/system/uwsgi.service
systemctl daemon-reload
systemctl enable caddy.service
systemctl enable uwsgi.service

cd /apps/TygerCaddy/TygerCaddy

echo Starting base Services.....
sleep 3

service uwsgi start
service caddy start

echo Setting up initial install....
sleep3

pip3 install -r requirements.txt

echo Installing TygerCaddy almost there! We need some input from you here.
sleep 3

python3 manage.py migrate
python3 manage.py loaddata config


read -p 'Please enter a username: ' uservar
read -sp 'Please enter a password: ' passvar
read -p 'Please enter an email address: ' emailvar
echo creating user with your details:
sleep 3
script="
from django.contrib.auth.models import User;
username = '$uservar';
password = '$passvar';
email = '$emailvar';
if User.objects.filter(username=username).count()==0:
    User.objects.create_superuser(username, email, password);
    print('Superuser created.');
else:
    print('Superuser creation skipped.');
"
printf "$script" | python3 manage.py shell

echo Install Complete!, Enter the server IP in your chosen browser and login with username $uservar and the password you provided earlier.





