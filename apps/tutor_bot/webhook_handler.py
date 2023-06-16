import traceback

import telebot
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telebot.callback_data import CallbackData
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import content_type_media

from common.constants import EXCEPTION_CHANNEL_ID
from tutor_bot.constants import TutorBotSteps, TutorCallbackData
from tutor_bot.controllers.main import BotController
from tutor_bot.loader import bot
from common.utils import send_exception
from tutor_bot.strings import messages


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
        elif message_text == controller.t('groups'):
            controller.get_groups()
        elif message_text == controller.t('add group'):
            controller.get_group_name()
        elif user_step == TutorBotSteps.LISTING_LANGUAGE:
            controller.set_language()
        elif user_step == TutorBotSteps.GET_FULL_NAME:
            controller.set_full_name()
        elif user_step == TutorBotSteps.GET_GROUP_NAME:
            controller.create_student_group()
    except:
        send_exception(traceback.format_exc(), 'start_handler', user=message.from_user)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(message):
    controller = BotController(message, bot)
    user_step = controller.step
    callback_data = message.data
    try:
        if callback_data == TutorCallbackData.main_menu_button:
            controller.main_menu(edit_message=True)
        elif callback_data.startswith(TutorCallbackData.back_button):
            controller.back_inline_button_handler()
        elif callback_data.startswith(TutorCallbackData.approve_tutor):
            controller.approve_tutor()
        elif callback_data.startswith(TutorCallbackData.reject_tutor):
            controller.reject_tutor()
        elif callback_data.startswith(TutorCallbackData.approve_student):
            controller.approve_student_membership()
        elif callback_data.startswith(TutorCallbackData.reject_student):
            controller.reject_student_membership()
        elif callback_data == TutorCallbackData.exception:
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(InlineKeyboardButton(messages.get('true icon'), callback_data='None'))
            bot.edit_message_text(chat_id=EXCEPTION_CHANNEL_ID, text=message.message.text, reply_markup=markup, message_id=controller.callback_query_id)
    except:
        send_exception(traceback.format_exc(), 'callback_handler', user=message.from_user)


@bot.message_handler(func=lambda message: True, content_types=content_type_media)
def echo_all(message):
    pass
