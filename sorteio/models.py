# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

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

    def populate(self):
        import csv
        with open('/home/thonnycleuton/PycharmProjects/Plantoes/sorteio/loads/DTB_BRASIL_MUNICIPIO.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Comarca.objects.get_or_create(nome=row['Nome_Município'], cod_ibge=row['Código Município Completo'])


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


class Sorteio(models.Model):

    data = models.DateField()
    defensor = models.ForeignKey(Defensor)

    def __str__(self):
        return str(self.data)

    def daterange(self, start_date, end_date):

        datas = []

        for n in range(int((end_date - start_date).days)):
            datas.append(datetime.timedelta(n))

        return datas

    def sortear(self):

        defensores = Defensor.objects.all()
        dt_inicial = datetime.date(2019, 1, 7)
        dt_final = datetime.date(2020, 1, 6)

        datas = self.daterange(dt_inicial, dt_final)

        for data in datas:
            self.objects.create(data=data, defensor=defensores.get(pk=datas.index(data)))

        return self.objects.all()
