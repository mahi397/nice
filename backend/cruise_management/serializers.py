import re
from tarfile import data_filter
from wsgiref.util import request_uri
from . import models
from datetime import date
from django.db import transaction
from rest_framework import serializers 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError, AuthenticationFailed


# Admin related features

class AdminLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        identifier = attrs.get('username')  # Can be email or username
        password = attrs.get('password')

        user = None

        # Check if the identifier is an email
        if re.match(r"[^@]+@[^@]+\.[^@]+", identifier):
            try:
                # Fetch user by email
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                raise AuthenticationFailed('No account found with that email.')
        else:
            try:
                # Fetch user by username
                user = User.objects.get(username=identifier)
            except User.DoesNotExist:
                raise AuthenticationFailed('No account found with that username.')

        # Restrict access to only staff and admin accounts
        if not user.is_staff and not user.is_superuser:
            raise AuthenticationFailed('Only staff and admin accounts are allowed to log in.')

        # Authenticate user explicitly using username and password
        user = authenticate(username=user.username, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials.')

        # Call the parent method to generate tokens
        data = super().validate({"username": user.username, "password": password})

        # Add custom claims
        data['username'] = user.username
        data['email'] = user.email
        if user.is_staff:
            data['is_staff'] = user.is_staff
        else:
            data['is_superuser'] = user.is_superuser

        return data

class MmsPortSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MmsPort
        fields = ['portname', 'address', 'portcity', 'portstate', 'portcountry', 'nearestairport', 'parkingspots']
        
    def validate_portname(self, data):
        # Ensure portname is a non-empty string
        if not data or data.strip() == "":
            raise ValidationError("Port name cannot be empty.")
        if models.MmsPort.objects.filter(portname=data).exists():
            raise ValidationError(f"A port with name {data} already exists.")
        return data

    def validate_address(self, data):
        # Ensure address is a non-empty string
        if not data or data.strip() == "":
            raise ValidationError("Address cannot be empty.")
        return data

    def validate_portcity(self, data):
        # Ensure portcity is a valid string
        if not data or data.strip() == "":
            raise ValidationError("Port city cannot be empty.")
        return data

    def validate_portstate(self, data):
        # Ensure portstate is a valid string
        if not data or data.strip() == "":
            raise ValidationError("Port state cannot be empty.")
        return data

    def validate_portcountry(self, data):
        # Ensure portcountry is a valid country
        if not data or data.strip() == "":
            raise ValidationError("Port country cannot be empty.")
        # Optional: Add a check to validate the country, e.g., check against a list of countries
        return data

    def validate_nearestairport(self, data):
        # Ensure nearestairport is a valid string (if applicable, you could check if the airport exists in a database)
        if not data or data.strip() == "":
            raise ValidationError("Nearest airport cannot be empty.")
        return data

    def validate_parkingspots(self, data):
        # Ensure parkingspots is a non-negative integer
        if data < 0:
            raise ValidationError("Parking spots must be a non-negative integer.")
        return data

    def validate(self, attrs):
        """
        Custom validation logic for the port.
        """
        if (
            not attrs.get('portname') 
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
        return models.MmsPort.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
                   
class MmsPortListSerializer(serializers.ModelSerializer):
    # Nested serializer for related start port (via MmsPortStop and MmsPort)

    class Meta:
        model = models.MmsPort
        fields = '__all__'
            
class MmsRestaurantCreateUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.MmsRestaurant
        fields = ['restaurantname', 'floornumber', 'openingtime', 'closingtime', 'servesbreakfast',
                  'serveslunch', 'servesdinner', 'servesalcohol', 'restaurant_description']
    
    def validate_restaurantname(self, data):
        # Ensure portname is a non-empty string
        if not data or data.strip() == "":
            raise ValidationError("Restaurant name cannot be empty.")
        if models.MmsRestaurant.objects.filter(restaurantname=data).exclude(restaurantname=data).exists():
            raise ValidationError(f"A restaurant with name {data} already exists.")
        return data
        
    def validate_floornumber(self, data):
        if data < 0:
            raise serializers.ValidationError("Floor number cannot be negative.")
        return data

    def validate_restaurant_description(self, data):
        """
        Validate restaurant description field.
        """
        # Ensure it's not empty
        if not data.strip():
            raise ValidationError("Description cannot be empty.")
        
        # Ensure it's not too long (max length 500 characters as an example)
        if len(data) > 500:
            raise ValidationError("Description cannot be longer than 500 characters.")
        
        return data
    
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
        if not any([
        data.get('servesbreakfast') == 'Y',
        data.get('serveslunch') == 'Y',
        data.get('servesdinner') == 'Y'
        ]):
            raise serializers.ValidationError("At least one meal service (breakfast, lunch, or dinner) must be 'Y'.")
        
        
        return data

    def create(self, validated_data):
        return models.MmsRestaurant.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
            
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class MmsRestaurantListSerializer(serializers.ModelSerializer):
    # Nested serializer for related start port (via MmsPortStop and MmsPort)

    class Meta:
        model = models.MmsRestaurant
        fields = '__all__'    
        
class MmsActivityCreateUpdateSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = models.MmsActivity
        fields = ['activitytype', 'activityname', 'activitydescription', 'floor', 'capacity']
        
    def validate_activityname(self, data):
        # Ensure portname is a non-empty string
        if not data or data.strip() == "":
            raise ValidationError("Activity name cannot be empty.")
        
        if len(data) > 100:
            raise serializers.ValidationError("Activity name cannot exceed 100 characters.")
        
        if models.MmsActivity.objects.filter(activityname=data).exists():
            raise ValidationError(f"An activity with name {data} already exists.")
        return data

    def validate_activitytype(self, data):
        valid_types = ['sports', 'leisure', 'entertainment']  # Example values
        if data.lower() not in valid_types:
            raise serializers.ValidationError(f"Invalid activity type. Must be one of {valid_types}.")
        return data
    
    def validate_activitydescription(self, data):
        # Ensure the description is not empty or just whitespace
        if not data or data.strip() == "":
            raise ValidationError("Activity description cannot be empty.")
        
        # Ensure the description does not exceed the maximum length
        if len(data) > 300:
            raise ValidationError("Activity description must not exceed 300 characters.")
        
        if not re.match(r'^[a-zA-Z0-9.,!? ]*$', data):
            raise ValidationError("Activity description contains invalid characters.")
        
        return data
    
    def validate_floor(self, data):
        if data < 0:
            raise serializers.ValidationError("Floor number cannot be negative.")
        if data > 20:
            raise serializers.ValidationError(("Floor number cannot exceed 20."))
        return data

    def validate_capacity(self, data):
        if data <= 0:
            raise serializers.ValidationError("Capacity must be a positive number.")
        return data

    def validate(self, data):
        activitytype = data.get('activitytype')
        capacity = data.get('capacity')
        
        if activitytype == 'entertainment' and capacity > 300:
            raise serializers.ValidationError("Entertainment activities cannot exceed a capacity of 300.")
        if activitytype == 'sports' and capacity > 100:
            raise serializers.ValidationError("Sports activities cannot exceed a capacity of 100.")
        
        return data
    
    def create(self, validated_data):
        return models.MmsActivity.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class MmsActivityListSerializer(serializers.ModelSerializer):
    # Nested serializer for related start port (via MmsPortStop and MmsPort)

    class Meta:
        model = models.MmsActivity
        fields = '__all__'

class MmsRoomLocCreateUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.MmsRoomLoc
        fields = ['location']
        
    def validate(self, data):
        location = data.get('location')
        # Validate location 
        valid_types = ['bow', 'stern', 'port side', 'starboard side']
        if location.lower() not in valid_types:
            raise serializers.ValidationError(f"Location has to be one of {valid_types}")
         
        return data

    def create(self, validated_data):
        return models.MmsRoomLoc.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Update fields on the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class MmsRoomLocListSerializer(serializers.ModelSerializer):
    # Nested serializer for related start port (via MmsPortStop and MmsPort)

    class Meta:
        model = models.MmsRoomLoc
        fields = '__all__'
       
class MmsRoomTypeCreateUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.MmsRoomType
        fields = ['stateroomtype', 'roomsize', 'numberofbeds', 'numberofbaths', 'numberofbalconies']
    
    def validate_stateroomtypeid(self, data):
        """
        Validate that the state room type ID is unique.
        Allow the current object to keep the same state room type ID during updates.
        """
        stateroomtype_id = self.instance.stateroomtypeid if self.instance else None
        if models.MmsRoomType.objects.filter(stateroomtypeid=data).exclude(stateroomtypeid=stateroomtype_id).exists():
            raise serializers.ValidationError("A state room type with this state room type ID already exists.")
        
        if data <= 0:
            raise serializers.ValidationError("Stateroom Type ID must be a positive number.")
        
        return data
    
    def validate_stateroomtype(self, data):
        if not data.strip():
            raise serializers.ValidationError("Stateroom type cannot be empty or whitespace.")
        valid_types = ['the haven suite', 'club balcony suite', 'family large balcony', 'family balcony', 'oceanview window', 'inside stateroom' 'studio stateroom']
        if data.lower() not in valid_types:
            raise serializers.ValidationError(f"Invalid stateroom type. Must be one of {valid_types}.")
        return data
    
    def validate_roomsize(self, data):
        if data <= 0:
            raise serializers.ValidationError("Room size must be a positive value.")
        if data > 10000:  # Arbitrary upper limit for room size
            raise serializers.ValidationError("Room size seems unrealistically large.")
        return data

    def validate_numberofbeds(self, data):
        if data <= 0:
            raise serializers.ValidationError("Number of beds must be at least 1.")
        if data > 10:
            raise serializers.ValidationError("Number of beds seems unrealistically high.")
        return data
    
    def validate_numberofbaths(self, data):
        if data <= 0:
            raise serializers.ValidationError("Number of bathrooms must be at least 0.5.")
        if data > 5:
            raise serializers.ValidationError("Number of bathrooms seems unrealistically high.")
        return data

    def validate_numberofbalconies(self, data):
        if data < 0:
            raise serializers.ValidationError("Number of balconies cannot be negative.")
        if data > 3:
            raise serializers.ValidationError("Number of balconies seems unrealistically high.")
        return data

    def validate(self, attrs):
        if attrs.get('numberofbeds', 0) == 0:
            raise serializers.ValidationError("A room must have at least one bed.")
        if attrs.get('numberofbalconies', 0) > 0 and attrs.get('numberofbeds', 0) == 0:
            raise serializers.ValidationError("A room with balconies must have at least one bed.")
        return attrs

    '''def create(self, validated_data):
        return models.MmsRoomType.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Update fields on the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance'''

class MmsRoomTypeListSerializer(serializers.ModelSerializer):
    # Nested serializer for related start port (via MmsPortStop and MmsPort)

    class Meta:
        model = models.MmsRoomType
        fields = '__all__'

class MmsRoomBaseSerializer(serializers.ModelSerializer):
    stateroomtypeid = serializers.CharField()
    locid = serializers.CharField()    
    class Meta:
        model = models.MmsRoom
        fields = ['roomnumber', 'roomfloor', 'roombaseprice', 'stateroomtypeid', 'locid']
    
    
    def validate_roomnumber(self, data):
        print(self.instance)
        room_number = self.instance.roomnumber if self.instance else None
        
        if models.MmsRoom.objects.filter(roomnumber=room_number).exclude(roomnumber=room_number).exists():
            raise serializers.ValidationError("A room with this room number already exists.")
        
        if data < 0:
            raise serializers.ValidationError("Room number must be a positive number.")
        return data
    
    def validate_roomfloor(self, data):
        if data < 0:
            raise serializers.ValidationError("Floor number cannot be negative.")
        if data > 20:
            raise serializers.ValidationError("Floor number cannot be more than 20.")
        return data
    
    def validate_roombaseprice(self, data):
        if data < 0:
            raise serializers.ValidationError("Room price cannot be negative.")
        if data > 1000:
            raise serializers.ValidationError("Room price seems unrealistically high.")
        return data
        
    def validate_stateroomtypeid(self, data):
        # Lookup the room type based on the name (or another attribute)
        room_type = models.MmsRoomType.objects.filter(stateroomtype=data).first()
        if not room_type:
            raise serializers.ValidationError(f"Invalid room type: {data}")
        return room_type  # Store the ID in the model

    def validate_locid(self, data):
        # Lookup the location based on the name (or another attribute)
        location = models.MmsRoomLoc.objects.filter(location=data).first()
        if not location:
            raise serializers.ValidationError(f"Invalid location: {data}")
        return location  # Store the ID in the model
    
class MmsRoomCreateUpdateSerializer(MmsRoomBaseSerializer):
    
    def create(self, validated_data):
        """
        Create a new room using the validated data.
        """
        return models.MmsRoom.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Update fields on the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class MmsRoomCSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, file):
        import csv
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        rows = []
        errors = {}
        for i, row in enumerate(reader, start=1):
            serializer = MmsRoomBaseSerializer(data=row)
            if serializer.is_valid():
                rows.append(serializer.validated_data)
            else:
                # You may want to include the row number in the error message for better clarity
                errors[i] = serializer.errors

        if errors:
            raise serializers.ValidationError({"row_errors": errors})

        return rows

    def create(self, validated_data):
        with transaction.atomic():
            try: 
                # Extract rows from the validated data
                rows = validated_data['file']

                # Bulk create MmsRoom instances
                rooms = [models.MmsRoom(**room_data) for room_data in rows]
                created_rooms = models.MmsRoom.objects.bulk_create(rooms)

                return created_rooms

            except Exception as e:
                raise serializers.ValidationError(f"Bulk create failed: {str(e)}")
    
class MmsRoomBulkUpdateSerializer(serializers.Serializer):
    rooms = serializers.ListField(
        child=serializers.DictField(),  # Use a DictField for simplicity
        allow_empty=False
    )

    def validate_rooms(self, data):
        #print(data)
        validated_data = []
        
        for room_data in data:
            # Validate using the base serializer logic
            #print(room_data)
            serializer = MmsRoomBaseSerializer(data=room_data)
            #print(serializer)
            serializer.is_valid(raise_exception=True)
            validated_data.append(serializer.validated_data)
            

        return validated_data
    

    def update(self, instance, validated_data):
        updated_instances = []

        for data in validated_data:
            # Match the roomnumber
            if instance.roomnumber == data.get("roomnumber"):
                # Update instance attributes
                for attr, value in data.items():
                    setattr(instance, attr, value)
                instance.save()  # Save the updated instance to the database
                updated_instances.append(instance)
    

        return updated_instances
        
class MmsRoomListSerializer(serializers.ModelSerializer):
    roomtype = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = models.MmsRoom
        fields = ['roomnumber', 'roomfloor', 'roombaseprice', 'roomtype', 'location']
        
    def get_roomtype(self, obj):
        """
        Retrieve the room type from the related stateroom type table.
        """
        return obj.stateroomtypeid.stateroomtype if obj.stateroomtypeid else None
    
    def get_location(self, obj):
        """
        Retrieve the location from the related location table.
        """
        return obj.locid.location if obj.locid else None

class MmsPackageCreateUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.MmsPackage
        fields = '__all__'
    
    def validate_packageid(self, data):
        """
        Validate that the location ID is unique.
        Allow the current object to keep the same location ID during updates.
        """
        if models.MmsPackage.objects.filter(packageid=data).exclude(packageid=data).exists():
            raise serializers.ValidationError("A package with this package ID already exists.")
        
        return data
        
    def validate_packagename(self, data):

        # Validate location 
        valid_types = [' hydration plus', 'cheers unlimited', 'connected traveler', 'internet freedom', 'gourmet feast']
        if data.lower() not in valid_types:
            raise serializers.ValidationError(f"Package has to be one of {valid_types}")
        
        if models.MmsPackage.objects.filter(packagename=data).exists():
            raise serializers.ValidationError("A package with this package name already exists.")
        return data
    
    def validate_base_price(self, data):
        if data <= 0:
            raise ValidationError("Base price must be a positive value.")
        # Optionally, set a maximum price
        if data> 1000:
            raise ValidationError("Base price seems unrealistically high.")
        
        return data
    
    def validate_packagedetails(self, data):
        if len(data) < 10:
             raise ValidationError("Package details must be at least 10 characters long.")
        if len(data) > 150:
            raise ValidationError("Package details must be less than 150 characters long.")
        
        return data

    '''def create(self, validated_data):
        return models.MmsPackage.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Update fields on the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance'''

class MmsPackageListSerializer(serializers.ModelSerializer):
    # Nested serializer for related start port (via MmsPortStop and MmsPort)

    class Meta:
        model = models.MmsPackage
        fields = '__all__'
                                     
class MmsPortStopCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MmsPortStop
        fields = ['arrivaltime', 'departuretime', 'orderofstop', 'isstartport', 'isendport']
    
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
        trip = models.MmsPortStop.objects.create(**validated_data)
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
        fields = ['tripname', 'startdate', 'enddate', 'tripcostperperson', 'tripstatus', 'capacity']
    
    def validate_tripid(self, data):
        trip_id = self.instance.tripid if self.instance else None
        if models.MmsTrip.objects.filter(tripid=data).exclude(tripid=trip_id).exists():
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
        trip = models.MmsTrip.objects.create(**validated_data)
        return trip
    
    def update(self, instance, validated_data):
        # Update trip fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class MmsTripListSerializer(serializers.ModelSerializer):
    # Nested serializer for related start port (via MmsPortStop and MmsPort)
    port_stops = serializers.SerializerMethodField()

    class Meta:
        model = models.MmsTrip
        fields = ['tripid', 'tripname', 'startdate', 'enddate', 'tripcostperperson', 'port_stops']
    
    def get_port_stops(self, obj):
        """
        Fetch all port stops with their details and order them.
        """
        port_stops = obj.portstop.all().order_by('orderofstop')
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
        
# User related features
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
            models.MmsUserProfile.objects.create(userid=user.pk, **profile_data)
        
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
            profile_instance = models.MmsUserProfile.objects.get(userid=instance.id)  
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

'''class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Check if the username exists
        username = attrs.get('username')
        password = attrs.get('password')
        user = None

        try:
            # Try fetching the user by username
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # If the user doesn't exist, raise an appropriate error
            raise AuthenticationFailed('No account found with that username.')
        
        # Check if the password is correct
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password.')
        
        # If everything is fine, call the parent class's validate method
        data = super().validate(attrs)
        
        # Add custom claims (username and email) to the token payload
        data['username'] = user.username
        data['email'] = user.email
        
        return data'''

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        identifier = attrs.get('username')  # Can be email or username
        password = attrs.get('password')

        user = None

        # Check if the identifier is an email
        if re.match(r"[^@]+@[^@]+\.[^@]+", identifier):
            try:
                # Fetch user by email
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                raise AuthenticationFailed('No account found with that email.')
        else:
            try:
                # Fetch user by username
                user = User.objects.get(username=identifier)
            except User.DoesNotExist:
                raise AuthenticationFailed('No account found with that username.')
        
        # Restrict access to staff and admin accounts
        if user.is_staff or user.is_superuser:
            raise AuthenticationFailed('Only regular users are allowed to log in.')

        # Authenticate user explicitly using username and password
        user = authenticate(username=user.username, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials.')

        # Call the parent method to generate tokens
        data = super().validate({"username": user.username, "password": password})

        # Add custom claims
        data['username'] = user.username
        data['email'] = user.email

        return data

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Check if the email exists in the database
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value
           