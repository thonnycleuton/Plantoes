# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.checks import messages
from django.shortcuts import redirect, render
from django.views.generic.base import View 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
class LoginView(View):

    def get(self, request):
        return render(request, 'usuarios/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'Verifique as credenciais digitadas e tente novamente')
        return redirect('/usuario/entrar')

class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/')


class ChangePasswordView(LoginRequiredMixin, View):
    login_url = '/usuario/entrar'
    redirect_field_name = 'redirect_to'
    
    def get(self, request):
        return render(request, 'usuarios/change_password.html')

    def post(self, request):
        senha_atual = request.POST.get('senha_atual')
        nova_senha = request.POST.get('nova_senha')

        if self.dados_validos_para_alterar_senha(request, senha_atual):
            user = request.user
            user.set_password(nova_senha)
            user.save()
            user_login = authenticate(request, username=user.username, password=senha_atual)
            login(request, user_login)
            return redirect('/')
        return redirect('/usuario/senha/alterar')

    def dados_validos_para_alterar_senha(self, request, senha_atual):
        valido = True
        username = request.user.username
        user = authenticate(request, username=username, password=senha_atual)

        if user is None:
            messages.add_message(request, messages.INFO, 'A senha informada está incorreta')
            valido = False
        return valido