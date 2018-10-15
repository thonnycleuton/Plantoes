# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from sorteio.models import *


class Home(ListView):
    model = Sorteio


class ComarcaList(ListView):
    model = Comarca


class DefensorList(ListView):
    model = Defensor


class FeriadoList(ListView):
    model = Feriado
