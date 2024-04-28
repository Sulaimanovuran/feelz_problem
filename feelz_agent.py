import telebot
from requests.exceptions import RequestException
import requests
from buttons_db.db_operations import CreateMenu

from new_utils import *

bot = telebot.TeleBot("7127670654:AAHmAaHtwZRicQ9ZpalygPZKqShFEqxEiX4")
cm = CreateMenu()

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 
                     "Добро пожаловать\nДанные созранены в [таблице](https://docs.google.com/spreadsheets/d/1hE0xs25iBil169bLxH8jvIimvUgOKruQojNg5lXGfhI/edit#gid=237711070)",
                      reply_markup= cm.create_menu('main'), parse_mode='Markdown')

################### BUTTONS HANDLING #############################

# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     if call.data == 'main':
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Что делаем?", reply_markup= cm.create_menu('main'))

#     if call.data == 'new_student':
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="New Student", reply_markup= cm.create_menu('new_student'))

#     if call.data == 'payment':
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Payment", reply_markup= cm.create_menu('payment'))

#     if call.data == 'pay':
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Pay", reply_markup= cm.create_menu('pay'))

#     if call.data == 'cold':
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Cold", reply_markup= cm.create_menu('cold'))


# Словарь для отслеживания состояний пользователей
user_states = {}

# Словарь для выбора типа абонемента
visit_types = {"mwf": "Понедельник • Среда • Пятница", "tts": "Вторник • Четверг • Суббота", "ed":"Каждый день, с Понедельника по Субботу"}

# Словари для сохранения данных, 
    # действие: Добавление ученика
add_student_answers = {}

    # действие: Заморозка
freez_answers = {}

    # действие: Массовая заморозка
bulk_freeze_answers = {}

    # действие: Оплата
payment_answers = {}



# Отлавливает callback значения кнопок и запускает соответствующую логику
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global add_student_answers, freez_answers, bulk_freeze_answers, payment_answers, user_states

    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == 'main':
        """Отображаем главное меню"""

        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Что делаем?", reply_markup=cm.create_menu('main'))

    
    ############### Добавление ученка #######################
    elif call.data == 'new_student':
        """Отображаем меню выбора типа посещений"""

        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Выберите тип посещений:", reply_markup=cm.create_menu('new_student'))

    elif call.data in ('mwf', 'tts', 'ed'):
        """После выбора типа посещений запрашиваем ввод имени.
           После введения имени текст будет выловлен соответствующей функцией,
           в зависимости от состояния user_states"""
        
        # Очищаем user_states чтобы данные не были отловлены другими обработчиками
        user_states = {}
        
        bot.send_message(chat_id=chat_id, text=f"Вы выбрали тип абонемента: {visit_types[call.data]}\nВведите имя ученика")
        user_states[chat_id] = 'waiting_for_name_add_student'
        add_student_answers['subscription_type'] = call.data

    
    ################ Оплата и продление абонемента #####################
    elif call.data == 'payment':
        """Запрашиваем имя ученика"""

        # Очищаем user_states чтобы данные не были отловлены другими обработчиками
        user_states = {}

        bot.send_message(chat_id=chat_id, text="Введите имя ученика")
        user_states[chat_id] = 'waiting_for_name_student_payment'

    elif call.data == 'continue':
        """Продлеваем абонемент ученика"""

        # TODO: Отправить данные payment_answers на сервер для создания нового абонемента ученику
        # TODO: Взять последний день последнего абонемента и передать функции get_lectures добавив аттрибут d=1 и взять последние 12 занятий
        # TODO: Отправить данные о новом расписании на сервер для создания нового абонемента
        # TODO: В случае успешного создания отправить в чат сообщение о новом расписании
        ...

    elif call.data == 'new_date':
        """Продлеваем абонемент ученика с новой даты"""

        # TODO: 
        bot.send_message(chat_id=chat_id, text="Введите новую дату начала обучения")
        user_states[chat_id] = 'waiting_for_new_date_student_payment'


      ################ Заморозка #####################
    elif call.data == 'freeze':
        """При заморозке данных отправляем запрос в БД на получение оставшихся занятий ученика"""

        # TODO: Отправить запрос в БД для получения списка занятий ученика
    



##################### Обработчики текстовых сообщений для добавления ученика
##################### ------------------------------------------------------
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_name_add_student')
def handle_name(message):
    global add_student_answers, user_states
    chat_id = message.chat.id
    user_name = message.text
    
    user_states[chat_id] = 'waiting_for_start_date_add_student'
    add_student_answers['name'] = user_name
    # TODO: Сделать валидацию имени, отправлять запрос в БД и 
    # TODO: сохранять имя только в случае если в БД нет такого же имени

    # Здесь запрашиваем дату начала обучения и переходим к следующему шагу
    bot.send_message(chat_id=chat_id, text=f"Вы ввели имя: {user_name}\nВведите дату начала обучения")


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_start_date_add_student')
def handle_date(message):
    global add_student_answers, user_states
    chat_id = message.chat.id
    start_date = message.text
    
    add_student_answers['start_date'] = start_date

    # Валидация даты
    message = get_next_lectures(add_student_answers['start_date'], add_student_answers['subscription_type'])

    if isinstance(message, list):
        user_states = {}
        message = str(message) + '\nУченик успешно добавлен' #TODO: Отправить POST запрос на создание нового ученика
        bot.send_message(chat_id=chat_id, text=message)
        bot.send_message(chat_id=chat_id, text="Выберите действие", reply_markup=cm.create_menu('main'))
    else:
        bot.send_message(chat_id=chat_id, text=message)



##################### Обработчики текстовых сообщений для добавления оплаты ученику
##################### -------------------------------------------------------------
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_name_student_payment')
def handle_name_payment(message):
    global payment_answers, user_states
    chat_id = message.chat.id
    user_name = message.text
    # TODO: Сделать валидацию имени
    # TODO: получить данные о студенте (его id, тип абонемента, дат его последнего абонемента если есть) и сохранить в payment_answers

    payment_answers['name'] = user_name
    
    # Создается меню payment а их callback будут обработаны функцией callback_inline в блоке "Оплата и продление абонемента"
    bot.send_message(chat_id=chat_id, text=f"Вы ввели имя: {user_name}\nВыберите действие", reply_markup=cm.create_menu('payment'))


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_new_date_student_payment')
def handle_new_date_payment(message):
    global payment_answers, user_states
    chat_id = message.chat.id
    new_date = message.text
    # Валидация даты
    message = get_next_lectures(new_date, 'mwf') # TODO: Вместо mwf использовать payment_answers['subscription_type']

    if isinstance(message, list):
        user_states = {}
        payment_answers['new_subscription'] = message
        formatted_dates = '\n'.join([f"{date}" for date in message])
        message = f"```\n{formatted_dates}\n```\nНовое расписание"  #TODO: Отправить POST запрос на создание нового абонемент и получения отформатированного сообщения
        
        bot.send_message(chat_id=chat_id, text=message,parse_mode="Markdown")
        bot.send_message(chat_id=chat_id, text="Выберите действие", reply_markup=cm.create_menu('main'))
    else:
        bot.send_message(chat_id=chat_id, text=message)





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
