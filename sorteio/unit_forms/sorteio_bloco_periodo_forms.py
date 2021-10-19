# -*- coding: utf-8 -*-
import datetime
from dateutil.rrule import rrule, DAILY
from django import forms
from sorteio.models import Comarca, Defensor, Sorteio

class SorteioBlocoPeriodoForm(forms.Form):
    # dados do formulário
    options = []
    query = Comarca.objects.all()
    for comarca in query:
        if comarca.ha_mais_de_um_defensor:
            options.append(comarca)

    inicio = forms.DateField(
        required=True, 
        initial=datetime.date(2022, 12, 20),
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )
    fim = forms.DateField(
        required=True, 
        initial=datetime.date(2023, 1, 6),
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )
    comarca = forms.ChoiceField(
        choices=[(query.pk, query.nome) for query in options],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Dados para os sorteio
    recesso_inicial = datetime.date(2022, 12, 20)
    recesso_final = datetime.date(2023, 1, 5)
    sorteios = [] # Os sorteios serão registrados na memória ram ao invés do disco rígido
    defensores = []

    def buscar_deferensores_do_banco_de_dados(self, comarca):
        self.defensores = Defensor.objects.filter(comarca=comarca).order_by('?')

    def sem_defensores(self):
        return len(self.defensores) == 0

    def sortear_por_periodo_e_bloco(self, comarca, data_inicial=None, data_final=None, salvar_ao_finalizar=False):
        self.sorteios.clear()
        self.buscar_deferensores_do_banco_de_dados(comarca)
        if self.sem_defensores():
            return
        data_inicial = data_inicial if data_inicial != None else self.recesso_inicial
        data_final = data_final if data_final != None else datetime.date(2022, 1, 6)
        
        periodo = rrule(DAILY, dtstart=data_inicial, until=data_final)
        periodo = [dia.date() for dia in periodo]
        quantidade_de_dias_cada = len(periodo) // len(self.defensores)
        resto = len(periodo) % len(self.defensores)
        
        indice_do_dia = 0
        indice_defensor = 0
        while indice_do_dia < len(periodo):
            if indice_defensor % 2 == 0 and resto > 0:
                for _ in range(quantidade_de_dias_cada + 1):
                    self.sorteios.append(Sorteio(data=periodo[indice_do_dia], defensor=self.defensores[indice_defensor]))
                    indice_do_dia += 1
            else:
                for _ in range(quantidade_de_dias_cada):
                    self.sorteios.append(Sorteio(data=periodo[indice_do_dia], defensor=self.defensores[indice_defensor]))
                    indice_do_dia += 1
            indice_defensor += 1
            
        if salvar_ao_finalizar:
            self.salvar_sorteio()
            

    def salvar_sorteio(self):
        Sorteio.objects.filter(defensor__in=self.defensores).delete()
        for sorteio in self.sorteios:
            sorteio.save()