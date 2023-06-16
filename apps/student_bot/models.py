from django.db import models

from common.constants import LanguageChoices
from common.models import BaseModel
from student_bot.constants import MembershipStatus


class StudentTelegramUser(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    chat_id = models.BigIntegerField(unique=True)
    language = models.CharField(max_length=5, null=True, blank=True, choices=LanguageChoices.choices,
                                default=LanguageChoices.UZBEK)

    full_name = models.CharField(max_length=100, null=True)
    permanent_address = models.CharField(max_length=150, null=True)
    rental_address = models.CharField(max_length=150, null=True)
    passport_data = models.CharField(max_length=150, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    father_data = models.CharField(max_length=150, null=True)
    father_phone_number = models.CharField(max_length=15, null=True)
    mother_data = models.CharField(max_length=150, null=True)
    mother_phone_number = models.CharField(max_length=15, null=True)
    photo_id = models.CharField(max_length=100, null=True)

    step = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.chat_id} - {self.name}'

    @property
    def joined_at(self):
        return f'{self.date.strftime("%X")} {self.date.strftime("%x")}'


class Membership(BaseModel):
    student = models.OneToOneField(StudentTelegramUser, on_delete=models.CASCADE, related_name='membership',
                                   parent_link=True)
    group = models.ForeignKey('tutor_bot.StudentGroup', on_delete=models.CASCADE, related_name='students')
    status = models.IntegerField(choices=MembershipStatus.choices, default=MembershipStatus.NEW)

    # def __str__(self):
    #     return f'{self.student.full_name} - {self.group.name}'

    @property
    def is_active(self):
        return self.status == MembershipStatus.ACTIVE

    @property
    def is_rejected(self):
        return self.status == MembershipStatus.REJECTED
