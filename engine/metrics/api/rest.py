# Python imports
from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework.status as rest_status

# Engine imports
from metrics.utils import create_record
from base.exceptions import BadDataException
from metrics.constants import REGION_INT


class MetricsHandler(APIView):

    valid_types = ("Tmax", "Tmin", "Rainfall")

    def get(self, request):
        """Returns weather data. """
        data = request.GET.dict()
        if "type" not in data:
            raise BadDataException("Please provide type of the metric i.e. Tmax, Tmin or Rainfall)")
        if "location" not in data:
            raise BadDataException("Please provide a location")
        return Response({"status": data})

    def post(self, request):
        """Creates weather data. """
        try:
            body = request.data
            metric_type = body.get("type", None)
            location = body.get("location", None)
            if not metric_type or not location:
                raise BadDataException("Please provide metric type and location")
            
            if metric_type not in self.valid_types or location not in REGION_INT.keys():
                raise BadDataException("Please provide metric type and location")
            
            resp = create_record(request.user, REGION_INT[body["location"]], body.get("data", []), metric_type)
            return Response({"status": "success", "result": resp}, status=rest_status.HTTP_201_CREATED)
        except BadDataException as exc:
            raise exc
        except Exception as exc:
            return Response({"status": "error"}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)