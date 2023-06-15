from telebot.types import KeyboardButton

from common.constants import LanguageChoices
from tutor_bot.constants import TutorBotSteps
from tutor_bot.controllers.base import BaseController


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

    def main_menu(self, text: str = None):
        if self.user.full_name is None:
            if text:
                self.send_message(message_text=text)
            self.get_full_name()
            return
        markup = self.reply_markup()
        markup.add(KeyboardButton(text=self.t('groups')))
        markup.add(KeyboardButton(text=f"{self.t('language flag')} {self.t('change language')}"))
        self.send_message(message_text=text or self.t('main menu'), reply_markup=markup)
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