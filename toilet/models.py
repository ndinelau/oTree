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


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    toilet_clean = models.PositiveIntegerField(min=0, max=12, default=4)


class Player(BasePlayer):

    health = models.PositiveIntegerField(min=0, max=12, default=12)
    resources = models.PositiveIntegerField(min=0, default=9)

    use_toilet = models.BooleanField()
    small_cleaning = models.BooleanField()

    big_clean = models.BooleanField()
