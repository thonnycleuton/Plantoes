import datetime

from dateutil.rrule import rrule, DAILY, MO, TU, WE, TH, FR, SA, SU
from django.forms import forms
from sorteio.models import Defensor, Sorteio, Feriado


class SorteioForm(forms.Form):

    def verificar_inconsistencia(self):

        sorteados = Sorteio.objects.all()
        count = 0
        verificador = True

        for plantao in range(sorteados.__len__() - 1):
            if sorteados[count] == sorteados[count + 1]:
                verificador = False
                print('Plantao bugado', sorteados[count].defensor)
                Sorteio.objects.all().delete()
            count += 1

        return verificador

    def sortear(self):

        dt_inicial = datetime.date(2019, 1, 7)
        dt_final = datetime.date(2019, 12, 19)
        feriados = Feriado.objects.all()

        # cria uma lista de dias úteis em um dado periodo
        workdays = rrule(DAILY, dtstart=dt_inicial, until=dt_final, byweekday=(MO, TU, WE, TH, FR))
        # cria uma lista de dias de fins de semana em um dado periodo
        weekends = rrule(DAILY, dtstart=dt_inicial, until=dt_final, byweekday=(SA, SU))
        recesso = rrule(DAILY, dtstart=datetime.date(2019, 12, 20), until=datetime.date(2020, 1, 6))

        # converte tipo RRULE para Date
        workdays = [dia.date() for dia in workdays]
        weekends = [dia.date() for dia in weekends]

        # remove feriados dos dias úteis e adiciona-os aos dias de fins de semana
        for feriado in feriados:
            if feriado.data in workdays:
                del workdays[workdays.index(feriado.data)]
            if feriado.data not in weekends:
                weekends.append(feriado.data)
        # ordena a lista de fins de semanas e feriados
        weekends = sorted(weekends)
        # laço para geração de sorteio para dias úteis da semana
        defensores = Defensor.objects.all().order_by('?')
        count = 0
        for day in workdays:

            while not Sorteio.objects.filter(data=day).first():

                defensor = defensores[count]

                if not defensor.afastamento_inicial <= day <= defensor.afastamento_final:
                    Sorteio.objects.create(data=day, defensor=defensor)
                else:
                    data_realocamento = self.get_next_day(workdays, day)
                    Sorteio.objects.create(data=data_realocamento, defensor=defensor)
                count = count + 1 if count < len(defensores) - 1 else 0

        # laço para geração de sorteio para dias de fim de semana
        defensores = Defensor.objects.all().order_by('?')
        count = 0
        for day in weekends:

            while not Sorteio.objects.filter(data=day).first():

                defensor = defensores[count]

                # se o defensor não estiver de ferias na data do laço o sorteio é realizado
                if not defensor.afastamento_inicial <= day <= defensor.afastamento_final:
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
