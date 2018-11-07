import datetime

from dateutil.rrule import rrule, DAILY, MO, TU, WE, TH, FR, SA, SU
from django.forms import forms
from sorteio.models import Defensor, Sorteio, Feriado, Afastamento


class SorteioForm(forms.Form):

    def verificar_inconsistencia(self):

        sorteados = Sorteio.objects.all().order_by('data')
        count = 0
        verificador = True

        for plantao in range(sorteados.__len__() - 1):
            if sorteados[count].defensor == sorteados[count + 1].defensor:
                verificador = False
                print('Inconsistencias', sorteados[count].defensor)
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
        # lista de feriadoes especiais que geram impedimentos
        feriadao = []
        for dia_feriado in feriados:
            if 'Carnaval' in dia_feriado.nome or 'Sexta-Feira Santa' in dia_feriado.nome or 'Corpus Christi' in dia_feriado.nome:
                feriadao.append(dia_feriado)

        # converte tipo RRULE para Date
        workdays = [dia.date() for dia in workdays]
        weekends = [dia.date() for dia in weekends]
        recesso = [dia.date() for dia in recesso]

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
                afastamentos = Afastamento.objects.filter(defensor_id=defensor.id)

                if afastamentos:

                    for afastamento in afastamentos:

                        if not afastamento.data_inicial <= day <= afastamento.data_final:
                            if not Sorteio.objects.filter(data=day).first():
                                Sorteio.objects.create(data=day, defensor=defensor)
                                Afastamento.objects.create(defensor=defensor, data_inicial=day, data_final=day + datetime.timedelta(days=1))
                        else:
                            data_realocamento = self.get_next_day(workdays, afastamento.data_final)
                            try:
                                Sorteio.objects.create(data=data_realocamento, defensor=defensor)
                                Afastamento.objects.create(defensor=defensor, data_inicial=day, data_final=day + datetime.timedelta(days=1))
                            except Exception as e:
                                print(e, day, afastamento.data_final)
                else:
                    Sorteio.objects.create(data=day, defensor=defensor)
                    Afastamento.objects.create(defensor=defensor, data_inicial=day, data_final=day + datetime.timedelta(days=1))

                count = count + 1 if count < len(defensores) - 1 else 0

        # laço para geração de sorteio para dias de fim de semana
        defensores = Defensor.objects.all().order_by('?')
        count = 0
        for day in weekends:

            while not Sorteio.objects.filter(data=day).first():

                defensor = defensores[count]

                afastamentos = Afastamento.objects.filter(defensor_id=defensor.id)

                if afastamentos:

                    for afastamento in afastamentos:

                        if not afastamento.data_inicial <= day <= afastamento.data_final:
                            if not Sorteio.objects.filter(data=day).first():
                                Sorteio.objects.create(data=day, defensor=defensor)
                                Afastamento.objects.create(defensor=defensor, data_inicial=day, data_final=day + datetime.timedelta(days=1))
                        else:
                            data_realocamento = self.get_next_day(weekends, afastamento.data_final)
                            try:
                                Sorteio.objects.create(data=data_realocamento, defensor=defensor)
                                Afastamento.objects.create(defensor=defensor, data_inicial=day, data_final=day + datetime.timedelta(days=1))
                            except Exception as e:
                                print(e, day, afastamento.data_final)
                else:
                    Sorteio.objects.create(data=day, defensor=defensor)
                    Afastamento.objects.create(defensor=defensor, data_inicial=day, data_final=day + datetime.timedelta(days=1))

                count = count + 1 if count < len(defensores) - 1 else 0

        # laço para geração de sorteio para dias de recesso de fim de ano
        defensores = Defensor.objects.exclude(recesso=True).order_by('?')
        count = 0
        for day in recesso:

            while not Sorteio.objects.filter(data=day).first():

                defensor = defensores[count]
                afastamentos = Afastamento.objects.filter(defensor_id=defensor.id)

                if afastamentos:

                    for afastamento in afastamentos:

                        if not afastamento.data_inicial <= day <= afastamento.data_final:
                            if not Sorteio.objects.filter(data=day).first():
                                Sorteio.objects.create(data=day, defensor=defensor)
                        else:
                            data_realocamento = self.get_next_day(recesso, afastamento.data_final)
                            try:
                                Sorteio.objects.create(data=data_realocamento, defensor=defensor)
                            except Exception as e:
                                print(e, day, afastamento.data_final)
                else:
                    Sorteio.objects.create(data=day, defensor=defensor)
                    Afastamento.objects.create(defensor=defensor, data_inicial=day, data_final=day + datetime.timedelta(days=1))
                count = count + 1 if count < len(defensores) - 1 else 0

    # Pega o proximo dia disponivel em uma dada lista
    @staticmethod
    def get_next_day(lista, dia):
        """Metodo para buscar a próxima data disponível em uma dada lista"""
        #TODO: Remover bug neste metodo. Provavelmente ocasionado pela mudanca do tipo de lista
        for l in lista:
            if l >= dia + datetime.timedelta(days=1):
                if not Sorteio.objects.filter(data=l).first():
                    return l
