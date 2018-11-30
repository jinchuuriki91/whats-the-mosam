# Python imports
import requests
import json
from time import sleep
from requests.exceptions import RequestException

# Django imports
from django.core.management.base import BaseCommand
from django.utils import timezone

# Engine imports
from metrics.constants import REGION_INT
from metrics.models import MaxTemperature, MinTemperature, Rainfall


class Command(BaseCommand):
    help = "Fetches data from the S3 urls and writes it to database via the API"
    base_url = "https://s3.eu-west-2.amazonaws.com/interview-question-data/metoffice"
    host = "localhost:8000"

    def add_arguments(self, parser):
        parser.add_argument('-H', '--HOST', type=str, help='Endpoint domain')
    
    def handle(self, *args, **kwargs):
        host = kwargs["HOST"]
        metoffice_data = {}
        if not host:
            host = "http://%s" % self.host
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s (%s)" % (time, host))

        for location in REGION_INT.keys():
            metoffice_data[location] = {}
            self.stdout.write("Location: %s, creating Tmax records ..." % location)
            # Create MaxTemperature records
            try:
                url = "%s/Tmax-%s.json" % (self.base_url, location)
                try:
                    resp = requests.get(url)
                    resp.raise_for_status()
                    resp_json = resp.json()
                    metoffice_data[location]["tmax"] = resp_json
                    body = {"type": "Tmax", "location": location, "data": resp_json}
                    requests.post("%s/api/v1/metric/" % host, json=body)
                except RequestException as exc:
                    raise exc
            except Exception as exc:
                self.stderr.write(exc.__str__())
            
            self.stdout.write("Location: %s, creating Tmin records ..." % location)
            # Create MinTemperature records
            try:
                url = "%s/Tmin-%s.json" % (self.base_url, location)
                try:
                    resp = requests.get(url)
                    resp.raise_for_status()
                    resp_json = resp.json()
                    metoffice_data[location]["tmin"] = resp_json
                    body = {"type": "Tmin", "location": location, "data": resp_json}
                    requests.post("%s/api/v1/metric/" % host, json=body)
                except RequestException as exc:
                    raise exc
            except Exception as exc:
                self.stderr.write(exc.__str__())

            self.stdout.write("Location: %s, creating Rainfall records ..." % location)
            # Create Rainfall records
            try:
                url = "%s/Rainfall-%s.json" % (self.base_url, location)
                try:
                    resp = requests.get(url)
                    resp.raise_for_status()
                    resp_json = resp.json()
                    metoffice_data[location]["rainfall"] = resp_json
                    body = {"type": "Rainfall", "location": location, "data": resp_json}
                    requests.post("%s/api/v1/metric/" % host, json=body)
                except RequestException as exc:
                    raise exc
            except Exception as exc:
                self.stderr.write(exc.__str__())

        self.stdout.write("Sleeping for 10 sec ...")
        sleep(10)
        # Now check if the data written is same as from S3 urls
        for location in REGION_INT.keys():
            # check if all Tmax records are written
            for metric in metoffice_data[location]["tmax"]:
                kwargs = {
                    "value": metric["value"],
                    "region": REGION_INT[location],
                    "record_date__year": metric["year"],
                    "record_date__month": metric["month"]
                }
                exists = MaxTemperature.objects.filter(**kwargs).exists()
                if not exists:
                    self.stderr.write("Following metric doesn't exist: %s" % json.dumps(metric))
            self.stdout.write("Done checking MaxTemperature for %s." % location)

            # check if all Tmin records are written
            for metric in metoffice_data[location]["tmin"]:
                kwargs = {
                    "value": metric["value"],
                    "region": REGION_INT[location],
                    "record_date__year": metric["year"],
                    "record_date__month": metric["month"]
                }
                exists = MinTemperature.objects.filter(**kwargs).exists()
                if not exists:
                    self.stderr.write("Following metric doesn't exist: %s" % json.dumps(metric))
            self.stdout.write("Done checking MinTemperature for %s." % location)

            # check if all Rainfall records are written
            for metric in metoffice_data[location]["rainfall"]:
                kwargs = {
                    "value": metric["value"],
                    "region": REGION_INT[location],
                    "record_date__year": metric["year"],
                    "record_date__month": metric["month"]
                }
                exists = Rainfall.objects.filter(**kwargs).exists()
                if not exists:
                    self.stderr.write("Following metric doesn't exist: %s" % json.dumps(metric))
            self.stdout.write("Done checking Rainfall for %s." % location)