import os
import time
import subprocess
from django.conf import settings
from .models import Host, Config
from django.contrib.auth.models import User


def generate_caddyfile():
    project = settings.BASE_DIR
    caddyfilepath = project + '/caddyfile.conf'
    # os.remove(caddyfilepath)
    print(caddyfilepath)
    print(os.remove(caddyfilepath))
    print('Caddyfile deleted')
    caddyfile = open(caddyfilepath, "w+")

    user = User.objects.get(pk=1)
    host_set = Host.objects.all()
    config = Config.objects.get(pk=1)

    for caddyhost in host_set:
        print('Generating ' + caddyhost.host_name)
        domain = caddyhost.host_name + ' { \n \n'
        print('Proxy ' + caddyhost.proxy_host)
        proxy = 'proxy / ' + caddyhost.proxy_host + ' { \n' \
                'transparent \n' \
                'insecure_skip_verify' \
                '  } \n'

        if caddyhost.tls:
            print('TLS ' + user.email)
            caddytls = 'tls ' + user.email + '\n } \n \n'
            caddyfile.write(domain + proxy + caddytls)

        else:
            print('No TLS ')
            proxy = proxy + '} \n \n'
            caddyfile.write(domain + proxy)

    caddyfile = open(caddyfilepath, "a")
    print('Generating default host' + config.interface)
    domain = config.interface + ' { \n \n'

    proxy = 'proxy / ' + config.proxy_host + ' { \n' \
                                             'transparent \n' \
                                             'except /assets \n' \
                                             '} \n \n'
    root = 'root /apps/TygerCaddy/TygerCaddy/ \n' \
           '} \n'
    caddyfile.write(domain + proxy + root)
    print('Finished')

    with open(project + '/caddypid.txt', 'r') as caddyservice:
        caddypid = caddyservice.read().replace('\n', '')
        print(caddypid)

    command = "kill -s USR1 " + caddypid
    print(command)
    reload = subprocess.run(command, shell=True)
    print(reload)
    return True






