# Django imports
from django.db import transaction
# Engine imports
from .models import MaxTemperature, MinTemperature, Rainfall
from base.decorators import run_in_thread


def create_record(caller, region, data, type):
    """Create record entries from data as per type. """
    try:
        if type == "Tmax":
            parse_tmax_record(region, data, type)
        elif type == "Tmin":
            parse_tmin_record(region, data, type)
        elif type == "Rainfall":
            parse_rainfall_record(region, data, type)
        else:
            return False
        return True
    except Exception as exc:
        raise exc


@run_in_thread
@transaction.atomic
def parse_tmax_record(region, data, type):
    """Parse throught the data given and add record entry. """
    try:
        for record in data:
            MaxTemperature.objects.add_or_update_record(record["value"], region, record["month"], record["year"])
    except Exception as exc:
        raise exc


@run_in_thread
@transaction.atomic
def parse_tmin_record(region, data, type):
    """Parse throught the data given and add record entry. """
    try:
        for record in data:
            MinTemperature.objects.add_or_update_record(record["value"], region, record["month"], record["year"])
    except Exception as exc:
        raise exc


@run_in_thread
@transaction.atomic
def parse_rainfall_record(region, data, type):
    """Parse throught the data given and add record entry. """
    try:
        for record in data:
            Rainfall.objects.add_or_update_record(record["value"], region, record["month"], record["year"])
    except Exception as exc:
        raise exc