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



##################### Add Student ########################
def add_students(student_data):
    try:
        students = read_s(sheet_pages[student_data[0]])
        lectures = get_next_lectures(student_data[-1], student_data[0])
        # print(lectures)
        students.append([student_data[1]] + lectures)
        return write_s(sheet_pages[student_data[0]], students), lectures
    
    except TypeError: 
        return lectures

    except Exception as ex:
        print(ex)
        return f"Ошибка записи данных\nInfo:{ex}"
    

##################### Find Rabbit Student ########################

def days_until_date(input_date_str):
    input_date = datetime.strptime(input_date_str, "%d.%m.%Y")
    current_date = datetime.now()
    delta = input_date - current_date
    if delta.days < 3 and delta.days > 0:
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


##################### Search Student ########################
def search_student(name):
    for wks_name, page_data in zip(['mwf', 'tts', 'ed'], [wks, wks2, wks3]):
        for indx, sublist in enumerate(read_s(page_data)):
            if sublist[0].lower() == name.lower():
                return wks_name, sublist, indx
            else:
                continue
    return None


##################### Payment ########################
def next_subscription(format, indx, action, date=None):
    students = read_s(sheet_pages[format])
    new_lectures = []
    prev_lectures = []

    if action == 'continue':
        new_lectures = get_next_lectures(students[indx][-1], format, 1)[1:]
    elif action == 'new_date' and date:
        new_lectures = get_next_lectures(date, format)
    else:
        return None
    try:
        if format != 'ed':
            prev_lectures = students[indx][-12:]
        elif format == 'ed':
            prev_lectures = students[indx][-20:]
        students[indx] += new_lectures
        write_s(sheet_pages[format], students)
    except:
        prev_lectures = None

    return new_lectures, prev_lectures






'''
если action == 'continue' вызываем функцию get_next_lectures(date, format, 1)[1:]

если action == 'new_date' вызываем функцию get_next_lectures(date, format)
'''