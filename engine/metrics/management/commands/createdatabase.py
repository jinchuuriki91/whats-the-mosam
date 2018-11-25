# Python imports
import requests
from requests.exceptions import RequestException

# Django imports
from django.core.management.base import BaseCommand
from django.utils import timezone

# Engine imports
from metrics.constants import REGION_INT


class Command(BaseCommand):
    help = "Fetches data from the S3 urls and writes it to database via the API"
    base_url = "https://s3.eu-west-2.amazonaws.com/interview-question-data/metoffice"
    host = "localhost:8000"

    def add_arguments(self, parser):
        parser.add_argument('-H', '--HOST', type=str, help='Endpoint domain')
    
    def handle(self, *args, **kwargs):
        host = kwargs["HOST"]
        if not host:
            host = "http://%s" % self.host
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s (%s)" % (time, host))

        for location in REGION_INT.keys():
            self.stdout.write("Location: %s, creating Tmax records ..." % location)
            # Create MaxTemperature records
            try:
                url = "%s/Tmax-%s.json" % (self.base_url, location)
                try:
                    resp = requests.get(url)
                    resp.raise_for_status()
                    resp_json = resp.json()
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
                    body = {"type": "Rainfall", "location": location, "data": resp_json}
                    requests.post("%s/api/v1/metric/" % host, json=body)
                except RequestException as exc:
                    raise exc
            except Exception as exc:
                self.stderr.write(exc.__str__())