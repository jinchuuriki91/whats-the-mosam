# Python imports
import requests

# Django imports
from django.test import TestCase

# Engine imports
from metrics.constants import REGION_INT


class APITestCase(TestCase):
    url = "http://localhost:8000/api/v1/metric/"
    metric_type = "Rainfall"
    location = "England"

    def test_post(self):
        try:
            url = "https://s3.eu-west-2.amazonaws.com/interview-question-data/metoffice/%s-%s.json" % (self.metric_type, self.location)
            resp = requests.get(url)
            resp.raise_for_status()
            data = resp.json()
            body = {"type": self.metric_type, "location": self.location, "data": data}
            resp = requests.post(self.url, json=body)
            self.assertEqual(resp.status_code, 201)
        except Exception as exc:
            raise exc

    def test_get(self):
        try:
            params = {
                "start_date": "1991-06-04",
                "end_date": "2015-06-04",
                "type": self.metric_type,
                "location": self.location
            }
            resp = requests.get(self.url, params=params)
            self.assertEqual(resp.status_code, 200)
            resp_json = resp.json()
            self.assertIn("count", resp_json.keys())
            self.assertIn("results", resp_json.keys())
            self.assertIsInstance(resp_json["results"], list)
        except Exception as exc:
            raise exc