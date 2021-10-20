# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from sorteio.models import *

@admin.register(Comarca)
class ComarcaAdmin(admin.ModelAdmin):
    list_display = ['pk', 'cod_ibge', 'nome', 'total_defensores_vinculados']
    ordering = ['nome']
    search_fields = ['cod_ibge', 'nome']


@admin.register(Defensor)
class DefensorAdmin(admin.ModelAdmin):
    list_display = ['pk', 'comarca', 'nome', 'quantidade_atuacao', 'recesso']
    ordering = ['comarca']
    list_filter = ['recesso', 'comarca']
    search_fields = ['comarca__nome', 'nome']


@admin.register(Afastamento)
class AfastamentoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'data_inicial','data_final','defensor']
    ordering = ['defensor']
    list_filter = ['defensor']
    search_fields = ['defensor__nome', 'data_inicial', 'data_final']


@admin.register(Sorteio)
class SorteioAdmin(admin.ModelAdmin):
    list_display = ['data', 'nome_comarca', 'defensor']
    ordering = ['data', 'defensor']
    list_filter = ['defensor__comarca__nome']
    search_fields = ['defensor__nome', 'data', 'defensor__comarca__nome']


@admin.register(Feriado)
class FeriadoAdmin(admin.ModelAdmin):
    def habilitar_sorteio(modeladmin, request, queryset):
        queryset.update(incluir_sorteio=True)
    habilitar_sorteio.short_description = "Habilitar feriado no sorteio"

    list_display = ['pk', 'data', 'nome', 'incluir_sorteio']
    ordering = ['data']
    actions = [habilitar_sorteio]
    list_filter = ['incluir_sorteio']
    search_fields = ['data', 'nome']
