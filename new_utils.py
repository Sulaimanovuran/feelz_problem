from datetime import datetime, timedelta


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