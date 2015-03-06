from datetime import datetime

def get_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()