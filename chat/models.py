# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import itertools
import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
# </standard imports>

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'chat'
    players_per_group = 4
    num_rounds = 1

    treatment_small_talk = "small_talk"
    treatment_normal_talk = "normal_talk"
    treatments = (treatment_small_talk, treatment_normal_talk)


class Subsession(BaseSubsession):

    def before_session_starts(self):
        treatments = itertools.cycle(Constants.treatments)
        for group in self.get_groups():
            group.treatment = next(treatments)


class Group(BaseGroup):

    treatment = models.CharField(choices=Constants.treatments)


class Player(BasePlayer):
    pass


# =============================================================================
# CHAT
# =============================================================================

class Message(models.Model):

    group = models.ForeignKey(Group)
    player = models.ForeignKey(Player)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    COLORS = {1: "#4F6FAB", 2: "#60AB4F", 3: "#FCC767", 4: "#FF7979"}

    @property
    def color(self):
        return Message.COLORS[self.player.id_in_group]

