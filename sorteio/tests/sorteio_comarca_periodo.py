# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from unittest import TestCase
from dateutil.rrule import DAILY, rrule
from sorteio.forms import SorteioForm
from sorteio.models import Comarca


class SorteioRecessoTestCase(TestCase):
    form = SorteioForm()
    comarca_filter = Comarca.objects.filter(nome='oeiras')
    picos = comarca_filter[0]
    data_inicial=datetime.date(2021, 12, 20)
    data_final=datetime.date(2022, 1, 6)
    form.sortear_por_periodo_e_bloco(
        comarca=picos, 
        salvar_ao_finalizar=False, 
        data_inicial=data_inicial, 
        data_final=data_final,
    )

    def test_nenhum_dia_sem_defensor(self):
        sorteios = self.form.sorteios
        periodo = rrule(DAILY, dtstart=self.data_inicial, until=self.data_final)
        periodo = [dia.date() for dia in periodo]

        for sorteio in sorteios:
            print('data: {} = {}'.format(sorteio.data, sorteio.defensor))

        self.assertEqual(len(sorteios) == len(periodo), True, 'Todos os dias do período foram registrados')


