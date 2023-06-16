import os
from django.db import models

TUTOR_BOT_TOKEN = os.environ.get('TUTOR_BOT_TOKEN')
TUTOR_WEBHOOK_URL = os.environ.get('TUTOR_WEBHOOK_URL')


class TutorBotSteps:
    LISTING_LANGUAGE = 1
    EDIT_LANGUAGE = 2
    MAIN_MENU = 3
    GET_FULL_NAME = 4
    GET_GROUPS = 5
    GET_GROUP_NAME = 6


class TutorCallbackData:
    main_menu_button = 'main_menu_button'
    back_button = 'back_button'
    skip = 'skip'
    exception = 'exception'
    approve_tutor = 'approve_tutor'
    reject_tutor = 'reject_tutor'
    approve_student = 'approve_student'
    reject_student = 'reject_student'


class TutorStatus(models.IntegerChoices):
    NEW = 1, 'NEW'
    PENDING = 2, 'Pending'
    VERIFIED = 3, 'Verified'
    REJECTED = 4, 'Rejected'
