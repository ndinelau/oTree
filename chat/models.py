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

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'chat'
    players_per_group = 4
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# =============================================================================
# CHAT
# =============================================================================

class Room(models.Model):

    group = models.ForeignKey(Group)


class Message(models.Model):

    room = models.ForeignKey(Room)
    player = models.ForeignKey(Player)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)