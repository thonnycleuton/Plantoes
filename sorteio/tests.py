# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from sorteio.forms import SorteioForm

# Create your tests here.
class SorteioFormTestCase(TestCase):
    form = SorteioForm()
    form.sortear()

