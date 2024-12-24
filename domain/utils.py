from datetime import datetime


def date_unix(date: datetime) -> int:
    return int((date - datetime(1970, 1, 1, tzinfo=date.tzinfo)).total_seconds())


def calc_current_index_week(current_time_unix: int) -> int:
    # 1703451600 - дата нулевой недели
    # 604800 - 7 дней
    current_index_link = (current_time_unix - 1703451600) // 604800
    return current_index_link
