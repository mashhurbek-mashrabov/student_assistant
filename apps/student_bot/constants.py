import os

STUDENT_BOT_TOKEN = os.environ.get('STUDENT_BOT_TOKEN')
STUDENT_WEBHOOK_URL = os.environ.get('STUDENT_WEBHOOK_URL')


class StudentBotSteps:
    LISTING_LANGUAGE = 1


class CallbackData:
    main_menu_button = 'main_menu_button'
    back_button = 'back_button'
    skip = 'skip'
    exception = 'exception'
