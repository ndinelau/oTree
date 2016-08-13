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

    toilet = models.FloatField(min=0, max=12, default=4)
    treatment = models.CharField(choices=Constants.treatments)

    def init_group(self):
        if self.round_number == 1:
            self.toilet_clean = 4
        else:
            self.toilet_clean = self.in_round(1).toilet_clean
        for p in self.get_players():
            p.init_player()

    def set_payoff(self):
        players = self.get_players()

        # retrieve the dirt and health lose of alive players
        # also select the part of big clean
        health_lose, toilet_dirt = 0., 0.
        part_of_big_clean = []
        for player in players:
            if player.health:
                if player.use_toilet and player.small_cleaning and player.resources:
                    toilet_dirt += 0.5
                elif player.use_toilet:
                    toilet_dirt += 1
                else:
                    healt_lose += 1
                if player.big_clean:
                    big_clean.append(player)

        # set the new status of toilet
        self.toilet -= toilet_dirt
        if self.toilet < 0:
            self.toilet  = 0

        # set the healt loses
        for player in players:
            if player.health:
                player.health -= healt_lose
                if player.health < 0:
                    player.health = 0

        # big clean
        #~ for player in big_clean:







class Player(BasePlayer):

    health = models.PositiveIntegerField(min=0, max=12)
    resources = models.PositiveIntegerField(min=0)

    use_toilet = models.BooleanField(widget=widgets.RadioSelectHorizontal())
    small_cleaning = models.BooleanField(widget=widgets.RadioSelectHorizontal())

    big_clean = models.BooleanField(widget=widgets.RadioSelectHorizontal())

    def init_player(self):
        if self.round_number == 1:
            self.health = 12
            self.resources = 9
        else:
            import ipdb; ipdb.set_trace()
