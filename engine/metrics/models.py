# Python imports
import calendar

# Django imports
from django.db import models
from django.utils import timezone

# Engine imports
from base.models import ModelBase
from .constants import REGION, MONTH


class MetricsBaseManager(models.Manager):

    def add_or_update_record(self, value, region, month, year):
        """
        Add or update a record.
        
        Args:
            value: value of the metric, a float value
            region: region of the metric
            month: index of the month of year (1-12)
            year: year of the metric

        Return:
            Metric object
        """
        try:
            # func_tag = "MetricsBaseManager:add_record"
            day = calendar.monthrange(year, month)[1]
            dt = timezone.datetime(year, month, day)
            return self.update_or_create(record_date=dt,
                                         region=region,
                                         defaults={"value": value})
        except Exception as exc:
            raise exc


class MetricsBase(ModelBase):

    value = models.FloatField(default=0.0)
    region = models.IntegerField(choices=REGION)
    record_date = models.DateField()
    
    objects = MetricsBaseManager()
    
    class Meta:
        abstract = True
        ordering = ["record_date"]

    @property
    def year(self):
        return self.record_date.year
    
    @property
    def month(self):
        return self.record_date.month


class MaxTemperature(MetricsBase):

    def __str__(self):
        return "Tmax <%s:%s DegC> (%s)" % (REGION[self.region][1], self.value, self.record_date)


class MinTemperature(MetricsBase):

    def __str__(self):
        return "Tmin <%s:%s DegC> (%s)" % (REGION[self.region][1], self.value, self.record_date)


class Rainfall(MetricsBase):

    def __str__(self):
        return "Rainfall <%s:%s mm> (%s)" % (REGION[self.region][1], self.value, self.record_date)