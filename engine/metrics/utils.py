# Django imports
from django.db import transaction
from django.utils import timezone

# Engine imports
from .models import MaxTemperature, MinTemperature, Rainfall
from base.decorators import run_in_thread
from base.utils import check_date_format
from base.exceptions import BadDataException
from .serializers import MaxTempSerializer, MinTempSerializer, RainfallSerializer


def get_records(caller, region, type, start_date="", end_date=""):
    """Get records based on type and region. """
    try:
        start_dt = None
        end_dt = None

        if start_date:
            try:
                start_dt = check_date_format(start_date)
            except Exception:
                raise BadDataException("Invalid start date format")

        if end_date:
            try:
                end_dt = check_date_format(end_date)
            except Exception:
                raise BadDataException("Invalid end date format")
        if start_dt and end_dt and start_dt > end_dt:
            raise BadDataException("Start date can't be greater than end date")
        
        kwargs = {"region": region, "is_active": True}
        if start_dt:
            kwargs.update({"record_date__gte": start_dt})
        if end_dt:
            kwargs.update({"record_date__lte": end_dt})

        if type == "Tmax":
            return MaxTempSerializer(MaxTemperature.objects.filter(**kwargs), many=True).data
        elif type == "Tmin":
            return MinTempSerializer(MinTemperature.objects.filter(**kwargs), many=True).data
        elif type == "Rainfall":
            return RainfallSerializer(Rainfall.objects.filter(**kwargs), many=True).data
        else:
            return [] 
    except Exception as exc:
        raise exc


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