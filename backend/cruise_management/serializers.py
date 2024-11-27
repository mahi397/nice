import re
from . import models
from datetime import date
from django.db import transaction
from rest_framework import serializers 
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MmsUserProfile
        fields = ['phonenumber', 'dateofbirth']
        
    def validate_phonenumber(self, value):
        """
        Validate phone number to ensure it only contains digits and is of a specific length.
        """
        if not re.fullmatch(r'\+?[1-9]\d{1,14}', value):  # E.164 international format
            raise ValidationError("Phone number must be valid and follow international standards.")
        return value

    def validate_dateofbirth(self, value):
        """
        Validate date of birth to ensure it's not in the future and the user is at least 13 years old.
        """
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        age = (date.today() - value).days // 365
        if age < 13:
            raise ValidationError("User must be at least 13 years old.")
        return value
        
class UserCreateSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    password = serializers.CharField(write_only=True, required=True, min_length=8, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'profile']
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
        
        # The line `if not re.search(r"[A-Z]", value):` is checking if the provided `value` (in this
        # case, a password) contains at least one uppercase letter (character from A to Z).
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
    
    @transaction.atomic
    def create(self, validated_data):
        # Remove password from validated data and handle separately
        password = validated_data.pop('password')
        profile_data = validated_data.pop('profile', None)
        # Create the user instance (without profile)
        user = User.objects.create_user(**validated_data)
        
        # Set the password (it gets hashed here)
        user.set_password(password)
        
        # Create the user profile if data is provided
        
        if profile_data:
            models.MmsUserProfile.objects.create(user_id=user.pk, **profile_data)
        
        # Save the user instance
        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile']  # Limit to updatable fields
        
    @transaction.atomic
    def update(self, instance, validated_data):
        # Update user's main fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        # Update profile fields if provided
        profile_data = validated_data.pop('profile', None)
        if profile_data:
            profile_instance = models.MmsUserProfile.objects.get(user_id=instance.id)  
            profile_instance.phonenumber = profile_data.get('phonenumber', profile_instance.phonenumber)
            profile_instance.save()

        instance.save()
        return instance
    
    def to_representation(self, instance):
        """
        Customize the serialized output to include the related profile data.
        """
        representation = super().to_representation(instance)

        # Manually add the profile data
        try:
            profile_instance = models.MmsUserProfile.objects.get(user_id=instance.id)
            representation['profile'] = UserProfileSerializer(profile_instance).data
        except models.MmsUserProfile.DoesNotExist:
            representation['profile'] = None

        return representation

class LoginSerializer(TokenObtainPairSerializer):
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
        model = models.MmsTrip
        fields = ['tripid', 'tripname', 'startdate', 'enddate', 'tripcostperperson', 'start_port', 'end_port', 'port_stops']
    
    def get_port_stops(self, obj):
        """
        Fetch all port stops with their details and order them.
        """
        port_stops = obj.portstops.all().order_by('orderofstop')
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
        for port_stop in obj.portstops.all().order_by('orderofstop'):
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
            for activity in activities
        ]
    
class MmsPortCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MmsPort
        fields = ['portid', 'portname', 'address', 'portcity', 'portstate', 'portcountry', 'nearestairport', 'parkingspots']
        
    def validate_restaurantid(self, data):
        """
        Validate that the itinerary ID is unique.
        Allow the current object to keep the same itinerary ID during updates.
        """
        port_id = self.instance.portid if self.instance else None
        if MmsPort.objects.filter(portid=data).exclude(portid=port_id).exists():
            raise serializers.ValidationError("A port with this port ID already exists.")
        
        return data

    def validate(self, attrs):
        """
        Custom validation logic for the port.
        """
        if (
            not attrs.get('portname') 
            or not attrs.get('portid') 
            or not attrs.get('portcity') 
            or not attrs.get('portcountry')
            or not attrs.get('address')
            or not attrs.get('portstate')
            or not attrs.get('nearestairport')
            or not attrs.get('parkingspots')
        ):
            raise serializers.ValidationError("All port details are required.")
        return attrs

    def create(self, validated_data):
        """
        Create a new port using the validated data.
        """
        return MmsPort.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        
        validated_data.pop('portid', None)  # Remove the portid field if it exists
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
        '''
        instance.portname = validated_data.get('portname', instance.portname)
        instance.address = validated_data.get('address', instance.address)
        instance.portcity = validated_data.get('portcity', instance.portcity)
        instance.portstate = validated_data.get('portstate', instance.portstate)
        instance.portcountry = validated_data.get('portcountry', instance.portcountry)
        instance.nearestairport = validated_data.get('nearestairport', instance.nearestairport)
        instance.parkingspots = validated_data.get('parkingspots', instance.parkingspots)
        '''
        instance.save()
        return instance
    
class MmsRestaurantCreateUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.MmsRestaurant
        fields = ['restaurantid', 'restaurantname', 'floornumber', 'openingtime', 'closingtime', 'servesbreakfast',
                  'serveslunch', 'servesdinner', 'servesalcohol']
    
    def validate_restaurantid(self, data):
        """
        Validate that the itinerary ID is unique.
        Allow the current object to keep the same itinerary ID during updates.
        """
        restaurant_id = self.instance.restaurantid if self.instance else None
        if MmsRestaurant.objects.filter(restaurantid=data).exclude(restaurantid=restaurant_id).exists():
            raise serializers.ValidationError("A restaurant with this restaurant ID already exists.")
        
        return data
        
    def validate_floornumber(self, value):
        if value < 0:
            raise serializers.ValidationError("Floor number cannot be negative.")
        return value

    def validate(self, data):
        openingtime = data.get('openingtime')
        closingtime = data.get('closingtime')

        # Validate openingtime exists
        if not openingtime:
            raise serializers.ValidationError("Opening time is required.")
        
        # Handle optional closingtime
        if closingtime:
            if openingtime >= closingtime:
                raise serializers.ValidationError(
                    "Opening time must be earlier than closing time unless the restaurant operates 24 hours."
                )
        
        # Check at least one meal service
        if not any([data.get('servesbreakfast'), data.get('serveslunch'), data.get('servesdinner')]):
            raise serializers.ValidationError("At least one meal service (breakfast, lunch, or dinner) must be provided.")
        
        return data

    def create(self, validated_data):
        return MmsRestaurant.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        
        validated_data.pop('restaurantid', None)  # Remove the portid field if it exists
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
        
class MmsActivityCreateUpdateSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = models.MmsActivity
        fields = ['activityid', 'activitytype', 'activityname', 'floor', 'capacity']
       
    def validate_activityid(self, data):
        """
        Validate that the itinerary ID is unique.
        Allow the current object to keep the same itinerary ID during updates.
        """
        activity_id = self.instance.activityid if self.instance else None
        if MmsActivity.objects.filter(activityid=data).exclude(activityid=activity_id).exists():
            raise serializers.ValidationError("An activity with this activity ID already exists.")
        
        return data
     
    def validate_activitytype(self, value):
        valid_types = ['sports', 'entertainment', 'educational']
        if value not in valid_types:
            raise serializers.ValidationError("Invalid activity type.")
        return value

    def validate_activityname(self, value):
        if len(value) > 100:
            raise serializers.ValidationError("Activity name is too long.")
        return value

    def validate_floor(self, value):
        if value < 0 or value > 20:
            raise serializers.ValidationError("Floor must be between 0 and 10.")
        return value

    def validate_capacity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Capacity must be a positive number.")
        if value > 1000:
            raise serializers.ValidationError("Capacity cannot exceed 1000.")
        return value

    def validate(self, data):
        if data['activitytype'] == 'sports' and data['capacity'] > 500:
            raise serializers.ValidationError("Sports activities cannot have a capacity greater than 500.")
        return data

    def create(self, validated_data):
        return MmsActivity.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        
        instance.activityname = validated_data.get('activityname', instance.activityname)
        instance.activitytype = validated_data.get('activitytype', instance.activitytype)
        instance.floor = validated_data.get('floor', instance.floor)
        instance.capacity = validated_data.get('capacity', instance.capacity)
        instance.save()
        return instance
    
class MmsPortStopCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MmsPortStop
        fields = ['itineraryid','tripid', 'portid', 'arrivaltime', 'departuretime', 'orderofstop', 'isstartport', 'isendport']
    
    def validate_itineraryid(self, data):
        """
        Validate that the itinerary ID is unique.
        Allow the current object to keep the same itinerary ID during updates.
        """
        current_itineraryid = self.instance.itineraryid if self.instance else None
        if MmsPortStop.objects.filter(itineraryid=data).exclude(itineraryid=current_itineraryid).exists():
            raise serializers.ValidationError("A port stop with this itinerary ID already exists.")
        
        return data
    
    def validate(self, data):
        # Ensure `isstartport` and `isendport` are valid
        if data.get('isstartport') not in ['Y', 'N']:
            raise serializers.ValidationError("isstartport must be 'Y' or 'N'.")
        if data.get('isendport') not in ['Y', 'N']:
            raise serializers.ValidationError("isendport must be 'Y' or 'N'.")

        # Ensure arrival time is before departure time
        if data['arrivaltime'] >= data['departuretime']:
            raise serializers.ValidationError("Arrival time must be before departure time.")
        return data 
    
    def create(self, validated_data): 
        # Create trip instance
        trip = MmsPortStop.objects.create(**validated_data)
        return trip

    '''def update(self, instance, validated_data):
        # Extract port stops data
        portstops_data = validated_data.pop('portstops', [])
        # Handle port stops
        existing_portstops = {ps.itineraryid: ps for ps in instance.portstops.all()}
        updated_portstops = []

        for portstop_data in portstops_data:
            itinerary_id = portstop_data.get('itineraryid')

            if itinerary_id and itinerary_id in existing_portstops:
                # Update existing port stop
                portstop = existing_portstops[itinerary_id]
                for attr, value in portstop_data.items():
                    setattr(portstop, attr, value)
                portstop.save()
            else:
                # Create a new port stop
                new_portstop = MmsPortStop.objects.create(tripid=instance, **portstop_data)
                updated_portstops.append(new_portstop.itineraryid)

        # Remove any port stops that are no longer in the update data
        instance.portstops.exclude(itineraryid__in=updated_portstops).delete()
        instance.save()
        return instance'''
    def update(self, instance, validated_data):
        # Update trip fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class MmsTripCreateUpdateSerializer(serializers.ModelSerializer):
                                                       
    class Meta:
        model = models.MmsTrip
        fields = ['tripid', 'tripname', 'startdate', 'enddate', 'tripcostperperson', 'tripstatus', 'capacity']
    
    def validate_tripid(self, data):
        trip_id = self.instance.tripid if self.instance else None
        if MmsTrip.objects.filter(tripid=data).exclude(tripid=trip_id).exists():
            raise serializers.ValidationError("A trip with this trip id already exists")
        
        return data
    
    def validate(self, data):
        # Validate trip dates
        if data['startdate'] >= data['enddate']:
            raise serializers.ValidationError("Start date must be before end date.")
        
        if data['capacity'] <=100:
            raise serializers.ValidationError("Cruise capacity must be more than 100.")
        return data

    def create(self, validated_data):
        
        # Create trip instance
        trip = MmsTrip.objects.create(**validated_data)
        return trip
    
    def update(self, instance, validated_data):
        # Update trip fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
