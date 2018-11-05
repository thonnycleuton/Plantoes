import datetime

from dateutil.rrule import rrule, DAILY, MO, TU, WE, TH, FR, SA, SU
from django.forms import forms
from sorteio.models import Defensor, Sorteio


class SorteioForm(forms.Form):

    def sortear(self):
        # TODO: Testar se ha defensores com datas vizinhas

        defensores = Defensor.objects.all().order_by('?')
        dt_inicial = datetime.date(2019, 1, 7)
        dt_final = datetime.date(2020, 1, 6)

        workdays = rrule(DAILY, dtstart=dt_inicial, until=dt_final, byweekday=(MO, TU, WE, TH, FR))
        weekends = rrule(DAILY, dtstart=dt_inicial, until=dt_final, byweekday=(SA, SU))

        count = 0
        # laço para geração de sorteio para dias úteis da semana
        for day in workdays:

            while not Sorteio.objects.filter(data=day.date()).first():

                defensor = defensores[count]

                if not defensor.afastamento_inicial <= day.date() <= defensor.afastamento_final:
                    Sorteio.objects.create(data=day, defensor=defensor)
                else:
                    data_realocamento = self.get_next_day(workdays, day)
                    Sorteio.objects.create(data=data_realocamento, defensor=defensor)
                count = count + 1 if count < len(defensores) - 1 else 0

        count = 0

        # laço para geração de sorteio para dias de fim de semana
        for day in weekends:

            while not Sorteio.objects.filter(data=day.date()).first():

                defensor = defensores[count]

                # se o defensor não estiver de ferias na data do laço o sorteio é realizado
                if not defensor.afastamento_inicial <= day.date() <= defensor.afastamento_final:
                    Sorteio.objects.create(data=day, defensor=defensor)
                # caso contrário, ele é realocado para o primeiro dia após seu retorno
                else:
                    # escolhe uma data de realocação
                    data_realocamento = self.get_next_day(weekends, day)
                    Sorteio.objects.create(data=data_realocamento, defensor=defensor)
                count = count + 1 if count < len(defensores) - 1 else 0

    # Pega o proximo dia disponivel em uma dada lista
    @staticmethod
    def get_next_day(lista, dia):
        """Metodo para buscar a próxima data disponível em uma dada lista"""
        for l in lista:
            if l >= dia + datetime.timedelta(days=1):
                return l
