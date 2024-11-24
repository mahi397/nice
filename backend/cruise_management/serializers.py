import re
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MmsTrip, MmsPortStop, MmsPort, MmsRestaurant, MmsTripActivity, MmsTripRestaurant, MmsActivity
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'first_name', 'last_name']
        extra_kwargs = {"password":{"write_only": True}}
    
    def validate_username(self, value):
        # Check if username is reserved (e.g., "admin")
        if value.lower() == "admin":
            raise serializers.ValidationError("Username 'admin' is reserved. Please choose a different username.")
        
        # Ensure the username is unique
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists. Please choose a different username.")
        
        # Return the cleaned username (ensure it's case-insensitive)
        return value.lower()

    def validate_email(self, value):
        # Ensure the email is valid
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("Enter a valid email address.")
        
        # Ensure email is unique
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email address already registered. Please use a different email.")
        
        # Return the cleaned email (lowercase for case-insensitive comparison)
        return value.lower()

    def validate_password(self, value):
        # Ensure password is strong (min 8 characters, includes a special character, number, and upper case letter)
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        if not re.search(r"\d", value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        
        return value

    def validate(self, data):
        # Confirm the passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        
        # Remove the confirm_password field from data as it's not saved
        data.pop('confirm_password')
        
        return data
    
    def create(self, validated_data):
        # Remove the password from validated data and handle separately
        password = validated_data.pop('password')

        # Create the user instance
        user = User.objects.create_user(**validated_data)

        # Set the password (hashing it before saving)
        user.set_password(password)
        user.save()

        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Call the parent class's validate method to get the validated data (access token and refresh token)
        data = super().validate(attrs)
        
        # Get the user object from the request (user is automatically attached to the request after authentication)
        user = self.user
        
        # Add custom claims (username and email) to the token payload
        data['username'] = user.username
        data['email'] = user.email
        
        return data
    
class MmsTripListSerializer(serializers.ModelSerializer):
    # Nested serializer for related start port (via MmsPortStop and MmsPort)
    port_stops = serializers.SerializerMethodField()
    start_port = serializers.SerializerMethodField()
    end_port = serializers.SerializerMethodField()

    class Meta:
        model = MmsTrip
        fields = ['tripid', 'tripname', 'startdate', 'enddate', 'tripcostperperson', 'start_port', 'end_port', 'port_stops']
    
    def get_port_stops(self, obj):
        """
        Fetch all port stops with their details and order them.
        """
        port_stops = obj.mmsportstop_set.all().order_by('orderofstop')
        return [
            {
                "port_name": stop.portid.portname if stop.portid else None,
                "city": stop.portid.portcity if stop.portid else None,
                "country": stop.portid.portcountry if stop.portid else None,
                "order_of_stop": stop.orderofstop,
                "is_start_port": stop.isstartport == "Y",
                "is_end_port": stop.isendport == "Y",
            }
            for stop in port_stops
        ]

    def get_start_port(self, obj):
        """
        Extract the start port from the list of port stops.
        """
        port_stops = self.get_port_stops(obj)  # Use the pre-fetched port stops
        start_port = next((stop for stop in port_stops if stop['is_start_port']), None)
        return start_port['port_name'] if start_port else None

    def get_end_port(self, obj):
        """
        Extract the end port from the list of port stops.
        """
        port_stops = self.get_port_stops(obj)  # Use the pre-fetched port stops
        end_port = next((stop for stop in port_stops if stop['is_end_port']), None)
        return end_port['port_name'] if end_port else None
             
class MmsTripDetailSerializer(MmsTripListSerializer):
    # Nested serializer for related start port (via MmsPortStop and MmsPort)
    # Additional fields
    trip_description = serializers.CharField(source='description', read_only=True)
    cancellation_policy = serializers.CharField(source='cancellationpolicy', read_only=True)
    #ship_details = serializers.SerializerMethodField()
    additional_fees = serializers.DecimalField(source='additionalfees', max_digits=10, decimal_places=2, read_only=True)
    port_times = serializers.SerializerMethodField()
    restaurants = serializers.SerializerMethodField()
    activities = serializers.SerializerMethodField()

    class Meta(MmsTripListSerializer.Meta):
        fields = MmsTripListSerializer.Meta.fields + [
            'trip_description', 
            'cancellation_policy',  
            'additional_fees', 
            'port_stops',
            'port_times',
            'restaurants',
            'activities'
        ]

    '''def get_ship_details(self, obj):
        """
        Fetch details about the ship associated with the trip.
        """
        ship = obj.ship
        return {
            "name": ship.name,
            "capacity": ship.capacity,
            "crew_count": ship.crew_count,
        } if ship else None'''
        
    def get_port_times(self, obj):
        """
        Get arrival and departure times for each port in the trip.
        """
        port_times = []

        # Iterate over all port stops for the trip
        for port_stop in obj.mmsportstop_set.all().order_by('orderofstop'):
            # Retrieve port information
            port = port_stop.portid  
            
            # Prepare the port time data
            port_time_data = {
                "port_name": port.portname,  
                "arrival_time": port_stop.arrivaltime,  
                "departure_time": port_stop.departuretime,  
            }
            # Add the port time data to the list
            port_times.append(port_time_data)

        return port_times if port_times else None
    
    def get_restaurants(self, obj):
        restaurants = obj.mmstriprestaurant_set.all()
        return [
            {
                "restaurant_name": restaurant.restaurantid.restaurantname if restaurant.restaurantid else None,
                "breakfast": restaurant.restaurantid.servesbreakfast if restaurant.servesbreakfast else None,
                "lunch": restaurant.restaurantid.serveslunch if restaurant.serveslunch else None,
                "dinner": restaurant.restaurantid.servesdinner if restaurant.servesdinner else None,
                "alcohol": restaurant.restaurantid.servesalcohol if restaurant.servesalcohol else None
            }
            for restaurant in restaurants
        ]
        
    def get_activities(self, obj):
        activities = obj.mmstripactivity_set.all()
        return [
            {
                "activity_name":activity.activityid.activityname if activity.activityid else None,
                "activity_type":activity.activityid.activitytype if activity.activitytype else None,
                "capacity":activity.activityid.capacity if activity.capacity else None
            }
            for acitivty in activities
        ]
    


    