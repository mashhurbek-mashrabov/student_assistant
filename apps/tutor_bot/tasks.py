from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from common.constants import MODERATOR_CHANNEL_ID
from config.celery import app
from tutor_bot.loader import bot
from tutor_bot.models import TutorTelegramUser
from tutor_bot.constants import TutorCallbackData


@app.task
def send_tutor_verification_to_admin(tutor_id):
    user = TutorTelegramUser.objects.get(id=tutor_id)
    if user.username:
        link = 'https://t.me/' + user.username
    else:
        link = f'tg://user?id={user.chat_id}'
    text = f"Ushbu foyalanuvchi <b>tutor</b> sifatida ro'yxatdan o'tmoqchi. Uni tasdiqlaysizmi?\n" \
           f"<a href='{link}'>{user.full_name}</a>"
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton(text='✅ Ha', callback_data=f"{TutorCallbackData.approve_tutor}:{user.id}"))
    markup.add(InlineKeyboardButton(text="❌ Yo'q", callback_data=f"{TutorCallbackData.reject_tutor}:{user.id}"))
    bot.send_message(MODERATOR_CHANNEL_ID, text, parse_mode='HTML', reply_markup=markup, disable_web_page_preview=True)

