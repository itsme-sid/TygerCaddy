import os
from .models import Host

host = Host
host_set = host.objects.all()

caddyfilepath = os.path.join('caddyfile.conf')


def generate_caddyfile():

    caddyfile = open(caddyfilepath, "w")

    for host in host_set:

        domain = host.host_name + ' { \n \n'

        proxy = 'proxy / ' + host.proxy_host + ' { \n' \
                'proxy_header Host {host} \n' \
                'proxy_header X-Real-IP {remote} \n' \
                'proxy_header X-Forwarded-Proto {scheme} \n' \
                '  } \n' \
                '} \n \n'

        caddyfile.write(domain + proxy)

    return True






