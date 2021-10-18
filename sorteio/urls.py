# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView, LoginView, LogoutView
from django.contrib.auth.decorators import login_required

from sorteio.views import *

urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
    url(r'sorteio/parnaiba', SorteioParnaibaFormView.as_view(), name='sorteio_parnaiba'),
    url(r'sorteio/periodo', SorteioBlocoPeriodoFormView.as_view(), name='sorteio_bloco_periodo'),
    url(r'sorteio', SorteioFormView.as_view(), name='sorteio_form'),
    url(r'comarcas/', ComarcaList.as_view(), name='comarca_list'),

    url(r'defensores/', DefensorList.as_view(), name='defensore_list'),
    url(r'defensor/criar', DefensorCreate.as_view(), name='defensore_create'),
    url(r'defensor/editar/(?P<pk>\d+)/$', DefensorEdit.as_view(), name='defensore_edit'),
    url(r'^defensor/detalhes/(?P<pk>\d+)/$', DefensorDetail.as_view(), name='defensor_detail'),
    url(r'^defensor/deletar/(?P<pk>\d+)/$', DefensorDelete.as_view(), name='defensor_delete'),

    url(r'feriados/', FeriadoList.as_view(), name='feriado_list'),
    url(r'feriado/criar', FeriadoFormView.as_view(), name='feriado_create'),
    url(r'feriado/editar/(?P<pk>\d+)/$', FeriadoEditarFormView.as_view(), name='feriado_edit'),
    url(r'^feriado/detalhes/(?P<pk>\d+)/$', FeriadoDetail.as_view(), name='feriado_detail'),
    url(r'^feriado/deletar/(?P<pk>\d+)/$', FeriadoDelete.as_view(), name='feriado_delete'),

    url(r'afastamentos/', AfastamentoListView.as_view(), name='afastamento_list'),
    url(r'novo_afastamento/', AfastamentoFormView.as_view(), name='afastamento_create'),
    url(r'afastamento/deletar/(?P<pk>\d+)/$', AfastamentoDeleteView.as_view(), name='afastamento_delete'),
]
