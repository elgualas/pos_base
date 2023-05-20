from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
# Create your views here.

class SinPrivilegios(LoginRequiredMixin,PermissionRequiredMixin):
    login_url="bases:login"
    raise_exception=False
    redirect_field_name="redirect_to"

    def handle_no_permission(self):
        from django.contrib.auth.models import AnonymousUser
        if not self.request.user==AnonymousUser():
            self.login_url='bases:sin_privilegios'
        self.login_url='bases:sin_prvilegios'
        return HttpResponseRedirect(reverse_lazy(self.login_url))

class Home(LoginRequiredMixin,generic.TemplateView):
    template_name= 'bases/home.html'
    login_url='bases:login'

class HomeSinPrivilegios(LoginRequiredMixin,generic.TemplateView):
    template_name= 'bases/sin_privilegios.html'
    
