import traceback

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import user_link

from common.constants import EXCEPTION_CHANNEL_ID
from common.strings import messages
from tutor_bot.constants import TutorCallbackData
from tutor_bot.loader import bot


def send_exception(e, step, user=None):
    try:
        user_step = step
        telegram_user_id = ''
        if user:
            if user.username:
                telegram_user_id = '@' + user.username
            else:
                telegram_user_id = user_link(user)
        except_message = f"{messages.get('person emoji')} {telegram_user_id}\n" \
                         f"{messages.get('step emoji')} {user_step}\n\n" \
                         f"{messages.get('warning emoji')} {e[len(e) - 1020:]}"
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(InlineKeyboardButton(messages.get('condition emoji'), callback_data=TutorCallbackData.exception))
        bot.send_message(chat_id=EXCEPTION_CHANNEL_ID, text=except_message, reply_markup=markup,
                         parse_mode='HTML')
    except Exception as e:
        print(e)
        print(traceback.format_exc())
