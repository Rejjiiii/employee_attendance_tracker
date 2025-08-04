from datetime import datetime

VALID_STATUSES = ["Present", "Absent", "Late"]


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_valid_status(status_str):
    return status_str.capitalize() in VALID_STATUSES
