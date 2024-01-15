import telebot
from requests.exceptions import RequestException
import time
from db import CreateMenu

from utils import add_students

bot = telebot.TeleBot("6773819389:AAE-OYFbtkhIZDsoC67YTzo1LGRO777MPMc")
cm = CreateMenu()

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать", reply_markup= cm.create_menu('main'))

questions = ["Напишите Ф.И. ученика", "Дата начала обучения"]

################## ADD STUDENT ########################

user_answers = []

def start_add_student(message, format, again=None):
    global user_answers
    user_answers = [format]
    if again:       
        ask_next_question(message)
    else:
        ask_next_question(message.chat.id)

def ask_next_question(user_id):
    if len(user_answers) <= len(questions):
        question_text = questions[len(user_answers)-1]
        bot.send_message(user_id, question_text)
    else:
        process_student_data(user_id)

@bot.message_handler(func=lambda message: True)
def handle_user_input(message):
    global user_answers
    user_answers.append(message.text)
    ask_next_question(message.chat.id)

def process_student_data(user_id):
    # Здесь вы можете использовать или сохранить ответы из user_answers
    message = add_students(user_answers)
    image_path = '/Users/mac/Desktop/code_/free-works/feelz_problem/Unknown.png'
    # if 'успешно' not in message:
    #     bot.send_message(user_id, message)
    #     start_add_student(user_id, user_answers, 'again')
    # else:
    with open(image_path, 'rb') as image_file:
        bot.send_photo(user_id, image_file, caption=message, parse_mode='HTML')
    # bot.send_message(user_id, message)
    bot.send_message(user_id, text="Что делаем?", reply_markup= cm.create_menu('main'))

########################################################################


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'new_student':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите формат", reply_markup= cm.create_menu('new_student'))
    if call.data == 'pay':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Новое расписание", reply_markup= cm.create_menu('pay'))
    if call.data == 'back':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Что делаем?", reply_markup= cm.create_menu('main'))
    if call.data == 'cold':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Проверьте данные", reply_markup= cm.create_menu('cold'))

    """new student"""
    if call.data in ['mwf', 'tts', 'ed']:
        start_add_student(call.message, call.data)

    



if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, interval=2)

            break
        except (telebot.apihelper.ApiException, RequestException) as e:

            bot.stop_polling()

            time.sleep(15)

