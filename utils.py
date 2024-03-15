from datetime import datetime, timedelta
import gspread


"""Авторизация"""
sa = gspread.service_account()

sh = sa.open_by_url("https://docs.google.com/spreadsheets/d/1TUfo70EJU-sLdjjmdKjIFyVVwDrmf2FJceUpLXhlu0A/edit?hl=ru#gid=0")

wks = sh.worksheet('even')
wks2 = sh.worksheet('odd')
wks3 = sh.worksheet('every_day')
wks_pay = sh.worksheet('Payment')

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

# print(get_next_lectures('01.01.2024', 'ed'))


def read_s(wks):
    students = wks.get("A3:BI103")
    return students


def write_s(wks, lst:list, ue=None):
    try:
        if isinstance(lst, list):
            if ue:
                # wks.batch_clear(['A3:H25'])
                wks.update("B3:BI103", lst)
                return "Данные успешно записаны"
            else:
                wks.update("A3:BI103", lst)
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

def search_student_payment(name):
    students = read_s(wks_pay)
    students_payment = []
    for student in students:
        if name.lower() == student[0].lower():
            student.append('Оплачено')
        students_payment.append(student[1:])
    return students_payment



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
        if isinstance(new_lectures, list) and isinstance(prev_lectures, list):
            students_with_pay = search_student_payment(students[indx][0])
            write_s(sheet_pages[format], students)
            write_s(wks_pay, students_with_pay, True)
    except:
        prev_lectures = None

    return new_lectures, prev_lectures


##################### Freeze ########################
from datetime import datetime

def filter_dates(format, indx):
    current_date = datetime.now().date()
    formatted_dates = "```\n"
    student = read_s(sheet_pages[format])[indx]

    last_subscription = student[-12:] if format in ['mwf', 'tts'] else student[1:]

    for number, date_str in enumerate(last_subscription, start=1):
        try:
            date_obj = datetime.strptime(date_str, '%d.%m.%Y').date()
            if date_obj >= current_date and number == len(last_subscription):
                formatted_dates+=f'    {number})  {date_str}'+'```'
            elif date_obj >= current_date:
                formatted_dates+=f'    {number})  {date_str}'+'\n'
        except ValueError:
            return f"Ошибка в формате даты: {date_str}"

    return formatted_dates


def freezing(lectures, days, format):
    indexes = list(map(int, days.split(',')))
    m = len(days)
    n = len(lectures)
    check = False
    if format == 'mwf':
        ras = [0, 2, 4]
    elif format == 'tts':
        ras = [1, 3, 5]
    else:
        ras = [0, 1, 2, 3, 4]
        check = True
    start_date = datetime.strptime(lectures[-1],'%d.%m.%Y') + timedelta(days=2 - check)
    for _ in range(m):
        while start_date.weekday() not in ras:
            start_date += timedelta(days=1)
        lectures.append(start_date.strftime("%d.%m.%Y"))
        start_date += timedelta(days=2 - check)
    result = []
    for idx, val in enumerate(lectures):
        if idx + 1 in indexes:
            continue
        result.append(val)

    if format in ['mwf','tts']:
        return result[:12]
    else:
        return result[:20]


def freeze_student(format, indx, numbers):
    try:
        numbers = numbers.strip()
        int(numbers[0])
        int(numbers[-1])
    except:
        return "Некоректный формат данных"
    students = read_s(sheet_pages[format])
    if format == 'ed':
        freezing_student = freezing(students[indx][-20:], numbers, format)
        students[indx][-20:] = freezing_student
    elif format in ['mwf', 'tts']:
        freezing_student = freezing(students[indx][-12:], numbers, format)
        students[indx][-12:] = freezing_student
    try:
        write_s(sheet_pages[format], students)
    except:
        return "Ошибка заморозки"
    return freezing_student
    









# lectures2 = ['01.01.2024', '02.01.2024', '03.01.2024', '04.01.2024', '05.01.2024', '08.01.2024', '09.01.2024', '10.01.2024', '11.01.2024', '12.01.2024', '15.01.2024', '16.01.2024', '17.01.2024', '18.01.2024', '19.01.2024', '22.01.2024', '23.01.2024', '24.01.2024', '25.01.2024', '26.01.2024']


# print(filter_dates('ed', 2))



'''
если action == 'continue' вызываем функцию get_next_lectures(date, format, 1)[1:]

если action == 'new_date' вызываем функцию get_next_lectures(date, format)
'''

['17.01.2024', '19.01.2024', '22.01.2024', '24.01.2024', '26.01.2024', '29.01.2024', '31.01.2024', '02.02.2024', '05.02.2024', '07.02.2024', '09.02.2024']