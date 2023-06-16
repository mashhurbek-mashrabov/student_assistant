import os

from django.db import models

STUDENT_BOT_TOKEN = os.environ.get('STUDENT_BOT_TOKEN')
STUDENT_WEBHOOK_URL = os.environ.get('STUDENT_WEBHOOK_URL')


class StudentBotSteps:
    LISTING_LANGUAGE = 1
    MAIN_MENU = 2
    GET_FULL_NAME = 3
    GROUP_LIST = 4
    GET_PERMANENT_ADDRESS = 5
    GET_RENTAL_ADDRESS = 6
    GET_PASSPORT_DATA = 7
    GET_PHONE_NUMBER = 8
    GET_FATHER_DATA = 9
    GET_FATHER_PHONE_NUMBER = 10
    GET_MOTHER_DATA = 11
    GET_MOTHER_PHONE_NUMBER = 12
    GET_PHOTO = 13


class StudentCallbackData:
    main_menu_button = 'main_menu_button'
    back_button = 'back_button'
    skip = 'skip'
    exception = 'exception'


class MembershipStatus(models.IntegerChoices):
    NEW = 1, 'New'
    PENDING = 2, 'Pending'
    ACTIVE = 3, 'Active'
    REJECTED = 4, 'Rejected'