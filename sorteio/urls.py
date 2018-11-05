from django.conf.urls import url

from sorteio.views import *

urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
    url(r'sorteio', SorteioFormView.as_view(), name='sorteio_form'),
    url(r'comarcas/', ComarcaList.as_view(), name='comarca_list'),
    url(r'defensores/', DefensorList.as_view(), name='defensore_list'),
    url(r'feriados/', FeriadoList.as_view(), name='feriado_list'),
]
