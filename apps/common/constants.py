import os

from django.db import models

DOMAIN = os.environ.get('DOMAIN')
EXCEPTION_CHANNEL_ID = os.environ.get('EXCEPTION_CHANNEL_ID')


class LanguageChoices(models.IntegerChoices):
    ENGLISH = 1, 'English'
    UZBEK = 2, 'Uzbek'
