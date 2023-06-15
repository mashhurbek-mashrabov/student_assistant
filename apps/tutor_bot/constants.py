import os
from django.db import models

TUTOR_BOT_TOKEN = os.environ.get('TUTOR_BOT_TOKEN')
TUTOR_WEBHOOK_URL = os.environ.get('TUTOR_WEBHOOK_URL')


class TutorBotSteps:
    LISTING_LANGUAGE = 1
    EDIT_LANGUAGE = 2
    MAIN_MENU = 3
    GET_FULL_NAME = 4


class TutorCallbackData:
    main_menu_button = 'main_menu_button'
    back_button = 'back_button'
    skip = 'skip'
    exception = 'exception'


class TutorStatus(models.IntegerChoices):
    PENDING = 1, 'Pending'
    APPROVED = 2, 'Approved'
    REJECTED = 3, 'Rejected'
