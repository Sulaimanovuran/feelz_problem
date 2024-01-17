import telebot
from requests.exceptions import RequestException
import time
from db import CreateMenu

from utils import *

bot = telebot.TeleBot("6773819389:AAE-OYFbtkhIZDsoC67YTzo1LGRO777MPMc")
cm = CreateMenu()

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать", reply_markup= cm.create_menu('main'))




################## ADD STUDENT ########################
questions = ["Введите Ф.И. ученика", "Введите дату начала обучения"]
user_answers = []
pay_flag = False
add_flag = False
new_date_flag = False
freeze_flag = False

def start_add_student(message, format, again=None):
    global user_answers
    user_answers = [format]
    if add_flag:
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
    if add_flag:
        user_answers.append(message.text)
        ask_next_question(message.chat.id)
    elif pay_flag:
        username.append(message.text)
        ask_next_question_pay(message.chat.id)
    elif new_date_flag:
        new_date.append(message.text)
        ask_next_question_new_date(message.chat.id)
    elif freeze_flag:
        freeze_answers.append(message.text)
        ask_next_question_freeze(message.chat.id)


def process_student_data(user_id):
    student_validated_data = add_students(user_answers)
    if len(student_validated_data) > 1 and 'успешно' in student_validated_data[0]: 
        lectures = student_validated_data[1]
        """Создание сообщения с датами"""
        message = f'Ученик *{user_answers[1]}* добавлен\nВот его расписание:\n```'
        for num, date in enumerate(lectures, start=1):
            if num != len(lectures):
                message+=f'   {num}) {date}\n'
            else:
                message+=f'   {num}) {date}```'

        bot.send_photo(user_id, photo=open('1.png', 'rb'), caption=message, parse_mode='Markdown')
        bot.send_message(user_id, text="Что делаем?", reply_markup= cm.create_menu('main'))
    else:
        bot.send_message(user_id, student_validated_data)
        start_add_student(user_id, user_answers[0], 'again')


################## ADD STUDENT PAYMENT ########################        
question = ['Введите Ф.И. ученика']
username = []
def start_add_student_payment(message):
    global username
    username = []
    if pay_flag:
        ask_next_question_pay(message.chat.id)
    
def ask_next_question_pay(user_id):
    if len(username) < len(question):
        question_text = question[len(username)]
        bot.send_message(user_id, question_text)
    else:
        process_student_data_pay(user_id)

search_results = []
lectures = []
def process_student_data_pay(user_id):
    global search_results
    if username:
        search_results = search_student(username[0])
        if search_results:
            bot.send_message(user_id, text=f'Ученик __*{username[0]}*__ найден.\nВыберите действие', reply_markup=cm.create_menu('payment'), parse_mode='Markdown')
        else:
            bot.send_message(user_id, text=f'Ученик __*{username[0]}*__  не найден =(', reply_markup=cm.create_menu('main'),parse_mode='Markdown')

################## ADD STUDENT NEW DATE ########################        
new_date_question = ['Введите новую дату']
new_date = []
def start_add_student_new_date(message):
    global new_date
    new_date = []
    if new_date_flag:
        ask_next_question_new_date(message.chat.id)
    
def ask_next_question_new_date(user_id):
    if len(new_date) < len(new_date_question):
        question_text = new_date_question[len(new_date)]
        bot.send_message(user_id, question_text)
    else:
        process_student_data_new_date(user_id)

lectures = []
def process_student_data_new_date(user_id):
    global search_results, lectures
    lectures = next_subscription(search_results[0], search_results[-1], 'new_date', date=new_date[0])
    new_lectures=lectures[0]
    if isinstance(new_lectures, list):
        message = f'У ученика *{username[0]}* обновлено расписание\nВот его новое расписание:\n```'
        for num, date in enumerate(new_lectures, start=1):
            if num != len(new_lectures):
                message+=f'   {num}) {date}\n'
            else:
                message+=f'   {num}) {date}```'
        bot.send_photo(user_id, photo=open('Unknown.png', 'rb'), caption=message, reply_markup=cm.create_menu('pay'), parse_mode='Markdown')
    else:
        bot.send_message(user_id, text=new_lectures, reply_markup=cm.create_menu('main'), parse_mode="Markdown")


################## FREEZE STUDENT ########################        
freeze_question = ['Введите Ф.И. ученика', 'Введите номера уроков через запятую которые хотите заморозить(5,6,7...) ТОЛЬКО ПО ПОРЯДКУ']
freeze_answers = []
def start_freeze_student(message):
    global freeze_answers, search_results
    freeze_answers = []
    if freeze_flag:
        ask_next_question_freeze(message.chat.id)

last_lectures = ''

def ask_next_question_freeze(user_id):
    global last_lectures, search_results
    if len(freeze_answers) < len(freeze_question):
        if len(freeze_answers) == 1:
            search_results = search_student(freeze_answers[0])
            if search_results:
                last_lectures = filter_dates(search_results[0], search_results[-1])
                bot.send_message(user_id, text=f'Оставшиеся занятия ученика:\n{last_lectures}', parse_mode='Markdown')
                question_text = freeze_question[len(freeze_answers)]
                bot.send_message(user_id, question_text)
            else:
                bot.send_message(user_id, text=f'Ученик *{freeze_answers[0]}* не найден', parse_mode='Markdown')
        else:
            question_text = freeze_question[len(freeze_answers)]
            bot.send_message(user_id, question_text)
    else:
        process_student_data_freeze(user_id)

def process_student_data_freeze(user_id):
    message=f'Ученик {freeze_answers[0]}\nЗаморозить уроки №:{freeze_answers[-1]}.\nВсе верно?\n{last_lectures}' 
    bot.send_message(user_id, text=message, reply_markup=cm.create_menu('cold'), parse_mode='Markdown')

################## CALLBACK HANDLER ########################        
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global pay_flag, add_flag, new_date_flag, freeze_flag, lectures
    if call.data == 'new_student':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите формат", reply_markup= cm.create_menu('new_student'))

    if call.data == 'pay':
        pay_flag=True
        add_flag=False
        new_date_flag = False
        start_add_student_payment(call.message)

    if call.data == 'back':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Что делаем?", reply_markup= cm.create_menu('main'))

    if call.data == 'cold':
        pay_flag=False
        add_flag=False
        new_date_flag = False
        freeze_flag = True
        start_freeze_student(call.message)

    """New student"""
    if call.data in ['mwf', 'tts', 'ed']:
        pay_flag=False
        new_date_flag = False
        add_flag=True
        start_add_student(call.message, call.data)

    """Pay"""
    if call.data == 'continue':
        lectures = next_subscription(search_results[0], search_results[-1], call.data)
        new_lectures = lectures[0]
        if isinstance(new_lectures, list):
            message = f'У ученика *{username[0]}* обновлено расписание\nВот его новое расписание:\n```'
            for num, date in enumerate(new_lectures, start=1):
                if num != len(new_lectures):
                    message+=f'   {num}) {date}\n'
                else:
                    message+=f'   {num}) {date}```'
            bot.send_photo(call.message.chat.id, photo=open('2.png', 'rb'), caption=message, reply_markup=cm.create_menu('pay'), parse_mode='Markdown')
            # bot.send_message(call.message.chat.id, text=message, reply_markup=cm.create_menu('pay'), parse_mode="Markdown")
        else:
            bot.send_message(call.message.chat.id, text=lectures[0], reply_markup=cm.create_menu('main'), parse_mode="Markdown")

    if call.data == 'previous':
        message = f'Предыдущее расписание ученика *{username[0]}*\n```'
        if lectures[-1]:
            for num, date in enumerate(lectures[-1], start=1):
                if num != len(lectures[-1]):
                    message+=f'   {num}) {date}\n'
                else:
                    message+=f'   {num}) {date}```'
            bot.send_photo(call.message.chat.id, photo=open('3.png', 'rb'), caption=message, reply_markup=cm.create_menu('main'), parse_mode='Markdown')
        else:
            bot.send_message(call.message.chat.id, text='Нет предыдущих занятий', reply_markup=cm.create_menu('main'))

    if call.data == 'new_date':
        pay_flag=False
        add_flag=False
        new_date_flag = True
        start_add_student_new_date(call.message)
    
    """Freeze"""
    if call.data == 'freeze':
        freeze = freeze_student(search_results[0], search_results[-1], freeze_answers[-1])
        message = f'Новое расписание\n*{freeze_answers[0]}*\n```'
        if isinstance(freeze, list):
            for num, date in enumerate(freeze, start=1):
                if num == len(freeze):
                    message+=f'   {num}) {date}```'
                else:
                    message+=f'   {num}) {date}\n'
                
            bot.send_photo(call.message.chat.id, photo=open('Unknown.png', 'rb'), caption=message, reply_markup=cm.create_menu('main'), parse_mode='Markdown')
        else:
            bot.send_message(call.message.chat.id, text=freeze, reply_markup=cm.create_menu('main'), parse_mode='Markdown')
        


"""Для остановки"""
import signal
import sys

def signal_handler(sig, frame):
    print("Вы нажали Ctrl+C. Завершение работы бота.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Error in main loop: {e}")
