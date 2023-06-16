from django.db import models

from common.constants import LanguageChoices
from common.models import BaseModel
from tutor_bot.constants import TutorStatus


class TutorTelegramUser(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    chat_id = models.BigIntegerField(unique=True)
    language = models.CharField(max_length=5, null=True, blank=True, choices=LanguageChoices.choices,
                                default=LanguageChoices.UZBEK)
    step = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(choices=TutorStatus.choices, default=TutorStatus.NEW)

    def __str__(self):
        return self.full_name or self.name

    @property
    def is_verified(self):
        return self.status == TutorStatus.VERIFIED

    @property
    def joined_at(self):
        return f'{self.date.strftime("%X")} {self.date.strftime("%x")}'


class StudentGroup(BaseModel):
    name = models.CharField(max_length=100, null=True)
    tutor = models.ForeignKey('tutor_bot.TutorTelegramUser', on_delete=models.CASCADE, related_name='student_groups')

    def __str__(self):
        return f'{self.name}'
