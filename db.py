import os
import sqlite3
from telebot import types

class CreateMenu:
    def __init__(self):
        '''Конструктор класса. Определяет файл базы данных'''
        self.__db_path = os.getcwd()
        self.db_name = os.path.join(self.__db_path, 'database.db')


    def __connect(self):
        '''Функция подключения к базе данных'''
        connect = sqlite3.connect(self.db_name)
        return connect


    def __select_button(self, type_menu: str) -> dict:
        '''В качестве аргумента принимает "тип меню". Возвращает словарь где ключ = текст кнопки, значение = callbackdata кнопки'''
        with self.__connect() as connect:
            cursor = connect.cursor()
            sql = """SELECT btn_name, btn_callback FROM create_menu WHERE type_menu = (?) ORDER BY order_num"""
            select_db = cursor.execute(sql, (type_menu,))
            result = dict()
            for btn_name, btn_callback in select_db.fetchall():
                result[btn_name] = btn_callback
            return result
    

    def create_menu(self, type_menu: str) -> types.InlineKeyboardMarkup:
        '''Создаём меню для TG бота'''
        markup = types.InlineKeyboardMarkup()
        btn_list = self.__select_button(type_menu)
        for element in btn_list.items():
            btn = types.InlineKeyboardButton(text= element[0], callback_data= element[1])
            markup.add(btn)
        return markup