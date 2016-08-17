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

    def get_resources_inc(self, player):
        if player.health <= 4:
            return 0
        elif player.health <= 8:
            return 1
        return 2

    def init_group(self):
        if self.round_number == 1:
            self.toilet = 4
        else:
            prev_round = self.in_round(self.round_number - 1)
            self.toilet = prev_round.toilet

        for player in self.get_players():
            if self.round_number == 1:
                player.health = 12
                player.resources = 9
            else:
                player_prev_round = player.in_round(self.round_number - 1)
                player.health = player_prev_round.health
                player.resources = (
                    player_prev_round.resources +
                    self.get_resources_inc(player))

    def get_health_lose(self, player):
        if player.use_toilet and self.toilet <= 4:
            return 2
        elif player.use_toilet:
            return 1
        return 0

    def set_payoff(self):
        players = self.get_players()

        # retrieve the dirt and health lose of alive players
        # also select the players part of big clean
        group_health_lose, toilet_dirt = 0., 0.
        part_of_big_clean = []
        for player in players:
            if player.health:
                if player.use_toilet and player.small_cleaning and player.resources:
                    toilet_dirt += 0.5
                elif player.use_toilet:
                    toilet_dirt += 1
                else:
                    group_health_lose += 1
                if player.big_clean:
                    part_of_big_clean.append(player)

        # set the new status of toilet
        self.toilet -= toilet_dirt
        if self.toilet < 0:
            self.toilet  = 0

        # set the healt loses
        for player in players:
            if player.health:
                player.health -= (self.get_health_lose(player) + group_health_lose)
                if player.health < 0:
                    player.health = 0

        # big clean
        if part_of_big_clean:
            contribution, resources = int(12/len(part_of_big_clean)), 0.
            for player in part_of_big_clean:
                if player.resources >= contribution:
                    resources += contribution
                    player.resources -= contribution
                else:
                    resources += plyer.resources
                    player.resources = 0

            clean_prop =  resources / 12.
            self.toilet += (12. - self.toilet) * clean_prop
        if self.toilet < 0:
            self.toilet = 0
        elif self.toilet > 12:
            self.toilet = 12

        # in the last round set the resources as payoff
        if self.round_number == Constants.num_rounds:
            for player in players:
                player.payoff = player.resources


class Player(BasePlayer):

    health = models.PositiveIntegerField(min=0, max=12)
    resources = models.PositiveIntegerField(min=0)

    use_toilet = models.BooleanField(widget=widgets.RadioSelectHorizontal())
    small_cleaning = models.BooleanField(widget=widgets.RadioSelectHorizontal())

    big_clean = models.BooleanField(widget=widgets.RadioSelectHorizontal())
