# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DetailView, CreateView
from django.views.generic.base import View
from django.views.generic.edit import DeleteView, UpdateView

from sorteio.forms import *
from sorteio.models import *


class Home(ListView):
    model = Sorteio
    ordering = 'data'
    template_name = 'sorteio/app/tables_dynamic.html'


class SorteioFormView(LoginRequiredMixin, FormView):
    login_url = '/usuario/entrar'
    redirect_field_name = 'redirect_to'
    form_class = SorteioForm
    template_name = 'sorteio/sorteio_list.html'
    success_url = '/'

    def form_valid(self, form):
        id_selecionado = int(form.cleaned_data['comarca'])
        comarca = Comarca.objects.filter(id=id_selecionado)
        form.sortear(comarca=comarca[0], salvar_ao_finalizar=True)
        return super().form_valid(form)


class SorteioBlocoPeriodoFormView(LoginRequiredMixin, FormView):
    login_url = '/usuario/entrar'
    redirect_field_name = 'redirect_to'
    form_class = SorteioBlocoPeriodoForm
    template_name = 'sorteio/sorteio_bloco_periodo.html'
    success_url = '/'
    
    def form_valid(self, form):
        id_selecionado = int(form.cleaned_data['comarca'])
        inicio = form.cleaned_data['inicio']
        fim = form.cleaned_data['fim']
        comarca = Comarca.objects.filter(id=id_selecionado)
        form.sortear_por_periodo_e_bloco(comarca=comarca[0], data_inicial=inicio, data_final=fim, salvar_ao_finalizar=True)
        return super().form_valid(form)


class ComarcaList(ListView):
    model = Comarca


class DefensorList(ListView):
    model = Defensor


class DefensorDetail(View):

    def get(self, request, pk):
        pk = int(pk)
        defensores = Defensor.objects.filter(pk=pk)
        if len(defensores) > 0:
            return render(request, 'sorteio/defensor_detail.html', {'defensor': defensores[0]})
        else:
            return redirect('/defensores')


class DefensorCreate(LoginRequiredMixin, FormView):
    login_url = '/usuario/entrar'
    redirect_field_name = 'redirect_to'
    form_class = DefensorForm
    model = Defensor
    template_name = 'sorteio/defensor_form.html'
    success_url = reverse_lazy('sorteio:defensore_list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class DefensorEdit(LoginRequiredMixin, UpdateView):
    login_url = '/usuario/entrar'
    redirect_field_name = 'redirect_to'
    form_class = DefensorForm
    model = Defensor
    template_name = 'sorteio/defensor_form.html'
    success_url = reverse_lazy('sorteio:defensore_list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class DefensorDelete(LoginRequiredMixin, DeleteView):
    login_url = '/usuario/entrar'
    redirect_field_name = 'redirect_to'
    model = Defensor
    success_url = reverse_lazy('sorteio:defensore_list')


class FeriadoDetail(DetailView):
    model = Feriado


class FeriadoList(ListView):
    model = Feriado
    ordering = ['pk']


class FeriadoFormView(LoginRequiredMixin, FormView):
    login_url = '/usuario/entrar'
    redirect_field_name = 'redirect_to'
    form_class = FeriadoForm
    context_object_name = 'feriados'
    template_name = 'sorteio/feriado_form.html'
    success_url = reverse_lazy('sorteio:feriado_list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AfastamentoListView(ListView):
    model = Afastamento


class AfastamentoFormView(LoginRequiredMixin, FormView):
    login_url = '/usuario/entrar'
    redirect_field_name = 'redirect_to'
    form_class = AfastamentoForm
    context_object_name = 'afastamentos'
    template_name = 'sorteio/afastamento_form.html'
    success_url = reverse_lazy('sorteio:defensore_list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AfastamentoDeleteView(LoginRequiredMixin, View):
    login_url = '/usuario/entrar'
    redirect_field_name = 'redirect_to'

    def get(self, request, pk):
        pk = int(pk)
        afastamentos = Afastamento.objects.filter(pk=pk)
        if len(afastamentos) > 0:
            defensor = afastamentos[0].defensor
            afastamentos[0].delete()
            return redirect('/defensor/detalhes/{}'.format(defensor.id))
        return redirect('/defensores')
