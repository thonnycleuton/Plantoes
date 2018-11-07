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
    recesso = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

    def quant_atuacao(self):
        return Sorteio.objects.filter(defensor=self).count()

    def populate(self):
        import csv
        with open('/home/thonnycleuton/PycharmProjects/Plantoes/sorteio/loads/defensores.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                comarca = Comarca.objects.get(nome=row['comarca'].lower())
                defensor = Defensor.objects.get_or_create(nome=row['nome'], setor=row['setor'], comarca=comarca, recesso=row['Recesso'])
                for i in range(4):
                    if row['Afastamento Inicial %s' % str(i + 1)]:
                        Afastamento.objects.get_or_create(data_inicial=row['Afastamento Inicial %s' % str(i + 1)],
                                                          data_final=row['Afastamento Final %s' % str(i + 1)],
                                                          defensor_id=defensor[0].id)


class Feriado(models.Model):
    data = models.DateField()
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=30)
    descricao = models.CharField(max_length=100)
    comarca = models.ForeignKey(Comarca)
    impedidos = models.CharField(max_length=300)

    def __str__(self):
        return self.nome + str(self.data)

    def populate(self):
        import urllib.request, json
        with urllib.request.urlopen(
                "https://api.calendario.com.br/?json=true&ano=2019&ibge=2211001&token=dGhvbm55Y2xldXRvbkBnbWFpbC5jb20maGFzaD05MzU5MzQx") as url:
            hollidays = json.loads(url.read().decode())
        for holliday in hollidays:
            comarca = Comarca.objects.get(cod_ibge=holliday['2211001'])
            Feriado.objects.create(data=holliday['date'], nome=holliday['name'], tipo=holliday['type'],
                                   descricao=holliday['description'], comarca=comarca)


class Sorteio(models.Model):
    data = models.DateField()
    defensor = models.ForeignKey(Defensor)

    def __str__(self):
        return str(self.data)


class Afastamento(models.Model):
    data_inicial = models.DateField()
    data_final = models.DateField()
    defensor = models.ForeignKey(Defensor)

    def __str__(self):
        return str(self.defensor)
