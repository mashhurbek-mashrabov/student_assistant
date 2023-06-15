import traceback

import telebot
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telebot.util import content_type_media

from student_bot.controllers.main import BotController
from student_bot.loader import bot
from common.utils import send_exception


@csrf_exempt
def student_webhook_handler(request):
    print(request.body)
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
    except:
        send_exception(traceback.format_exc(), 'start_handler', user=message.from_user)


@bot.message_handler(content_types=['text'])
def message_handler(message):
    pass


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(message):
    pass


@bot.message_handler(func=lambda message: True, content_types=content_type_media)
def echo_all(message):
    pass
