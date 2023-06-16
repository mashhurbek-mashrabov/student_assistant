import re

from telebot.types import KeyboardButton

from common.constants import LanguageChoices
from student_bot.constants import StudentBotSteps, MembershipStatus
from student_bot.controllers.base import BaseController
from student_bot.models import Membership
from student_bot.tasks import send_request_to_join_group
from tutor_bot.models import StudentGroup


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

        if step == StudentBotSteps.GROUP_LIST:
            self.get_full_name()
        elif step == StudentBotSteps.GET_PERMANENT_ADDRESS:
            if hasattr(self.user, 'membership') and self.user.membership.status == MembershipStatus.ACTIVE:
                self.get_full_name()
                return
            self.group_list()
        elif step == StudentBotSteps.GET_RENTAL_ADDRESS:
            self.get_permanent_address()
        elif step == StudentBotSteps.GET_PASSPORT_DATA:
            self.get_rental_address()
        elif step == StudentBotSteps.GET_PHONE_NUMBER:
            self.get_passport_data()
        elif step == StudentBotSteps.GET_FATHER_DATA:
            self.get_phone_number()
        elif step == StudentBotSteps.GET_FATHER_PHONE_NUMBER:
            self.get_father_data()
        elif step == StudentBotSteps.GET_MOTHER_DATA:
            self.get_father_phone_number()
        elif step == StudentBotSteps.GET_MOTHER_PHONE_NUMBER:
            self.get_mother_data()
        elif step == StudentBotSteps.GET_PHOTO:
            self.get_mother_phone_number()

    def back_inline_button_handler(self):
        pass

    def list_language(self, text: str = None):
        uzbek = KeyboardButton(text=self.messages('uzbek'))
        english = KeyboardButton(text=self.messages('english'))
        markup = self.reply_markup()
        markup.add(uzbek, english)
        self.send_message(message_text=text or self.messages('select the language'), reply_markup=markup)
        self.set_step(StudentBotSteps.LISTING_LANGUAGE)

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
        markup = self.reply_markup()
        markup.add(KeyboardButton(text=self.t('fill data')))
        markup.add(KeyboardButton(text=f"{self.t('language flag')} {self.t('change language')}"))
        if edit_message:
            self.delete_message(message_id=self.callback_query_id)
        self.send_message(message_text=text or self.t('main menu'), reply_markup=markup)
        self.set_step(StudentBotSteps.MAIN_MENU)

    def get_full_name(self, text: str = None):
        markup = self.reply_markup()
        markup.add(self.main_menu_reply_button)
        self.send_message(message_text=text or self.t('get full name'), reply_markup=markup)
        self.set_step(StudentBotSteps.GET_FULL_NAME)

    def set_full_name(self):
        full_name = self.message_text
        if len(full_name) > 100:
            self.get_full_name(text=self.t('full name is too long'))
            return
        elif len(full_name) < 4:
            self.get_full_name(text=self.t('full name is too short'))
            return
        self.user.full_name = full_name
        self.user.save()
        if hasattr(self.user, 'membership') and self.user.membership.status == MembershipStatus.ACTIVE:
            self.get_permanent_address()
            return
        self.group_list()

    def group_list(self, text: str = None):
        markup = self.reply_markup()
        groups = StudentGroup.objects.all().order_by('name')
        for i in groups:
            markup.add(KeyboardButton(text=f"{i.name} | {i.tutor}"))
        markup.add(self.main_menu_reply_button, self.back_reply_button)
        self.send_message(message_text=text or self.t('select a group'), reply_markup=markup)
        self.set_step(StudentBotSteps.GROUP_LIST)

    def set_group(self):
        group_name = self.message_text
        group_name = group_name.split(' | ')[0]
        group = StudentGroup.objects.filter(name=group_name)
        if not group.exists():
            self.group_list()
            return
        group = group.first()
        if not hasattr(self.user, 'membership'):
            Membership.objects.create(student=self.user, group=group, status=MembershipStatus.PENDING)
        else:
            self.user.membership.group = group
            self.user.membership.status = MembershipStatus.PENDING
            self.user.membership.save()
        self.get_permanent_address()

    def get_permanent_address(self, text: str = None):
        markup = self.reply_markup()
        markup.add(self.main_menu_reply_button)
        self.send_message(message_text=text or self.t('enter permanent address'), reply_markup=markup)
        self.set_step(StudentBotSteps.GET_PERMANENT_ADDRESS)

    def set_permanent_address(self):
        permanent_address = self.message_text
        if len(permanent_address) > 100:
            self.get_permanent_address(text=self.t('text is too long'))
            return
        elif len(permanent_address) < 4:
            self.get_permanent_address(text=self.t('text is too short'))
            return
        self.user.permanent_address = permanent_address
        self.user.save()
        self.get_rental_address()

    def get_rental_address(self, text: str = None):
        markup = self.reply_markup()
        markup.add(self.main_menu_reply_button, self.back_reply_button)
        self.send_message(message_text=text or self.t('enter rental address'), reply_markup=markup)
        self.set_step(StudentBotSteps.GET_RENTAL_ADDRESS)

    def set_rental_address(self):
        address = self.message_text
        if len(address) > 100:
            self.get_rental_address(text=self.t('text is too long'))
            return
        elif len(address) < 4:
            self.get_rental_address(text=self.t('text is too short'))
            return
        self.user.rental_address = address
        self.user.save()
        self.get_passport_data()

    def get_passport_data(self, text: str = None):
        markup = self.reply_markup()
        markup.add(self.main_menu_reply_button, self.back_reply_button)
        self.send_message(message_text=text or self.t('enter passport data'), reply_markup=markup)
        self.set_step(StudentBotSteps.GET_PASSPORT_DATA)

    def set_passport_data(self):
        passport_data = self.message_text
        if len(passport_data) > 100:
            self.get_passport_data(text=self.t('text is too long'))
            return
        elif len(passport_data) < 4:
            self.get_passport_data(text=self.t('text is too short'))
            return
        self.user.passport_data = passport_data
        self.user.save()
        self.get_phone_number()

    def get_phone_number(self, text: str = None):
        markup = self.reply_markup()
        markup.add(KeyboardButton(self.t('send number button'), request_contact=True))
        markup.add(self.main_menu_reply_button, self.back_reply_button)
        self.send_message(message_text=text or self.t('enter phone number or click button'), reply_markup=markup)
        self.set_step(StudentBotSteps.GET_PHONE_NUMBER)

    def set_phone_number(self, is_contact: bool = False):
        if is_contact:
            phone = self.message.contact.phone_number
            phone = phone if "+" in phone else "+" + phone
            self.user.phone_number = phone
            self.user.save()
        else:
            phone_number = self.message_text
            pattern = r"\+998\d{9}"
            match = re.match(pattern, phone_number)
            if match:
                self.user.phone_number = phone_number
                self.user.save()
            else:
                self.get_phone_number(text=self.t('enter correct phone number'))
                return
        self.get_father_data()

    def get_father_data(self, text: str = None):
        markup = self.reply_markup()
        markup.add(self.main_menu_reply_button, self.back_reply_button)
        self.send_message(message_text=text or self.t('enter father data'), reply_markup=markup)
        self.set_step(StudentBotSteps.GET_FATHER_DATA)

    def set_father_data(self):
        father_data = self.message_text
        if len(father_data) > 100:
            self.get_father_data(text=self.t('text is too long'))
            return
        elif len(father_data) < 4:
            self.get_father_data(text=self.t('text is too short'))
            return
        self.user.father_data = father_data
        self.user.save()
        self.get_father_phone_number()

    def get_father_phone_number(self, text: str = None):
        markup = self.reply_markup()
        markup.add(self.main_menu_reply_button, self.back_reply_button)
        self.send_message(message_text=text or self.t('enter father phone number'), reply_markup=markup)
        self.set_step(StudentBotSteps.GET_FATHER_PHONE_NUMBER)

    def set_father_phone_number(self):
        father_phone_number = self.message_text
        pattern = r"\+998\d{9}"
        match = re.match(pattern, father_phone_number)
        if match:
            self.user.father_phone_number = father_phone_number
            self.user.save()
        else:
            self.get_father_phone_number(text=self.t('enter correct phone number'))
            return
        self.get_mother_data()

    def get_mother_data(self, text: str = None):
        markup = self.reply_markup()
        markup.add(self.main_menu_reply_button, self.back_reply_button)
        self.send_message(message_text=text or self.t('enter mother data'), reply_markup=markup)
        self.set_step(StudentBotSteps.GET_MOTHER_DATA)

    def set_mother_data(self):
        mother_data = self.message_text
        if len(mother_data) > 100:
            self.get_mother_data(text=self.t('text is too long'))
            return
        elif len(mother_data) < 4:
            self.get_mother_data(text=self.t('text is too short'))
            return
        self.user.mother_data = mother_data
        self.user.save()
        self.get_mother_phone_number()

    def get_mother_phone_number(self, text: str = None):
        markup = self.reply_markup()
        markup.add(self.main_menu_reply_button, self.back_reply_button)
        self.send_message(message_text=text or self.t('enter mother phone number'), reply_markup=markup)
        self.set_step(StudentBotSteps.GET_MOTHER_PHONE_NUMBER)

    def set_mother_phone_number(self):
        mother_phone_number = self.message_text
        pattern = r"\+998\d{9}"
        match = re.match(pattern, mother_phone_number)
        if match:
            self.user.mother_phone_number = mother_phone_number
            self.user.save()
        else:
            self.get_mother_phone_number(text=self.t('enter correct phone number'))
            return
        self.get_photo()

    def get_photo(self, text: str = None):
        markup = self.reply_markup()
        markup.add(self.main_menu_reply_button, self.back_reply_button)
        self.send_message(message_text=text or self.t('send photo'), reply_markup=markup)
        self.set_step(StudentBotSteps.GET_PHOTO)

    def set_photo(self):
        self.user.photo_id = self.message.photo[0].file_id
        self.user.save()
        self.send_message(message_code='your information saved')
        if hasattr(self.user, 'membership') and self.user.membership.status == MembershipStatus.PENDING:
            send_request_to_join_group.delay(self.user.id)
            self.send_message(message_code='sent request to join the group')
        self.main_menu()

