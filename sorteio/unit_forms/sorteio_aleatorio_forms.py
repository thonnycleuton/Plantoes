# -*- coding: utf-8 -*-
import datetime
from dateutil.rrule import rrule, DAILY, MO, TU, WE, TH, FR, SA, SU
from django import forms
from sorteio.models import Comarca, Defensor, Sorteio, Feriado, Afastamento

class SorteioForm(forms.Form):
    # dados do formulário
    options = []
    query = Comarca.objects.all()
    for comarca in query:
        if comarca.minimo_de_defensores(20):
            options.append(comarca)

    comarca = forms.ChoiceField(
        choices=[(query.pk, query.nome) for query in options], 
        widget=forms.Select(attrs={'class': 'form-control'}))

    # Dados para os sorteio
    dt_inicial = datetime.date(2022, 1, 6)
    dt_final = datetime.date(2022, 12, 19)
    recesso_inicial = datetime.date(2022, 12, 20)
    recesso_final = datetime.date(2023, 1, 5)
    feriados = Feriado.objects.all()

    workdays = rrule(DAILY, dtstart=dt_inicial, until=dt_final, byweekday=(MO, TU, WE, TH, FR))
    weekends = rrule(DAILY, dtstart=dt_inicial, until=dt_final, byweekday=(SA, SU))
    recesso = rrule(DAILY, dtstart=recesso_inicial, until=recesso_final)
    todos_os_dias = rrule(DAILY, dtstart=dt_inicial, until=recesso_final, byweekday=(MO, TU, WE, TH, FR, SA, SU))

    sorteios = [] # Os sorteios serão registrados na memória ram ao invés do disco rígido
    nao_alocados = []
    indice_do_defensor = 0
    ultimo_defensor_selecionado = None
    defensores = []

    # Verifica quem possui mais ou menos dias ], a diferenca deve ser menor ou igual a 3
    def diferenca_de_dias_valida(self):
        defensores = self.defensores
        contagem_defensores = []

        # Verifica a quantidade de dias dos defensores sorteados
        for defensor in defensores:
            contagem = 0
            for sorteio in self.sorteios:
                if sorteio.defensor == defensor:
                    contagem += 1
            contagem_defensores.append(contagem)
        
        # Verifica o número minimo e maximo de dias
        min = contagem_defensores[0]
        max = contagem_defensores[0]
        for contagem in contagem_defensores:
            if contagem < min:
                min = contagem
            if contagem > max:
                max = contagem

        diferenca = max - min
        if diferenca > 3:
            return False
        return True


    def verificar_inconsistencia(self):
        sorteados = sorted(self.sorteios, key=lambda x: x.data)
        recesso = [dia.date() for dia in self.recesso]
        verificador = True

        for posicao in range(sorteados.__len__() - 1):
            if sorteados[posicao].defensor == sorteados[posicao + 1].defensor:
                verificador = False
                break
            elif sorteados[0].defensor == sorteados[-1].defensor:
                verificador = False
                break
            elif sorteados[-1].data in recesso and sorteados[-1].defensor.recesso:
                verificador = False
                break
        if not verificador:
            print('Realocando Duplicidade')
        return verificador

    # Seleciona o defensor se o não houver ninguem pendente de alocacao
    def selecionar_defensor(self):
        if self.ultimo_defensor_selecionado == None:
            defensor = self.defensores[self.indice_do_defensor]
            self.indice_do_defensor += 1
            return defensor
        else:
            # Verifica se há alguém pendente de alocacao
            if len(self.nao_alocados) > 0:
                # Verifica se a pessoa pendente de alocacao é diferente da ultima iteracao
                if self.nao_alocados[0] != self.ultimo_defensor_selecionado:
                    defensor = self.nao_alocados[0]
                    del self.nao_alocados[0]
                    return defensor
                else:
                    # Verifica se o atual defensor é o mesmo da ultima iteracao
                    if self.defensores[self.indice_do_defensor] != self.ultimo_defensor_selecionado:
                        defensor = self.defensores[self.indice_do_defensor]
                        self.indice_do_defensor += 1
                        return defensor
                    else:
                        self.nao_alocados.append(self.defensores[self.indice_do_defensor])
                        self.indice_do_defensor += 1
            else:
                # Verica se o atual defensor é o mesmo da ultima iteracao
                if self.defensores[self.indice_do_defensor] != self.ultimo_defensor_selecionado:
                    defensor = self.defensores[self.indice_do_defensor]
                    self.indice_do_defensor += 1
                    return defensor
                else:
                    self.nao_alocados.append(self.defensores[self.indice_do_defensor])
                    self.indice_do_defensor += 1

    def limpar_dados(self):
        # Limpa os dados do último sorteio antes de iniciar o novo sorteio
        self.sorteios.clear()
        self.nao_alocados.clear()
        self.indice_do_defensor = 0
        self.ultimo_defensor_selecionado = None

    def buscar_deferensores_do_banco_de_dados(self, comarca):
        self.defensores = Defensor.objects.filter(comarca=comarca).order_by('?')

    def sem_defensores(self):
        return len(self.defensores) == 0

    def sortear(self, comarca, salvar_ao_finalizar=False):
        self.limpar_dados()
        self.buscar_deferensores_do_banco_de_dados(comarca)
        if self.sem_defensores():
            return

        # converte tipo RRULE para Date
        recesso = [dia.date() for dia in self.recesso]
        todos_os_dias = sorted([dia.date() for dia in self.todos_os_dias])

        # variaveis de controle para a geracao do sorteio
        indice_do_dia = 0
        while indice_do_dia < len(todos_os_dias):
            # A lista de defensores foi percorrida e precisa ser reiniciada
            if self.indice_do_defensor >= len(self.defensores):
                self.buscar_deferensores_do_banco_de_dados(comarca)
                self.indice_do_defensor = 0

            dia = todos_os_dias[indice_do_dia]
            defensor = self.selecionar_defensor()

            # Impede que um defensor com direito a recesso seja alocado em um dia de recesso
            if defensor == None or dia in recesso and defensor.recesso:
                continue

            # Informa o último defensor
            afastamentos = defensor.afastamentos.all()
            self.ultimo_defensor_selecionado = defensor

            # Tratamento dos afastamentos, impede que um defensor afastado seja alocado em uma data de afastamento
            if afastamentos.__len__() > 0:
                impedimento = False
                for afastamento in afastamentos:
                    if afastamento.data_inicial <= dia <= afastamento.data_final:
                        impedimento = True
                        break
                if not impedimento:
                    self.sorteios.append(Sorteio(data=dia, defensor=defensor))
                    indice_do_dia += 1
            else:
                self.sorteios.append(Sorteio(data=dia, defensor=defensor))
                indice_do_dia += 1
        
        # verifica a inconsistencia do sorteio para poder salvar os dados
        while not self.verificar_inconsistencia() or not self.diferenca_de_dias_valida():
            self.sortear(comarca=comarca, salvar_ao_finalizar=salvar_ao_finalizar)

        if salvar_ao_finalizar:
            self.salvar_sorteio()

    def salvar_sorteio(self):
        Sorteio.objects.filter(defensor__in=self.defensores).delete()
        for sorteio in self.sorteios:
            sorteio.save()