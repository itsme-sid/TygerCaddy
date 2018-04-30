from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator

from django.views.generic import ListView

from hosts.models import Host

# Create your views here.


class IndexView(ListView):
    template_name = 'dashboard/index.html'
    context_object_name = 'hosts'
    queryset = Host.objects.order_by('id')
    paginate_by = 10
    title = 'Dashboard'
