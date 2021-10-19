# -*- coding: utf-8 -*-
import datetime
from dateutil.rrule import rrule, DAILY, SA, SU
from django import forms
from sorteio.models import Comarca, Defensor, Sorteio, Feriado

class SorteioParnaibaForm(forms.Form):
    # dados do formulário
    defensores = []
    try:
        parnaiba = Comarca.objects.get(nome='parnaíba')
        query = Defensor.objects.filter(comarca=parnaiba)
        for defensor in query:
            defensores.append(defensor)
    except:
        pass

    selecionados_recesso = forms.MultipleChoiceField(
        choices=[(query.pk, query.nome) for query in defensores],
        widget=forms.SelectMultiple(attrs={'class': 'select2_multiple form-control', 'multiple': 'multiple'})
    )

    # Dados para os sorteio
    dt_inicial = datetime.date(2022, 1, 7)
    dt_final = datetime.date(2022, 12, 20)
    recesso_inicial = datetime.date(2022, 12, 20)
    recesso_final = datetime.date(2023, 1, 6)
    
    weekends = rrule(DAILY, dtstart=dt_inicial, until=dt_final, byweekday=(SA, SU))
    recesso = rrule(DAILY, dtstart=recesso_inicial, until=recesso_final)
    feriados = [feriado.data for feriado in Feriado.objects.filter(incluir_sorteio=True)]

    recesso_inicial = datetime.date(2022, 12, 20)
    recesso_final = datetime.date(2023, 1, 6)
    
    sorteios_custodias = []
    sorteios_recesso = []
    defensores = []

    def sortear(self, selecionados):
        self.sorteios_custodias.clear()
        self.sorteios_recesso.clear()
        self.sortear_audiencias_de_custodias()
        self.sortear_recesso(selecionados)
        all = self.sorteios_custodias
        all.extend(self.sorteios_recesso)
        return all

    def sortear_audiencias_de_custodias(self):
        self.buscar_deferensores_de_parnaiba()
        # Finaliza o sorteio se nenhum defensor estiver sido selecionado
        if self.sem_defensores():
            return

        # Seleciona todos os finais de semana e adiciona os feriados de forma ordenada
        dias = self.selecionar_finais_de_semana_com_feriados()
        # Transforma todos os finais de semana em blocos de finais de semana e feriado
        blocos = self.criar_blocos_de_finais_de_semana_com_feriados(dias)
        # Sorteia os blocos para os defensores vinculados a comarca de parnaiba
        self.sortear_blocos_para_defensores(blocos)

    def sortear_recesso(self, selecionados):
        self.sorteios_recesso.clear()
        self.buscar_deferensores_do_banco_de_dados(selecionados)
        # Finaliza o sorteio se nenhum defensor estiver sido selecionado
        if self.sem_defensores():
            return
        
        data_inicial = self.recesso_inicial
        data_final = datetime.date(2023, 1, 6)
        
        periodo = rrule(DAILY, dtstart=data_inicial, until=data_final)
        periodo = [dia.date() for dia in periodo]
        quantidade_de_dias_cada = len(periodo) // len(self.defensores)
        resto = len(periodo) % len(self.defensores)
        
        indice_do_dia = 0
        indice_defensor = 0
        while indice_do_dia < len(periodo):
            if indice_defensor % 2 == 0 and resto > 0:
                for _ in range(quantidade_de_dias_cada + 1):
                    self.sorteios_recesso.append(Sorteio(data=periodo[indice_do_dia], defensor=self.defensores[indice_defensor]))
                    indice_do_dia += 1
            else:
                for _ in range(quantidade_de_dias_cada):
                    self.sorteios_recesso.append(Sorteio(data=periodo[indice_do_dia], defensor=self.defensores[indice_defensor]))
                    indice_do_dia += 1
            indice_defensor += 1

    def buscar_deferensores_do_banco_de_dados(self, selecionados):
        self.defensores = Defensor.objects.filter(id__in=selecionados).order_by('?')

    def buscar_deferensores_de_parnaiba(self):
        try:
            parnaiba = Comarca.objects.get(nome='parnaíba')
            self.defensores = Defensor.objects.filter(comarca=parnaiba).order_by('?')
        except:
            return

    def sem_defensores(self):
        return len(self.defensores) == 0

    def selecionar_finais_de_semana_com_feriados(self):
        todos_os_finais_de_semana = sorted([dia.date() for dia in self.weekends])
        todos_os_finais_de_semana.extend(self.feriados)
        todos_os_finais_de_semana.sort()
        todos_os_finais_de_semana = self.remover_dias_repetidos(todos_os_finais_de_semana)
        return todos_os_finais_de_semana

    def remover_dias_repetidos(self, datas):
        resultado = []
        for data in datas:
            if data not in resultado:
                resultado.append(data)
        return resultado

    def criar_blocos_de_finais_de_semana_com_feriados(self, dias):
        index = 0
        blocos_para_sorteio = []

        while True:
            bloco_auxiliar = []
            while True:
                if index == len(dias) - 1:
                    bloco_auxiliar.append(data_posterior)
                    blocos_para_sorteio.append(bloco_auxiliar.copy())
                    break

                # Prepara os dados para a verificação
                um_dia = datetime.timedelta(days=1)
                data_atual = dias[index]
                data_posterior = dias[index + 1]

                # Incremente a data atual em 1 apos preparar os dados
                index += 1

                # Verifica se a data seguinte é equivalente a data atual mais um dia
                if (data_atual + um_dia) == data_posterior:
                    bloco_auxiliar.append(data_atual)
                else:
                    bloco_auxiliar.append(data_atual)
                    break

            # Quebra feriados longos em feriados menores
            if len(bloco_auxiliar) > 3:
                blocos_para_sorteio.append(bloco_auxiliar[0:2].copy())
                blocos_para_sorteio.append(bloco_auxiliar[2:].copy())
            else:
                blocos_para_sorteio.append(bloco_auxiliar.copy())
                
            # Verifica se a lista de datas chegou ao fim
            if index == len(dias) - 1:
                break
        
        return blocos_para_sorteio

    def sortear_blocos_para_defensores(self, blocos):
        contador_blocos_atribuidos = 0
        while contador_blocos_atribuidos < len(blocos):
            for defensor in self.defensores:
                if contador_blocos_atribuidos == len(blocos):
                    break
                for data in blocos[contador_blocos_atribuidos]:
                    self.sorteios_custodias.append(Sorteio(data=data, defensor=defensor))
                contador_blocos_atribuidos += 1
            self.buscar_deferensores_de_parnaiba()
