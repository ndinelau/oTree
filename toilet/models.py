# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
# </standard imports>

author = 'Juan B Cabral'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'toilet'
    players_per_group = 4
    num_rounds = 12

    treatment_affective = "affective"
    treatment_not_affective = "not affective"
    treatments = (treatment_affective, treatment_not_affective)



class Subsession(BaseSubsession):

     def before_session_starts(self):
        groups = self.get_groups()
        if self.round_number == 1:
            groups_n = len(groups)
            not_affective = int(groups_n / 2)
            for idx, g in enumerate(groups):
                if idx < not_affective:
                    g.treatment = Constants.treatment_not_affective
                else:
                    g.treatment = Constants.treatment_affective
        else:
            for g in groups:
                g.treatment = g.in_round(1).treatment


class Group(BaseGroup):

    toilet_clean = models.PositiveIntegerField(min=0, max=12, default=4)
    treatment = models.CharField(choices=Constants.treatments)

    def init_group(self):
        import ipdb; ipdb.set_trace()


class Player(BasePlayer):

    health = models.PositiveIntegerField(min=0, max=12)
    resources = models.PositiveIntegerField(min=0)

    use_toilet = models.BooleanField(widget=widgets.RadioSelectHorizontal())
    small_cleaning = models.BooleanField(widget=widgets.RadioSelectHorizontal())

    big_clean = models.BooleanField(widget=widgets.RadioSelectHorizontal())

    def init_player(self):
        import ipdb; ipdb.set_trace()
        if self.health < 12:
            self.health += 1
