import traceback

import telebot
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telebot.util import content_type_media

from student_bot.constants import StudentBotSteps
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
        elif message_text == controller.t('fill data'):
            controller.get_full_name()
        elif user_step == StudentBotSteps.LISTING_LANGUAGE:
            controller.set_language()
        elif user_step == StudentBotSteps.GET_FULL_NAME:
            controller.set_full_name()
        elif user_step == StudentBotSteps.GROUP_LIST:
            controller.set_group()
        elif user_step == StudentBotSteps.GET_PERMANENT_ADDRESS:
            controller.set_permanent_address()
        elif user_step == StudentBotSteps.GET_RENTAL_ADDRESS:
            controller.set_rental_address()
        elif user_step == StudentBotSteps.GET_PASSPORT_DATA:
            controller.set_passport_data()
        elif user_step == StudentBotSteps.GET_PHONE_NUMBER:
            controller.set_phone_number()
        elif user_step == StudentBotSteps.GET_FATHER_DATA:
            controller.set_father_data()
        elif user_step == StudentBotSteps.GET_FATHER_PHONE_NUMBER:
            controller.set_father_phone_number()
        elif user_step == StudentBotSteps.GET_MOTHER_DATA:
            controller.set_mother_data()
        elif user_step == StudentBotSteps.GET_MOTHER_PHONE_NUMBER:
            controller.set_mother_phone_number()

    except:
        send_exception(traceback.format_exc(), 'start_handler', user=message.from_user)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(message):
    pass


@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    controller = BotController(message, bot)
    user_step = controller.step
    try:
        if user_step == StudentBotSteps.GET_PHONE_NUMBER:
            controller.set_phone_number(True)
    except:
        send_exception(traceback.format_exc(), 'start_handler', user=message.from_user)


@bot.message_handler(content_types=['photo'])
def contact_handler(message):
    controller = BotController(message, bot)
    user_step = controller.step
    try:
        if user_step == StudentBotSteps.GET_PHOTO:
            controller.set_photo()
    except:
        send_exception(traceback.format_exc(), 'start_handler', user=message.from_user)


@bot.message_handler(func=lambda message: True, content_types=content_type_media)
def echo_all(message):
    pass
