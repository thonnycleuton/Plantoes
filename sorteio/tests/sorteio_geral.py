# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from unittest import TestCase
from sorteio.forms import SorteioForm
from sorteio.models import Comarca


class SorteioFormTestCase(TestCase):
    form = SorteioForm()
    comarca_filter = Comarca.objects.filter(nome='teresina')
    teresina = comarca_filter[0]
    form.sortear(comarca=teresina, salvar_ao_finalizar=False)

    def test_defesor_de_recesso_nao_alocados_no_recesso(self):
        sorteios = self.form.sorteios
        recesso = [dia.date() for dia in self.form.recesso]
        dados_validos = True

        for sorteio in sorteios:
            if sorteio.data in recesso and sorteio.defensor.recesso:
                dados_validos = False
        
        self.assertEqual(dados_validos, True, 'Nenhum defensor de recesso foi alocado no recesso estabelecido no ano')

    def test_nao_ha_duplicidade_na_virada_do_ano(self):
        sorteios = self.form.sorteios
        self.assertEqual(sorteios[0].defensor != sorteios[-1].defensor, True, 'O defensor que irá trabalhar no final do ano não irá trabalhar no dia primeiro')

    def test_nao_ha_duplicidade(self):
        sorteios = self.form.sorteios
        dados_validos = True

        for indice in range(len(sorteios) - 1):
            if sorteios[indice].defensor == sorteios[indice + 1].defensor:
                dados_validos = False
                break

        self.assertEqual(dados_validos, True, 'Nao ha duplicidade entre os dias do sorteio')

    def test_diferenca_entre_os_sorteios_menor_igual_a_tres(self):
        sorteios = self.form.sorteios
        defensores = []
        contagem_defensores = []

        for sorteio in sorteios:
            if sorteio.defensor not in defensores:
                defensores.append(sorteio.defensor)

        for defensor in defensores:
            contagem = 0
            for sorteio in sorteios:
                if sorteio.defensor == defensor:
                    contagem += 1
            contagem_defensores.append(contagem)
        
        min = contagem_defensores[0]
        max = contagem_defensores[0]
        for contagem in contagem_defensores:
            if contagem < min:
                min = contagem
            if contagem > max:
                max = contagem

        diferenca = max - min
        self.assertLessEqual(diferenca, 3, 'Diferenca de quem possui mais sorteios para menos sorteios é de tres ou mesno')
