# -*- coding: utf-8 -*-
from __future__ import division

from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.template import loader

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


MESSAGES_TPL = loader.get_template("chat/messages.html")


# =============================================================================
# PAGES
# =============================================================================

class ChatWaitPage(WaitPage):
    pass


class Chat(Page):
    pass

page_sequence = [
    ChatWaitPage,
    Chat,
]

# =============================================================================
# CHAT WEB SOCKET
# =============================================================================

@require_GET
def retrieve_messages(request):
    MESSAGES_TPL = loader.get_template("chat/messages.html")
    player_id = int(request.GET["player"])

    player = models.Player.objects.get(id=player_id)
    group = player.group

    messages = models.Message.objects.filter(group=group).order_by("timestamp")
    message_html = MESSAGES_TPL.render({"messages": messages});
    return JsonResponse({"messagesHTML": message_html})


@require_POST
def send_message(request):
    player_id = int(request.POST["player"])
    message_txt = request.POST["message"]

    player = models.Player.objects.get(id=player_id)
    group = player.group

    message = models.Message.objects.create(
    group=group, player=player, message=message_txt)

    response = JsonResponse({'message': message.id})
    return response
