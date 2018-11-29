# Django imports
from django.utils import timezone


def check_date_format(date_str):
    """Given a string, check if it matches the format. """
    try:
        return timezone.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")