import traceback

import telebot
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telebot.util import content_type_media

from tutor_bot.constants import TutorBotSteps
from tutor_bot.controllers.main import BotController
from tutor_bot.loader import bot
from common.utils import send_exception


@csrf_exempt
def tutor_webhook_handler(request):
    if request.method == 'POST':
        bot.process_new_updates(
            [telebot.types.Update.de_json(
                request.body.decode("utf-8")
            )]
        )
        return HttpResponse(status=200)
    else:
        return HttpResponse('.')


@bot.message_handler(commands=['start'])
def start_handler(message):
    try:
        controller = BotController(message, bot)
        controller.greeting()
        controller.list_language()
    except:
        send_exception(traceback.format_exc(), 'start_handler', user=message.from_user)


@bot.message_handler(content_types=['text'])
def message_handler(message):
    controller = BotController(message, bot)
    user_step = controller.step
    message_text = message.text
    try:
        if message_text == controller.t('main menu'):
            controller.main_menu()
        elif message_text == controller.t('back button'):
            controller.back_reply_button_handler()
        elif message_text == f"{controller.t('language flag')} {controller.t('change language')}":
            controller.list_language()
        elif user_step == TutorBotSteps.LISTING_LANGUAGE:
            controller.set_language()
        elif user_step == TutorBotSteps.GET_FULL_NAME:
            controller.set_full_name()
    except:
        send_exception(traceback.format_exc(), 'start_handler', user=message.from_user)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(message):
    pass


@bot.message_handler(func=lambda message: True, content_types=content_type_media)
def echo_all(message):
    pass
