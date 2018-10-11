from django.conf.urls import url

from sorteio.views import ComarcaList

urlpatterns = [
    url(r'comarcas/', ComarcaList.as_view(), name='comarca_list'),
    url(r'defensores/', ComarcaList.as_view(), name='defensore_list'),
    url(r'feriados/', ComarcaList.as_view(), name='feriado_list'),
]
