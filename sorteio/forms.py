# -*- coding: utf-8 -*-
import datetime
from dateutil.rrule import rrule, DAILY, MO, TU, WE, TH, FR, SA, SU
from django import forms
from sorteio.models import Comarca, Defensor, Sorteio, Feriado, Afastamento


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
        fields = ('data', 'nome', 'incluir_sorteio')
        widgets = {
            'data': forms.DateInput(attrs={"class": "form-control", "data-inputmask": "'mask': '99/99/9999'"}),
            'nome': forms.TextInput(attrs={"class": "form-control"}),
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

