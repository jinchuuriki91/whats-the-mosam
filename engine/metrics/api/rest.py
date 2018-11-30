# Python imports
from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework.status as rest_status
from rest_framework.pagination import PageNumberPagination

# Engine imports
from metrics.utils import create_record, get_records
from base.exceptions import BadDataException
from metrics.constants import REGION_INT


class MetricsHandler(APIView):

    valid_types = ("Tmax", "Tmin", "Rainfall")

    def get(self, request):
        """Returns weather data. """
        try:
            body = request.GET.dict()
            metric_type = body.get("type", None)
            location = body.get("location", None)
            start_date = body.get("start_date", "")
            end_date = body.get("end_date", "")
            
            if metric_type not in self.valid_types or location not in REGION_INT.keys():
                raise BadDataException("Please provide metric type and location")
            
            results = get_records(request.user, REGION_INT[body["location"]], metric_type, start_date, end_date)
            resp = {
                "type": metric_type,
                "location": location,
                "start_date": start_date,
                "end_date": end_date,
                "results": results,
                "count": len(results)
            }
            return Response(resp, status=rest_status.HTTP_200_OK)
        except BadDataException as exc:
            raise exc
        except Exception:
            return Response({"status": "error"}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """Creates weather data. """
        try:
            body = request.data
            metric_type = body.get("type", None)
            location = body.get("location", None)
            if metric_type not in self.valid_types or location not in REGION_INT.keys():
                raise BadDataException("Please provide metric type and location")
            
            resp = create_record(request.user, REGION_INT[body["location"]], body.get("data", []), metric_type)
            return Response({"status": "success", "results": resp}, status=rest_status.HTTP_201_CREATED)
        except BadDataException as exc:
            raise exc
        except Exception:
            return Response({"status": "error"}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)