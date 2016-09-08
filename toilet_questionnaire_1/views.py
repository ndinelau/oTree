# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Questionnaire1(Page):

    form_model = models.Player
    form_fields = [
        'q_first_game_judge_satisfied', "q_first_game_judge_surprised", "q_first_game_judge_upset",

        'q_players_helping_each_other',
        'q_team_spirit_or_cohesion',
        'q_important_presented_image_of_and_to_yourself',
        'q_important_maximum_and_fair_resources_to_everyone',
        'q_important_other_members_trust_in_you',
        'q_important_not_you_maximum_and_fair_resources_to_everyone',
        'q_trust_do_you_have_into_other_members',
        'q_how_much_do_you_like_the_other_team_members',
        'q_how_good_do_you_understand_solving',
        'q_how_good_do_the_other_group_members_understand_solving',

        'q_how_to_improve_the_groups_behavior_to_maximize_resources',
        'q_which_strategy_would_you_follow_and_why',
        'q_if_communicate_what_would_you_say_and_why']



page_sequence = [
    Questionnaire1
]
