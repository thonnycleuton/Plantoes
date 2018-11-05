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
                # defensor = defensores_licensa[0] if defensores_licensa[0] else defensores[count]
                if defensores_licensa:
                    defensor = defensores_licensa[0]
                    del defensores_licensa[0]
                else:
                    defensor = defensores[count]
                    count = count + 1 if count < len(defensores) - 1 else 0

                if not defensor.afastamento_inicial <= data <= defensor.afastamento_final:
                    Sorteio.objects.create(data=data, defensor=defensor)
                else:
                    defensores_licensa.append(defensor)
