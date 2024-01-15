from datetime import datetime, timedelta
import gspread
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


"""Авторизация"""
sa = gspread.service_account()

sh = sa.open_by_url("https://docs.google.com/spreadsheets/d/1TUfo70EJU-sLdjjmdKjIFyVVwDrmf2FJceUpLXhlu0A/edit?hl=ru#gid=0")

wks = sh.worksheet('even')
wks2 = sh.worksheet('odd')
wks3 = sh.worksheet('every_day')

sheet_pages = {'mwf': wks, 'tts': wks2, 'ed': wks3}


""" Расчет дат обучения """
def get_next_lectures(start_date, format=None, d=None):
    try:
        start_date = datetime.strptime(start_date, "%d.%m.%Y")
    except:
        return 'Некорректный формат даты!'
    
    if format == 'mwf':
        if start_date.weekday() not in [0, 2, 4]:
            return "Выбранная дата не является понедельником, средой или пятницей."
        
        lectures = []
        for _ in range(12 if not d else 12 + d):
            while start_date.weekday() not in [0, 2, 4]:
                start_date += timedelta(days=1)
            lectures.append(start_date.strftime("%d.%m.%Y"))
            start_date += timedelta(days=2)


    if format == 'tts':
        if start_date.weekday() not in [1, 3, 5]:
            return "Выбранная дата не является вторником, четвергом или субботой."
        
        lectures = []
        for _ in range(12 if not d else 12 + d):
            while start_date.weekday() not in [1, 3, 5]:
                start_date += timedelta(days=1)
            lectures.append(start_date.strftime("%d.%m.%Y"))
            start_date += timedelta(days=2)


    if format == 'ed':
        if start_date.weekday() not in [0, 1, 2, 3, 4]:
            return "Выбранная дата является воскресеньем."
        
        lectures = []
        for _ in range(20 if not d else 20 + d):
            while start_date.weekday() not in [0, 1, 2, 3, 4]:
                start_date += timedelta(days=1)
            lectures.append(start_date.strftime("%d.%m.%Y"))
            start_date += timedelta(days=1)

    return lectures




def read_s(wks):
    students = wks.get("A3:BI53")
    return students


def write_s(wks, lst:list):
    try:
        if isinstance(lst, list):
            wks.update("A3:BI53", lst)
            return "Данные успешно записаны"
        else:
            return "Неверный формат данных"
    except Exception as ex:
        return f"Ошибка записи данных\nInfo2: {ex}"


def find_sublist_with_length_one(lst):
    for i, sublist in enumerate(lst):
        if len(sublist) == 1:
            return i
    return None



def find_sublist_by_first_element(lst, target_value):
    for i, sublist in enumerate(lst):
        if len(sublist) > 0 and sublist[0] == target_value:
            return i
    return None  # Возвращаем None, если подходящий подсписок не найден


def edit_s(pk, char, value):
    data = read_s()
    student_id = find_sublist_by_first_element(data, pk)
    if char == 'name':
        data[student_id][1] = value

    elif char == 'start_date':
        data[student_id] = data[student_id][:2] + get_next_lectures(value)
        # print(data[student_id][:3] + get_next_lectures(value))
    elif char == 'rescheduled':
        data[student_id] = data[student_id][:2] + get_next_lectures(data[student_id][2], int(value))

    write_s(data)

    return "Данные успешно записаны"


##################### Add Student ########################
def add_students(student_data):
    try:
        students = read_s(sheet_pages[student_data[0]])
        lectures = get_next_lectures(student_data[-1], student_data[0])
        # print(lectures)
        students.append([student_data[1]] + lectures)
        write_s(sheet_pages[student_data[0]], students)
        message = f'<b>{student_data[1]}</b><ul>'
        for i in lectures:
            message+=f'<li>{i}</li>'
        message+='</ul>'
        return message
    
    except TypeError: 
        return lectures

    except Exception as ex:
        print(ex)
        return f"Ошибка записи данных\nInfo:{ex}"
    


def days_until_date(input_date_str):

    input_date = datetime.strptime(input_date_str, "%d.%m.%Y")

    current_date = datetime.now()

    delta = input_date - current_date

    if delta.days < 30 and delta.days > 0:
        return delta.days + 1
    else:
        return None


def rabbits_hunt():
    students = read_s()
    rabbits = 'Ученики у которых скоро закончится абонемент или что у вас там:\n'
    for student in students:
        if len(student) > 1:
            if days_until_date(student[-1]):
                rabbits+=f"{student[0]}. {student[1]}: конец: {student[-1]} – дней: {days_until_date(student[-1])}\n"
        else:
            continue
    
    return rabbits

    
