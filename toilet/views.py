# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Choice(Page):

    form_model = models.Player
    form_fields = ['use_toilet', 'small_cleaning']


class ChoiceWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class BigClean(Page):
    pass


class BigCleanWaitPahe(WaitPage):

    def after_all_players_arrive(self):
        pass


class Result(Page):
    pass


page_sequence = [
    Choice,

]
