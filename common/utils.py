from datetime import datetime


def human_week_day(week_day_index: int) -> str:
    return {
        0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье",
    }[week_day_index]


def human_date(date: datetime) -> str:
    return date.strftime("%d.%m.%Y")


def bytes_str_to_str(bytes_str: str) -> str:
    # "b'\\xd0\\x9f\\xd1\\x80\\xd0\\xb8\\xd0\\xb2\\xd0\\xb5\\xd1\\x82'" -> "Привет"
    return bytes_str.encode('utf-8').decode('unicode_escape').encode('latin1').decode('utf-8')
