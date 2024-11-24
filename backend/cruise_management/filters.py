from django_filters import rest_framework as filters
from django.db.models import F
from datetime import timedelta
from .models import MmsTrip, MmsPortStop, MmsPort

class CruiseFilter(filters.FilterSet):
    # Filter trips based on the start date range
    startdate_min = filters.DateTimeFilter(field_name='startdate', lookup_expr='gte', label="Start Date (>=)")
    startdate_max = filters.DateTimeFilter(field_name='startdate', lookup_expr='lte', label="Start Date (<=)")
    
    # Filter trips by the duration of the cruise
    duration_min = filters.NumberFilter(method='filter_by_duration_min', label="Min Duration (Days)")
    duration_max = filters.NumberFilter(method='filter_by_duration_max', label="Max Duration (Days)")
    
    # Price filters
    tripcostperperson_min = filters.NumberFilter(field_name='tripcostperperson', lookup_expr='gte', label="Min Cost")
    tripcostperperson_max = filters.NumberFilter(field_name='tripcostperperson', lookup_expr='lte', label="Max Cost")
    
    # Filter by start port name (this is from related MmsPort model via MmsPortStop)
    start_port_name = filters.CharFilter(method='filter_by_start_port_name', label="Start Port Name")

    class Meta:
        model = MmsTrip
        fields = ['startdate_min', 'startdate_max', 'duration_min', 'duration_max', 'tripcostperperson_min', 'tripcostperperson_max', 'tripstatus', 'start_port_name']

    def filter_by_start_port_name(self, queryset, name, value):
        """
        Filters trips based on the start port name (via MmsPortStop).
        """
        return queryset.filter(
            mmsportstop__portid__portname__icontains=value,
            mmsportstop__isstartport='Y'  # Only consider the start port (assuming 'Y' means start port)
        )

    def filter_by_duration_min(self, queryset, name, value):
        """
        Filters trips based on the minimum duration (startdate and enddate).
        """
        return queryset.filter(enddate__gt=F('startdate') + timedelta(days=value))

    def filter_by_duration_max(self, queryset, name, value):
        """
        Filters trips based on the maximum duration (startdate and enddate).
        """
        return queryset.filter(enddate__lt=F('startdate') + timedelta(days=value))