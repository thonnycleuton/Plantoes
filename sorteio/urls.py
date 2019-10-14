from django.conf.urls import url

from sorteio.views import *

urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
    url(r'sorteio', SorteioFormView.as_view(), name='sorteio_form'),
    url(r'comarcas/', ComarcaList.as_view(), name='comarca_list'),
    url(r'defensores/', DefensorList.as_view(), name='defensore_list'),
    url(r'^defensor_details/(?P<pk>\d+)/$', DefensorDetail.as_view(), name='defensor_detail'),
    url(r'feriados/', FeriadoList.as_view(), name='feriado_list'),
    url(r'afastamentos/', AfastamentoFormView.as_view(), name='afastamento_create'),
]
