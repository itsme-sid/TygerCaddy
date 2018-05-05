from django.db import models

# Create your models here.

class Local(models.Model):
    interface = models.CharField(max_length=200, blank=False)
    proxy_host = models.CharField(max_length=200, blank=True)