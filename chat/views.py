# -*- coding: utf-8 -*-
from __future__ import division

import csv
import datetime

from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.template import loader
from django.forms.models import model_to_dict
from django.utils.six.moves import range
from django.http import HttpResponse

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants

import dateutil.parser


MESSAGES_TPL = loader.get_template("chat/messages.html")


# =============================================================================
# PAGES
# =============================================================================

class SmallTalk(Page):

    def is_displayed(self):
        return self.player.group.treatment  == Constants.treatment_small_talk


class ChatWaitPage(WaitPage):
    pass


class Chat(Page):
    pass

page_sequence = [
    #~ SmallTalk,
    ChatWaitPage,
    Chat,
]

# =============================================================================
# CHAT WEB SOCKET
# =============================================================================

@require_GET
def retrieve_messages(request):
    MESSAGES_TPL = loader.get_template("chat/messages.html")
    group_id = int(request.GET["group"])
    last_message = request.GET["last_message"] or None

    messages = models.Message.objects.filter(group__id=group_id)

    if last_message:
        last_message = dateutil.parser.parse(last_message)
        messages = messages.filter(timestamp__gt=last_message)

    messages = list(messages.order_by("timestamp")[:10].select_related())

    if messages:
        message_html = MESSAGES_TPL.render({"messages": messages})
        last_message = messages[-1].timestamp.isoformat()
        response = {
            "hasMessages": True,
            "messagesHTML": message_html,
            "lastMessage": last_message}
    else:
        response = {"hasMessages": False}
    return JsonResponse(response)

@require_POST
def send_message(request):
    group_id = int(request.POST["group"])
    player_id = int(request.POST["player"])
    message_txt = request.POST["message"]

    message = models.Message.objects.create(
        group_id=group_id, player_id=player_id, message=message_txt)

    response = JsonResponse({'message': message.id})
    return response


@require_GET
def export(request):
    class Echo(object):
        def write(self, value):
            return value

    rows = []
    fieldnames = set()
    for msg in models.Message.objects.all().order_by("timestamp"):
        player = msg.player
        participant = player.participant
        group = msg.group
        subsession = group.subsession
        session = subsession.session

        row = {
            "Participant.id_in_session": participant.id_in_session,
            "Participant.code": participant.code,
            "Participant.label": participant.label,
            "Participant._is_bot": participant._is_bot,
            "Participant._index_in_pages": participant._index_in_pages,
            "Participant._max_page_index": participant._max_page_index,
            "Participant._current_app_name": participant._current_app_name,
            "Participant._round_number": participant._round_number,
            "Participant._current_page_name": participant._current_page_name,
            "Participant.ip_address": participant.ip_address,
            "Participant.time_started": participant.time_started,
            "Participant.exclude_from_data_analysis": participant.exclude_from_data_analysis,
            "Participant.visited": participant.visited,
            "Participant.mturk_worker_id": participant.mturk_worker_id,
            "Participant.mturk_assignment_id": participant.mturk_assignment_id,

            "Player.id_in_group": player.id_in_group,
            "Group.id_in_subsession": group.id_in_subsession,

            "Subsession.round_number": subsession.round_number,

            "Session.code": session.code,
            "Session.label": session.label,
            "Session.experimenter_name": session.experimenter_name,
            "Session.time_scheduled": session.time_scheduled,
            "Session.time_started": session.time_started,
            "Session.comment": session.comment,
            "Session.is_demo": session.is_demo,

            "Message.message": msg.message,
            "Message.timestamp": msg.timestamp.isoformat(),
        }

        fieldnames.update(row.keys())
        rows.append(row)


    now = datetime.date.today().isoformat()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="chat_messages (accesed {}).csv"'.format(now)

    writer = csv.DictWriter(response, list(fieldnames))
    writer.writeheader()
    writer.writerows(rows)

    return response


