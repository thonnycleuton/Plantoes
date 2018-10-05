from django.conf.urls import url

from sorteio.views import ComarcaList

urlpatterns = [
    url(r'comarcas/', ComarcaList.as_view(), name='comarca_list'),
]
