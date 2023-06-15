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

    def back_inline_button_handler(self):
        pass
