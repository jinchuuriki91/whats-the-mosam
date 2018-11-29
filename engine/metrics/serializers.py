# Python imports
from rest_framework import serializers

# Engine imports
from .models import MaxTemperature, MinTemperature, Rainfall


class BaseMetricsSerializer(serializers.ModelSerializer):
    year = serializers.ReadOnlyField()
    month = serializers.ReadOnlyField()


class MaxTempSerializer(BaseMetricsSerializer):
    class Meta:
        model = MaxTemperature
        fields = ("value", "year", "month")


class MinTempSerializer(BaseMetricsSerializer):
    class Meta:
        model = MinTemperature
        fields = ("value", "year", "month")


class RainfallSerializer(BaseMetricsSerializer):
    class Meta:
        model = Rainfall
        fields = ("value", "year", "month")