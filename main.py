import telebot
from telebot import types
from utils import *


TOKEN = '6773819389:AAE-OYFbtkhIZDsoC67YTzo1LGRO777MPMc'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для учета посещений учеников. Используйте команды /add, /edit и /rabbit_hunt.\nСсылка на вашу таблицу: https://docs.google.com/spreadsheets/d/1TUfo70EJU-sLdjjmdKjIFyVVwDrmf2FJceUpLXhlu0A/edit?hl=ru#gid=0")


@bot.message_handler(commands=['add'])
def add_student(message):
    chat_id = message.chat.id
    msg = bot.reply_to(message, "Введите имя учеников и даты начала их обучения в формате <student1 name: 12.12.2023, student2 name: 13.12.2023, ...>")
    bot.register_next_step_handler(msg, process_name_step, chat_id)


def process_name_step(message, chat_id):
    students = message.text
    done_message = add_students(students)
    bot.reply_to(message, f"{done_message}")


@bot.message_handler(commands=['edit'])
def edit_student(message):
    chat_id = message.chat.id
    msg = bot.reply_to(message, "Слушай сюда пидор\nсначала пишешь мне ID ученика после\nесли нужно изменить имя пиши: <id:1, name:need_name>\nдату первого занятия: <id:1, start_date:13.12.2023>\nдобавить доп. занятия: <id:1, rescheduled:1 или 2 и нехуй мне тут всякую хуйню писать>\nИ за один раз только одно действие а то начнешь мне тут тупить как обычно")
    bot.register_next_step_handler(msg, process_edit_step, chat_id)


def process_edit_step(message, chat_id):
    student_triggers = message.text.split(',')
    student_id = student_triggers[0].split(':')[1]

    student_char = student_triggers[1].split(':')[0].strip()
    student_char_value = student_triggers[1].split(':')[1].strip()

    done_message = edit_s(student_id, student_char, student_char_value)

    bot.reply_to(message, f"{done_message}")



@bot.message_handler(commands=['rabbit_hunt'])
def rabbit_hunt(message):
    
    bot.send_message(message.chat.id, rabbits_hunt())


if __name__ == '__main__':
    bot.polling(none_stop=True)