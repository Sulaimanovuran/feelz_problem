# import telebot
# from telebot import types
# from utils import *


# TOKEN = '6773819389:AAE-OYFbtkhIZDsoC67YTzo1LGRO777MPMc'
# bot = telebot.TeleBot(TOKEN)

# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#     bot.reply_to(message, "Привет! Я бот для учета посещений учеников. Используйте команды /add, /edit и /rabbit_hunt.\nСсылка на вашу таблицу: https://docs.google.com/spreadsheets/d/1TUfo70EJU-sLdjjmdKjIFyVVwDrmf2FJceUpLXhlu0A/edit?hl=ru#gid=0")


# @bot.message_handler(commands=['add'])
# def add_student(message):
#     chat_id = message.chat.id
#     msg = bot.reply_to(message, "Введите имя учеников и даты начала их обучения в формате: student1 name: 12.12.2023, student2 name: 13.12.2023, ...")
#     bot.register_next_step_handler(msg, process_name_step, chat_id)


# def process_name_step(message, chat_id):
#     students = message.text
#     done_message = add_students(students)
#     bot.reply_to(message, f"{done_message}")


# @bot.message_handler(commands=['edit'])
# def edit_student(message):
#     chat_id = message.chat.id
#     msg = bot.reply_to(message, "Слушай сюда пидор\nсначала пишешь мне ID ученика после\nесли нужно изменить имя пиши: id:1, name:need_name\nдату первого занятия: id:1, start_date:13.12.2023\nдобавить доп. занятия: id:1, rescheduled:1 или 2 и нехуй мне тут всякую хуйню писать\nИ за один раз только одно действие а то начнешь мне тут тупить как обычно")
#     bot.register_next_step_handler(msg, process_edit_step, chat_id)


# def process_edit_step(message, chat_id):
#     student_triggers = message.text.split(',')
#     student_id = student_triggers[0].split(':')[1]

#     student_char = student_triggers[1].split(':')[0].strip()
#     student_char_value = student_triggers[1].split(':')[1].strip()

#     done_message = edit_s(student_id, student_char, student_char_value)

#     bot.reply_to(message, f"{done_message}")



# @bot.message_handler(commands=['rabbit_hunt'])
# def rabbit_hunt(message):
    
#     bot.send_message(message.chat.id, rabbits_hunt())


# if __name__ == '__main__':
#     bot.polling(none_stop=True)



# import telebot

# TOKEN = '6773819389:AAE-OYFbtkhIZDsoC67YTzo1LGRO777MPMc'
# bot = telebot.TeleBot(TOKEN)

# # Список вопросов
# questions = ["Как его зовут?", "Сколько ему лет?", "Когда он начинает обучение?"]

# # Список для хранения ответов
# user_answers = []

# @bot.message_handler(commands=['add_student'])
# def start_add_student(message):
#     global user_answers
#     user_answers = []  # Обнуляем список ответов
#     ask_next_question(message.chat.id)

# def ask_next_question(user_id):
#     if len(user_answers) < len(questions):
#         question_text = questions[len(user_answers)]
#         bot.send_message(user_id, question_text)
#     else:
#         process_student_data(user_id)

# @bot.message_handler(func=lambda message: True)
# def handle_user_input(message):
#     global user_answers
#     user_answers.append(message.text)
#     ask_next_question(message.chat.id)

# def process_student_data(user_id):
#     # Здесь вы можете использовать или сохранить ответы из user_answers
#     bot.send_message(user_id, "Спасибо за ответы! Ученик добавлен.")
#     print("Данные ученика:", user_answers)

# if __name__ == "__main__":
#     bot.polling(none_stop=True)

"""Полезные ссылки"""

#https://habr.com/ru/sandbox/163347/
#https://habr.com/ru/sandbox/181424/
#https://habr.com/ru/articles/735394/

#####################

# import sqlite3

# # # Устанавливаем соединение с базой данных
# connection = sqlite3.connect('database.db')
# cursor = connection.cursor()

# # Создаем таблицу create_menu
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS create_menu (
# type_menu TEXT NOT NULL,
# order_num INTEGER,
# btn_name TEXT NOT NULL,
# btn_callback TEXT NOT NULL
# )
# ''')

# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('main', 1, '➕ Новый ученик', 'new_student')),
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('main', 2, "💸 Оплата", 'pay')),
# # cursor.execute('UPDATE create_menu SET age = ? WHERE username = ?', (29, 'newuser'))

# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('main', 3, "🥶 Зоморозка", 'cold')),
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('main', 3, "❄️ Массовая зоморозка", 'mass_freeze')),
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('new_student', 1, "Пн • Ср • Пт", 'mwf')),
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('new_student', 2, "Вт • Чт • Сб", 'tts')),
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('new_student', 3, "Пн ••• Пт", 'ed')),
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('new_student', 4, "🔙 Назад", 'back')),
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('pay',1, '◀️ Предыдущий абонемент', "previous")),
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('pay', 2, '🔙 Назад',  'back'))
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('cold', 1,  '🌬 Заморозить', 'freeze'))
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('cold', 2,  '🔙 Назад', 'main'))

# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('payment', 1,  '⏭ Продолжить', 'continue'))
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('payment', 2,  '🆕 Новая дата', 'new_date'))
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('payment', 3,  '🔙 Назад', 'back'))



# # # Сохраняем изменения и закрываем соединени
# connection.commit()
# connection.close()

# # #•.,:;…!?·