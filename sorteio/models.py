# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Comarca(models.Model):
    """
    Classe que modela a persistencia de comarcas
    @:param nome: nome da Comarca ou normalmente a cidade
    """
    nome = models.CharField(max_length=100)


class Defensor(models.Model):
    nome = models.CharField(max_length=100)
    comarca = models.ForeignKey(Comarca)


class Feriado(models.Model):
    data = models.DateField()
    nome = models.CharField(max_length=100)
    comarca = models.ForeignKey(Comarca)
