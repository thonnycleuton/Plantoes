import datetime

from django.forms import forms

from sorteio.models import Defensor, Sorteio
from sorteio.utils import daterange


class SorteioForm(forms.Form):

    def sortear(self):

        defensores = Defensor.objects.all()
        # TODO: datas poderiam ser parametros de funcao
        dt_inicial = datetime.date(2019, 1, 7)
        dt_final = datetime.date(2020, 1, 6)

        datas = daterange(dt_inicial, dt_final)

        count = 1
        for data in datas:
            Sorteio.objects.create(data=data, defensor=defensores.get(pk=count))
            count = count + 1 if count < len(defensores) else 1
