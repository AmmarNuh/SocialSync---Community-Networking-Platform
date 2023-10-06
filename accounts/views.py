from django.shortcuts import render
from django.urls import reverse,reverse_lazy # when login or logout
from django.shortcuts import reverse 
from django.views.generic import TemplateView, CreateView


from . import forms
# Create your views here.
class SignUp(CreateView):
    # revers to login page after succcess signup
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'