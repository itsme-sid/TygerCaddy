from django.db import models
from django.urls import reverse

# Create your models here.


class Host(models.Model):
    host_name = models.CharField(max_length=200, blank=False, unique=True)
    proxy_host = models.CharField(max_length=200, blank=True)
    root_path = models.CharField(max_length=200, blank=True)

    def get_absolute_url(self):
        return reverse('host-detail', kwargs={'host': self.host_name})