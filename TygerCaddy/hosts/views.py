from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from.models import Host
from .caddyfile import generate_caddyfile

# Create your views here.


class CreateHost(LoginRequiredMixin, CreateView):
    model = Host
    fields = ['host_name', 'proxy_host', 'root_path', 'tls']
    title = 'Add Host'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):

        form.save()
        caddy = generate_caddyfile()
        return redirect(reverse_lazy('dashboard'))


class UpdateHost(LoginRequiredMixin, UpdateView):
    model = Host
    fields = ['host_name', 'proxy_host', 'root_path']
    slug_field = 'host_name'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):

        form.save()
        caddy = generate_caddyfile()
        return redirect(reverse_lazy('dashboard'))


class DeleteHost(LoginRequiredMixin, DeleteView):
    model = Host
    title = "Delete Host"
    success_url = reverse_lazy('dashboard')

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        self.object.delete()
        caddy = generate_caddyfile()
        return HttpResponseRedirect(self.get_success_url())


def generate(request):
    run = generate_caddyfile()
    return redirect('/dashboard')