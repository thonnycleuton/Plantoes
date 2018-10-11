# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Comarca(models.Model):
    """
    Classe que modela a persistencia de comarcas'
    @:param nome: nome da Comarca ou normalmente a cidade
    """
    cod_ibge = models.CharField(max_length=8)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Defensor(models.Model):
    nome = models.CharField(max_length=100)
    comarca = models.ForeignKey(Comarca)
    setor = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Feriado(models.Model):
    data = models.DateField()
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=30)
    descricao = models.CharField(max_length=100)
    comarca = models.ForeignKey(Comarca)

    def __str__(self):
        return self.nome

