import datetime

from django.forms import forms

from sorteio.models import Defensor, Sorteio
from sorteio.utils import daterange


class SorteioForm(forms.Form):

    def sortear(self):

        defensores = Defensor.objects.all().order_by('?')
        # TODO: datas poderiam ser parametros de funcao
        dt_inicial = datetime.date(2019, 1, 7)
        dt_final = datetime.date(2020, 1, 6)

        datas = daterange(dt_inicial, dt_final)
        count = 0
        defensores_licensa = []
        for data in datas:

            while not Sorteio.objects.filter(data=data).first():

                defensor = defensores[count]

                if not defensor.afastamento_inicial <= data <= defensor.afastamento_final:
                    Sorteio.objects.create(data=data, defensor=defensor)
                else:
                    defensores_licensa.append(defensor)
                    data_realocamento = defensor.afastamento_final + datetime.timedelta(days=2)
                    Sorteio.objects.create(data=data_realocamento, defensor=defensor)
                count = count + 1 if count < len(defensores) - 1 else 0
