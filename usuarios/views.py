from django.core.checks import messages
from django.shortcuts import redirect, render
from django.views.generic import CreateView
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