# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DetailView, CreateView

from sorteio.forms import SorteioForm, AfastamentoForm
from sorteio.models import *


class Home(ListView):
    model = Sorteio
    ordering = 'data'
    template_name = 'sorteio/app/tables_dynamic.html'


class SorteioFormView(FormView):
    form_class = SorteioForm
    template_name = 'sorteio/sorteio_list.html'
    success_url = '/'

    def form_valid(self, form):
        form.sortear()
        form.verificar_inconsistencia()

        return super().form_valid(form)


class ComarcaList(ListView):
    model = Comarca


class DefensorList(ListView):
    model = Defensor


class DefensorDetail(DetailView):
    model = Defensor


class FeriadoList(ListView):
    model = Feriado


class AfastamentoFormView(FormView):

    form_class = AfastamentoForm
    context_object_name = 'afastamentos'
    template_name = 'sorteio/afastamento_form.html'
    success_url = reverse_lazy('sorteio:defensore_list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
