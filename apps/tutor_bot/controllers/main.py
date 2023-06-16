from telebot.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from common.constants import LanguageChoices, MODERATOR_CHANNEL_ID
from student_bot.constants import MembershipStatus
from student_bot.models import StudentTelegramUser
from tutor_bot.constants import TutorBotSteps, TutorStatus
from tutor_bot.controllers.base import BaseController
from tutor_bot.models import TutorTelegramUser
from tutor_bot.tasks import send_tutor_verification_to_admin
from student_bot.loader import bot as s_bot


class BotController(BaseController):
    def greeting(self, restart: bool = False):
        self.sync_user()
        if restart:
            self.send_message(message_text=self.messages('restart bot'))
        else:
            self.send_message(message_text=self.messages('greeting'))

    def send_exception_message_to_user(self):
        step = self.step

    def back_reply_button_handler(self):
        step = self.step

        if step == TutorBotSteps.GET_FULL_NAME:
            self.list_language()
        elif step == TutorBotSteps.GET_GROUP_NAME:
            self.get_groups()

    def back_inline_button_handler(self):
        pass

    def list_language(self, text: str = None):
        uzbek = KeyboardButton(text=self.messages('uzbek'))
        english = KeyboardButton(text=self.messages('english'))
        markup = self.reply_markup()
        markup.add(uzbek, english)
        self.send_message(message_text=text or self.messages('select the language'), reply_markup=markup)
        self.set_step(TutorBotSteps.LISTING_LANGUAGE)

    def set_language(self):
        selected_language = self.message_text
        if selected_language == self.messages('english'):
            self.user.language = LanguageChoices.ENGLISH
        elif selected_language == self.messages('uzbek'):
            self.user.language = LanguageChoices.UZBEK
        else:
            self.list_language(text=self.messages("selected language doesn't exist"))
            return
        self.user.save()
        self.main_menu(text=self.t('saved your language'))

    def main_menu(self, text: str = None, edit_message: bool = False):
        if self.user.full_name is None:
            if text:
                self.send_message(message_text=text)
            self.get_full_name()
            return
        markup = self.reply_markup()
        markup.add(KeyboardButton(text=self.t('groups')))
        markup.add(KeyboardButton(text=f"{self.t('language flag')} {self.t('change language')}"))
        if edit_message:
            self.delete_message(message_id=self.callback_query_id)
        self.send_message(message_text=text or self.t('main menu'), reply_markup=markup)
        if self.user.status == TutorStatus.NEW:
            send_tutor_verification_to_admin.delay(self.user.id)
            self.send_message(message_code='verification sent')
            self.user.status = TutorStatus.PENDING
        self.set_step(TutorBotSteps.MAIN_MENU)

    def get_full_name(self, text: str = None):
        markup = self.reply_markup()
        markup.add(self.back_reply_button)
        self.send_message(message_text=text or self.t('get full name'), reply_markup=markup)
        self.set_step(TutorBotSteps.GET_FULL_NAME)

    def set_full_name(self):
        full_name = self.message_text
        if len(full_name) < 3:
            self.get_full_name(text=self.t('full name is too short'))
            return
        elif len(full_name) > 40:
            self.get_full_name(text=self.t('full name is too long'))
            return
        self.user.full_name = full_name
        self.user.save()
        self.main_menu(text=self.t('saved'))

    def get_groups(self, text: str = None):
        if not self.user.is_verified:
            self.main_menu(text=self.t('you ware not verified'))
            return
        markup = self.reply_markup()
        groups = self.user.student_groups.all().order_by('name')
        for i in groups:
            markup.add(KeyboardButton(text=i.name))
        markup.add(self.main_menu_reply_button, KeyboardButton(text=self.t('add group')))
        self.send_message(message_text=text or self.t('get groups'), reply_markup=markup)
        self.set_step(TutorBotSteps.GET_GROUPS)

    def approve_tutor(self):
        try:
            user_id = self.callback_data.split(':')[1]
            user = TutorTelegramUser.objects.get(id=user_id)
            user.status = TutorStatus.VERIFIED
            user.save()
            markup = self.inline_markup()
            markup.add(InlineKeyboardButton(text=self.messages('approved'), callback_data='None'))
            self.edit_message(chat_id=MODERATOR_CHANNEL_ID, message=self.message.message.html_text,
                              message_id=self.callback_query_id, reply_markup=markup)
            self.send_message(chat_id=user.chat_id, message_text=self.t('you are approved', user.language))
        except Exception as e:
            self.answer_callback(message=str(e), show_alert=True)

    def reject_tutor(self):
        try:
            user_id = self.callback_data.split(':')[1]
            user = TutorTelegramUser.objects.get(id=user_id)
            user.status = TutorStatus.REJECTED
            user.save()
            markup = self.inline_markup()
            markup.add(InlineKeyboardButton(text=self.messages('rejected'), callback_data='None'))
            self.edit_message(chat_id=MODERATOR_CHANNEL_ID, message=self.message.message.html_text,
                              message_id=self.callback_query_id, reply_markup=markup)
            self.send_message(chat_id=user.chat_id, message_text=self.t('you are rejected', user.language))
        except Exception as e:
            self.answer_callback(message=str(e), show_alert=True)

    def get_group_name(self, text: str = None):
        markup = self.reply_markup()
        markup.add(self.main_menu_reply_button, self.back_reply_button)
        self.send_message(message_text=text or self.t('get group name'), reply_markup=markup)
        self.set_step(TutorBotSteps.GET_GROUP_NAME)

    def create_student_group(self):
        group_name = self.message_text
        if len(group_name) < 3:
            self.get_group_name(text=self.t('group name is too short'))
            return
        elif len(group_name) > 15:
            self.get_group_name(text=self.t('group name is too long'))
            return
        self.user.student_groups.create(name=group_name)
        self.get_groups(text=self.t('saved'))

    def approve_student_membership(self):
        student_id = self.callback_data.split(':')[1]
        student = StudentTelegramUser.objects.get(id=student_id)
        student.membership.status = MembershipStatus.ACTIVE
        student.membership.save()
        markup = self.inline_markup()
        markup.add(InlineKeyboardButton(text=self.messages('approved'), callback_data='None'))
        self.edit_message(message_id=self.callback_query_id, message=self.message.message.html_text, reply_markup=markup)
        s_bot.send_message(chat_id=student.chat_id, text=self.t('your request approved', student.language).format(group_name=student.membership.group.name), parse_mode='HTML')

    def reject_student_membership(self):
        student_id = self.callback_data.split(':')[1]
        student = StudentTelegramUser.objects.get(id=student_id)
        student.membership.status = MembershipStatus.REJECTED
        student.membership.save()
        markup = self.inline_markup()
        markup.add(InlineKeyboardButton(text=self.messages('rejected'), callback_data='None'))
        self.edit_message(message_id=self.callback_query_id, message=self.message.message.html_text, reply_markup=markup)
        s_bot.send_message(chat_id=student.chat_id, text=self.t('your request rejected', student.language).format(group_name=student.membership.group.name), parse_mode='HTML')