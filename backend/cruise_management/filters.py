from dataclasses import field
from django_filters import rest_framework as filters
from django.db.models import F
from datetime import timedelta
from .models import MmsActivity, MmsRestaurant, MmsRoom, MmsTrip, MmsPortStop, MmsPort

class TripFilter(filters.FilterSet):
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
    
    # Filter by regions
    port_city = filters.CharFilter(method='filter_by_port_city', label = "Places to visit")
    port_country = filters.CharFilter(method='filter_by_port_country', label = "Regions")

    class Meta:
        model = MmsTrip
        fields = ['startdate_min', 'startdate_max', 'duration_min', 'duration_max', 'tripcostperperson_min', 'tripcostperperson_max', 'start_port_name', 'port_city', 'port_country']

    def filter_by_start_port_name(self, queryset, name, value):
        """
        Filters trips based on the start port name (via MmsPortStop).
        """
        return queryset.filter(
            mmsportstop__portid__portname__icontains=value,
            mmsportstop__isstartport='Y'  # Only consider the start port (assuming 'Y' means start port)
        )
        
    def filter_by_port_city(self, queryset, name, value):
        """
        Filters trips based on the start port name (via MmsPortStop).
        """
        return queryset.filter(mmsportstop__portid__portcity__iexact=value)
    
    def filter_by_port_country(self, queryset, name, value):
        """
        Filters trips based on the start port name (via MmsPortStop).
        """
        return queryset.filter(mmsportstop__portid__portcountry__iexact=value)

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
    
class PortFilter(filters.FilterSet):
    
    port_name = filters.CharFilter(field_name='portname', lookup_expr='icontains', label="Port Name (partial match)")
    port_city = filters.CharFilter(field_name='portcity', lookup_expr='iexact', label="City (exact match)")
    port_country = filters.CharFilter(field_name='portcountry', lookup_expr='iexact', label="Country")
    nearest_airport = filters.CharFilter(field_name='nearestairport', lookup_expr='icontains', label="Nearest Airport")
    parking_spots_min = filters.NumberFilter(field_name='parkingspots', lookup_expr='gte', label="Minimum Parking Spots")
    parking_spots_max = filters.NumberFilter(field_name='parkingspots', lookup_expr='lte', label="Maximum Parking Spots")

    class Meta:
        model = MmsPort
        fields = ['port_name', 'port_city', 'port_country', 'nearest_airport', 'parking_spots_min', 'parking_spots_max'] 
    
class RestaurantFilter(filters.FilterSet):
    
    restaurant_name = filters.CharFilter(field_name='restaurantname', lookup_expr='icontains', label="Restaurant Name (partial match)")
    serves_breakfast = filters.CharFilter(field_name='servesbreakfast', lookup_expr='iexact', label="Serves Breakfast")
    serves_lunch = filters.CharFilter(field_name='serveslunch', lookup_expr='iexact', label="Serves Lunch")
    serves_dinner = filters.CharFilter(field_name='servesdinner', lookup_expr='iexact', label="Serves Dinner")
    serves_alcohol = filters.CharFilter(field_name='servesalcohol', lookup_expr='iexact', label="Server Alcohol")
    
    class Meta:
        model = MmsRestaurant
        fields = ['restaurant_name', 'serves_breakfast', 'serves_lunch', 'serves_dinner', 'serves_alcohol'] 
        
class ActivityFilter(filters.FilterSet):
    
    activity_name = filters.CharFilter(field_name='activityname', lookup_expr='icontains', label="Restaurant Name (partial match)")
    activity_type = filters.CharFilter(field_name='activitytype', lookup_expr='iexact', label="Serves Breakfast")
    capacity_min = filters.CharFilter(field_name='capacity', lookup_expr='gte', label="Min Capacity")
    capacity_max = filters.NumberFilter(field_name='capacity', lookup_expr='lte', label="Max Capacity")
    
    class Meta:
        model = MmsActivity
        fields = ['activity_name', 'activity_type', 'capacity_min', 'capacity_max']

class RoomFilter(filters.FilterSet):
    room_floor = filters.CharFilter(field_name='roomfloor', lookup_expr='iexact', label="Floor number")
    room_base_price_min = filters.NumberFilter(field_name='roombaseprice', lookup_expr='gte', label="Min Cost")
    room_base_price_max = filters.NumberFilter(field_name='roombaseprice', lookup_expr='lte', label="Max Cost")
    ship_location = filters.CharFilter(method='filter_by_ship_location', label="Start Port Name")
    room_type = filters.CharFilter(method='filter_by_room_type', label="Start Port Name")
    
    class Meta:
        model = MmsRoom
        fields = ['room_floor', 'room_base_price_min', 'room_base_price_max', 'ship_location', 'room_type']
        
        def filter_by_ship_location(self, queryset, name, value):
            """
            Filters trips based on the start port name (via MmsPortStop).
            """
            return queryset.filter(mmsroomloc__locid__location__icontains=value)
        
        def filter_by_room_type(self, queryset, name, value):
            """
            Filters trips based on the start port name (via MmsPortStop).
            """
            return queryset.filter(mmsroomtype__stateroomtypeid__stateroomtype__icontains=value)
               
        