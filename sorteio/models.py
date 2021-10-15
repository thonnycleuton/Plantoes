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

    @property
    def ha_mais_de_um_defensor(self):
        return len(self.defensores.all()) > 1

    def minimo_de_defensores(self, valor):
        return len(self.defensores.all()) >= valor

    def __str__(self):
        return self.nome

    def populate(self):
        import csv
        with open('/home/pedrohenrique/Github/Plantoes/sorteio/loads/DTB_BRASIL_MUNICIPIO.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Comarca.objects.get_or_create(nome=row['Nome_Município'], cod_ibge=row['Código Município Completo'])


class Defensor(models.Model):
    nome = models.CharField(max_length=100)
    comarca = models.ForeignKey(Comarca, related_name='defensores')
    setor = models.CharField(max_length=20)
    recesso = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

    def quant_atuacao(self):
        return Sorteio.objects.filter(defensor=self).count()

    @staticmethod
    def populate():
        import csv
        with open('/home/thonnycleuton/PycharmProjects/Plantoes/sorteio/loads/Afastamentos.csv') as csvfile:
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
    # tipo = models.CharField(max_length=30)
    # descricao = models.CharField(max_length=100)
    # comarca = models.ForeignKey(Comarca)
    impedidos = models.CharField(max_length=300)

    def __str__(self):
        return self.nome + " - " + str(self.data)

    @staticmethod
    def populate():
        Feriado.objects.all().delete()
        import urllib.request, json
        with urllib.request.urlopen(
                "https://api.calendario.com.br/?json=true&ano=2022&ibge=2211001&token=dGhvbm55Y2xldXRvbkBnbWFpbC5jb20maGFzaD05MzU5MzQx") as url:
            hollidays = json.loads(url.read().decode())

        for holliday in hollidays:
            # comarca = Comarca.objects.get(pk=440)
            data_split = holliday['date'].split('/')
            data = '{}-{}-{}'.format(data_split[2], data_split[1], data_split[0])
            Feriado.objects.create(
                data=data,
                nome=holliday['name'],
                # tipo=holliday['type'], 
                # descricao=holliday['description'], 
                # comarca=comarca
            )


class Sorteio(models.Model):
    data = models.DateField()
    defensor = models.ForeignKey(Defensor)

    def __str__(self):
        return str(self.data)


class Afastamento(models.Model):

    data_inicial = models.DateField()
    data_final = models.DateField()
    defensor = models.ForeignKey(Defensor, related_name='afastamentos')

    def quant_afastamentos(self):

        return len(self.defensor.afastamentos.all())

    def __str__(self):
        return str(self.data_inicial) + ' a ' + str(self.data_final)
