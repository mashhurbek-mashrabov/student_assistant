from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config.celery import app
from student_bot.models import StudentTelegramUser
from tutor_bot.constants import TutorCallbackData
from tutor_bot.loader import bot
from tutor_bot.strings import messages


@app.task
def send_request_to_join_group(user_id):
    student = StudentTelegramUser.objects.get(id=user_id)
    group = student.membership.group
    tutor = group.tutor
    if student.username:
        link = 'https://t.me/' + student.username
    else:
        link = f'tg://user?id={student.chat_id}'
    text = messages.get(tutor.language).get('request join group').format(group_name=group.name, link=link, student_name=student.full_name)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton(text=messages.get(tutor.language).get('yes'), callback_data=f"{TutorCallbackData.approve_student}:{student.id}"))
    markup.add(InlineKeyboardButton(text=messages.get(tutor.language).get('no'), callback_data=f"{TutorCallbackData.approve_student}:{student.id}"))
    bot.send_message(tutor.chat_id, text, parse_mode='HTML', reply_markup=markup, disable_web_page_preview=True)