from datetime import datetime, timedelta
import gspread


"""Авторизация"""
sa = gspread.service_account()

sh = sa.open_by_url("https://docs.google.com/spreadsheets/d/1TUfo70EJU-sLdjjmdKjIFyVVwDrmf2FJceUpLXhlu0A/edit?hl=ru#gid=0")

wks = sh.worksheet('students_days')

def get_next_lectures(start_date, d=None):
    """Для расчета ёбаных учебных дней"""
    try:
        start_date = datetime.strptime(start_date, "%d.%m.%Y")
    except:
        return 'Некорректный формат даты!'
    
    if start_date.weekday() not in [0, 2, 4]:
        return "Выбранная дата не является понедельником, средой или пятницей."

    lectures = []

    for _ in range(12 if not d else 12 + d):
        while start_date.weekday() not in [0, 2, 4]:
            start_date += timedelta(days=1)
        lectures.append(start_date.strftime("%d.%m.%Y"))
        start_date += timedelta(days=2)

    return lectures


def read_s():
    students = wks.get("A2:R50")
    return students


def write_s(lst:list):
    if isinstance(lst, list):
        wks.update("A2:R50", lst)
        return "Данные записаны"
    else:
        return "Ошибка записи данных"


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

"student1 name: 12.12.2023, student2 name: 13.12.2023"

def add_students(text):
    texts_lst = text.split(',')
    students = read_s()
    try:
        for student_info in texts_lst:
            student_name = student_info.split(':')[0].strip()
            student_l_dates = get_next_lectures(student_info.split(':')[1].strip())
            if isinstance(student_l_dates,list):
                students[find_sublist_with_length_one(students)] = students[find_sublist_with_length_one(students)] + [student_name] + student_l_dates
            else:
                raise
        # print(students)
        write_s(students)
        return "Данные успешно записаны"
    except Exception as ex:
        print(ex)
        return "Ошибка записи данных"
    


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

    
