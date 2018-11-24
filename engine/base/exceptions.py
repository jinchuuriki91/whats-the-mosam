from rest_framework.exceptions import APIException
from rest_framework import status as rest_status


class BadDataException(APIException):
    status_code = rest_status.HTTP_400_BAD_REQUEST
    default_detail = "Bad Request"