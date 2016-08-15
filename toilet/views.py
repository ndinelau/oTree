# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions1(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class Instructions2(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class Instructions3(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class Instructions4(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class InitGroup(WaitPage):
    def after_all_players_arrive(self):
        self.group.init_group()


class Choice(Page):
    form_model = models.Player
    form_fields = ['use_toilet', 'small_cleaning', 'big_clean']

    def is_displayed(self):
        return self.player.health > 0


class ChoiceWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoff()


class Results(Page):
    pass


page_sequence = [
    #~ Instructions1, Instructions2, Instructions3, Instructions4,
    InitGroup, Choice, ChoiceWaitPage, Results

]
