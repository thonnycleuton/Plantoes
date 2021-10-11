from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^entrar/$', LoginView.as_view(), name='login'),
    url(r'^sair/$', LogoutView.as_view(), name='logout'),
]
