# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, FormView

from sorteio.forms import SorteioForm
from sorteio.models import *


class Home(ListView):
    model = Sorteio


class SorteioFormView(FormView):
    form_class = SorteioForm
    template_name = 'sorteio/sorteio_list.html'
    success_url = '/'

    def form_valid(self, form):

        form.sortear()
        while not form.verificar_inconsistencia():
            form.sortear()

        return super().form_valid(form)


class ComarcaList(ListView):
    model = Comarca


class DefensorList(ListView):
    model = Defensor


class FeriadoList(ListView):
    model = Feriado
