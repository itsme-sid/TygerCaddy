import os
from .models import Host, Config

host = Host
host_set = host.objects.all()
config = Config.objects.get(pk=1)

caddyfilepath = os.path.join('caddyfile.conf')


def generate_caddyfile():

    caddyfile = open(caddyfilepath, "w")

    for caddyhost in host_set:

        domain = host.host_name + ' { \n \n'

        proxy = 'proxy / ' + caddyhost.proxy_host + ' { \n' \
                'proxy_header Host {host} \n' \
                'proxy_header X-Real-IP {remote} \n' \
                'proxy_header X-Forwarded-Proto {scheme} \n' \
                '  } \n' \
                '} \n \n'

        caddyfile.write(domain + proxy)

    caddyfile = open(caddyfilepath, "a")
    domain = config.interface + ' { \n \n'

    proxy = 'proxy / ' + config.proxy_host + ' { \n' \
                                             'transparent' \
                                             'except /assets' \
                                             'proxy_header Host {host} \n' \
                                             'proxy_header X-Real-IP {remote} \n' \
                                             'proxy_header X-Forwarded-Proto {scheme} \n' \
                                             '} \n \n'
    caddyfile.write(domain + proxy)
    return True






