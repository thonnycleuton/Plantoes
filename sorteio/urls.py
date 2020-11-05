from django.conf.urls import url
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView, LoginView, LogoutView

from sorteio.views import *

urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
    url(r'sorteio', SorteioFormView.as_view(), name='sorteio_form'),
    url(r'comarcas/', ComarcaList.as_view(), name='comarca_list'),
    url(r'defensores/', DefensorList.as_view(), name='defensore_list'),
    url(r'^defensor_details/(?P<pk>\d+)/$', DefensorDetail.as_view(), name='defensor_detail'),
    url(r'feriados/', FeriadoList.as_view(), name='feriado_list'),
    url(r'afastamentos/', AfastamentoListView.as_view(), name='afastamento_list'),
    url(r'novo_afastamento/', AfastamentoFormView.as_view(), name='afastamento_create'),

    url(r'^password_reset/$', PasswordResetView.as_view(email_template_name='registration/password_reset_email.html', template_name='registration/password_reset.html'), name='password_reset'),
    url(r'^password_reset/done/$', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    url(r'^entrar/$', LoginView.as_view(), name='login'),
    url(r'^sair/$', LogoutView.as_view(), name='logout'),
]
