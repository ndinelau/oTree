# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class ChatWaitPage(WaitPage):
    pass


class Chat(Page):
    pass


page_sequence = [
    ChatWaitPage,
    Chat,
]
