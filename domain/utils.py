from datetime import datetime, timedelta


def calc_current_start_end_date_week(current_time_unix: int) -> (str, str):
    dt = datetime.fromtimestamp(current_time_unix)
    start_of_week = dt - timedelta(days=dt.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week.date().strftime("%Y-%m-%d"), end_of_week.date().strftime("%Y-%m-%d")


def calc_start_end_date_week(date: datetime) -> (str, str):
    start_of_week = date - timedelta(days=date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week.strftime("%Y-%m-%d"), end_of_week.strftime("%Y-%m-%d")
