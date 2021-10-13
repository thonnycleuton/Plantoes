import datetime

from dateutil.rrule import rrule, DAILY, MO, TU, WE, TH, FR, SA, SU
from django import forms
from sorteio.models import Defensor, Sorteio, Feriado, Afastamento


class SorteioForm(forms.Form):
    dt_inicial = datetime.date(2021, 1, 6)
    dt_final = datetime.date(2021, 12, 19)
    recesso_inicial = datetime.date(2021, 12, 20)
    recesso_final = datetime.date(2022, 1, 5)
    feriados = Feriado.objects.all()

    # cria uma lista de dias úteis em um dado periodo
    workdays = rrule(DAILY, dtstart=dt_inicial, until=dt_final, byweekday=(MO, TU, WE, TH, FR))
    weekends = rrule(DAILY, dtstart=dt_inicial, until=dt_final, byweekday=(SA, SU))
    recesso = rrule(DAILY, dtstart=recesso_inicial, until=recesso_final)
    todos_os_dias = rrule(DAILY, dtstart=dt_inicial, until=recesso_final, byweekday=(MO, TU, WE, TH, FR, SA, SU))

    sorteios = [] # Os sorteios serão registrados na memória ram ao invés do disco rígido

    def diferenca_de_dias_e_valida(self):
        defensores = Defensor.objects.all()
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

    def sortear(self, salvar_ao_finalizar=False):
        # Limpa os dados do último sorteio antes de iniciar a nova geração
        self.sorteios.clear()
        # converte tipo RRULE para Date
        recesso = [dia.date() for dia in self.recesso]
        todos_os_dias = [dia.date() for dia in self.todos_os_dias]
        todos_os_dias = sorted(todos_os_dias)

        # variaveis de controle para a geracao do sorteio
        defensores = Defensor.objects.all().order_by('?')
        nao_alocados = []
        indice_do_dia = 0
        indice_do_defensor = 0
        ultimo_defensor_selecionado = None

        while indice_do_dia < len(todos_os_dias):
            dia = todos_os_dias[indice_do_dia]

            # Seleciona o defensor se o não houver ninguem pendente de alocacao
            if ultimo_defensor_selecionado == None:
                defensor = defensores[indice_do_defensor]
                indice_do_defensor += 1
            else:
                # Verifica se há alguém pendente de alocacao
                if len(nao_alocados) > 0:
                    # Verifica se a pessoa pendente de alocacao é diferente da ultima iteracao
                    if nao_alocados[0] != ultimo_defensor_selecionado:
                        defensor = nao_alocados[0]
                        del nao_alocados[0]
                    else:
                        # Verica se o atual defensor é o mesmo da ultima iteracao
                        if defensores[indice_do_defensor] != ultimo_defensor_selecionado:
                            defensor = defensores[indice_do_defensor]
                            indice_do_defensor += 1
                        else:
                            nao_alocados.append(defensores[indice_do_defensor])
                            indice_do_defensor += 1
                else:
                    # Verica se o atual defensor é o mesmo da ultima iteracao
                    if defensores[indice_do_defensor] != ultimo_defensor_selecionado:
                        defensor = defensores[indice_do_defensor]
                        indice_do_defensor += 1
                    else:
                        nao_alocados.append(defensores[indice_do_defensor])
                        indice_do_defensor += 1

            # Impede que um defensor com direito a recesso seja alocado em um dia de recesso
            # Caso seja verdade o loop é interrompido e um novo defensor é selecionado para a data
            if dia in recesso and defensor.recesso:
                continue

            # Informa o último defensor
            afastamentos = defensor.afastamentos.all()
            ultimo_defensor_selecionado = defensor

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

            # A lista de defensores foi percorrida e precisa ser reiniciada
            if indice_do_defensor >= len(defensores):
                defensores = Defensor.objects.all().order_by('?')
                indice_do_defensor = 0
        
        # verifica a inconsistencia do sorteio para poder salvar os dados
        while not self.verificar_inconsistencia() or not self.diferenca_de_dias_e_valida():
            self.sortear()

        if salvar_ao_finalizar:
            self.salvar_sorteio()
    
    def salvar_sorteio(self):
        Sorteio.objects.all().delete()
        for sorteio in self.sorteios:
            sorteio.save()


class AfastamentoForm(forms.ModelForm):

    class Meta:
        model = Afastamento
        fields = '__all__'
        widgets = {
            'data_inicial': forms.DateInput(attrs={"class": "form-control", "data-inputmask": "'mask': '99/99/9999'"}),
            'data_final': forms.DateInput(attrs={"class": "form-control", "data-inputmask": "'mask': '99/99/9999'"}),
            'defensor': forms.Select(attrs={'class': 'form-control'}),
        }


class FeriadoForm(forms.ModelForm):

    class Meta:
        model = Feriado
        exclude = ('impedidos', )
        widgets = {
            'data': forms.DateInput(attrs={"class": "form-control", "data-inputmask": "'mask': '99/99/9999'"}),
        }

class DefensorForm(forms.ModelForm):

    class Meta:
        model = Defensor
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={"class": "form-control"}),
            'comarca': forms.Select(attrs={"class": "form-control"}),
            'setor': forms.TextInput(attrs={"class": "form-control"}),
            'recesso': forms.CheckboxInput(attrs={"class": "form-control"})
        }

