from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def get_next_lectures(start_date, format=None, d=None):
    """Для расчета ёбаных учебных дней"""
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



def create_image():
    # Создание изображения
    absent_days = {'Пн': True, 'Вт': False, 'Ср': True, 'Чт': False, 'Пт': True}
    img = Image.new('RGB', (400, 300), color='white')
    draw = ImageDraw.Draw(img)
    
    # Загрузка красивого шрифта (в данном случае, Montserrat)
    font_path = "/Users/mac/Desktop/code_/free-works/feelz_problem/MontaguSlab-VariableFont_opsz,wght.ttf"
    font_size = 20
    font = ImageFont.truetype(font_path, font_size)

    # Получение размеров изображения
    img_width, img_height = img.size
    
    # Начальные координаты для текста
    x = (img_width - font_size) // 2
    y = 20

    # Добавление информации о днях отсутствия на изображение
    for day, is_absent in absent_days.items():
        status = "Отсутствовал" if is_absent else "Присутствовал"
        text = f"{day}: {status}"

        # Получение размеров текста
        text_bbox = draw.textbbox((x, y), text, font=font)

        # Рассчет координат для центрирования текста
        x = (img_width - text_bbox[2]) // 2

        # Добавление текста на изображение
        draw.text((x, y), text, fill='black', font=font)

        # Увеличение координат для следующей строки
        y += text_bbox[3] + 5

    # Сохранение изображения в байтовом формате с улучшенным качеством
    img_byte_array = BytesIO()
    img.save(img_byte_array, format='PNG', quality=95)
    img_byte_array.seek(0)

    with open('test.png', 'wb') as f:
        f.write(img_byte_array.getvalue())  # использование getvalue()

    return img_byte_array

# create_image()
# print(get_next_lectures('15.01.2024', 'ed'))

from datetime import datetime

def filter_dates(input_dates):
    current_date = datetime.now()
    formatted_dates = []

    for date_str in input_dates:
        try:
            date_obj = datetime.strptime(date_str, '%d.%m.%Y')
            if date_obj <= current_date:
                formatted_dates.append(date_str)
        except ValueError:
            print(f"Ошибка в формате даты: {date_str}")

    return formatted_dates

# Пример использования
input_dates = ['13.01.2024', '15.01.2024', '17.01.2024', '18.01.2024', '19.01.2024', '20.01.2024', '31.01.2024', '02.02.2024', '05.02.2024', '07.02.2024', '09.02.2024']
filtered_dates = filter_dates(input_dates)


f = ['John Snow', '01.01.2024', '03.01.2024', '05.01.2024', '08.01.2024', '10.01.2024', '12.01.2024', '15.01.2024', '17.01.2024', '19.01.2024', '22.01.2024', '24.01.2024', '26.01.2024']


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


dates = ['01.01.2024', '03.01.2024', '05.01.2024', '08.01.2024', '10.01.2024', '12.01.2024', '15.01.2024', '17.01.2024', '19.01.2024', '22.01.2024', '24.01.2024', '26.01.2024']
dates2 = ['01.01.2024', '02.01.2024', '03.01.2024', '04.01.2024', '05.01.2024', '08.01.2024', '09.01.2024', '10.01.2024', '11.01.2024', '12.01.2024', '15.01.2024', '16.01.2024', '17.01.2024', '18.01.2024', '19.01.2024', '22.01.2024', '23.01.2024', '24.01.2024', '25.01.2024', '26.01.2024']
print(freezing(dates2, '9,10', 'ed'))