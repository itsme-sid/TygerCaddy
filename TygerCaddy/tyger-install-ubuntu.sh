#!/bin/sh bash
set -eu -o pipefail # fail on error , debug all lines

sudo -n true
test $? -eq 0 || exit 1 "you should have sudo priveledge to run this script"
add-apt-repository ppa:jonathonf/python-3.6
apt update
apt upgrade

echo installing the must-have pre-requisites
while read -r p ; do sudo apt-get install -y $p ; done < <(cat << "EOF"
    zip unzip
    python-pip
    python-dev
    python3.6
    python3-pip
    build-essential
EOF
)

echo installing the pre-requisites
echo you have 5 seconds to proceed ...
echo or
echo hit Ctrl+C to quit
echo -e "\n"
sleep 6
echo Updating system,

apt-get update && apt-get upgrade -y

echo Installing some handy extras...

apt-get install wget git -y
pip3 install --upgrade pip

echo Making the app directories...
mkdir /apps

echo Cloning repository....

cd /apps
git clone https://github.com/morph1904/TygerCaddy.git

echo Installing and setting up CaddyServer
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
cp /apps/TygerCaddy/caddy.service /etc/systemd/system/caddy.service
chown root:root /etc/systemd/system/caddy.service
chmod 744 /etc/systemd/system/caddy.service
systemctl daemon-reload
systemctl enable caddy.service

cd /apps/TygerCaddy/TygerCaddy

echo Setting up initial install....
pip3 install -r requirements.txt

cp /apps/TygerCaddy/uwsgi.service /etc/systemd/system/uwsgi.service
systemctl enable uwsgi.service
systemctl start uwsgi.service


python3 manage.py migrate

USER="admin"
PASS="password"
MAIL="admin@admin.com"
script="
from django.contrib.auth.models import User;
username = '$USER';
password = '$PASS';
email = '$MAIL';
if User.objects.filter(username=username).count()==0:
    User.objects.create_superuser(username, email, password);
    print('Superuser created.');
else:
    print('Superuser creation skipped.');
"
printf "$script" | python3 manage.py shell





