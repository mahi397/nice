import re
import csv
from . import models
from rest_framework import status
from django.db import transaction
from datetime import date, datetime
from rest_framework import serializers 
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError, AuthenticationFailed


# Admin related features

class AdminLoginSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for admin login.
    Validates login credentials (email or username) and generates JWT tokens for authenticated users.
    """
    def validate(self, attrs):
        # Extract username or email and password from the request attributes
        identifier = attrs.get('username')  # Can be email or username
        password = attrs.get('password')

        user = None  # Initialize the user variable

        # Check if the identifier is an email (using a simple regex to match email format)
        if re.match(r"[^@]+@[^@]+\.[^@]+", identifier):
            try:
                # Fetch user by email if identifier is an email
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                # Raise an error if no user is found with the provided email
                raise AuthenticationFailed('No account found with that email.')
        else:
            try:
                # Fetch user by username if the identifier is not an email
                user = User.objects.get(username=identifier)
            except User.DoesNotExist:
                # Raise an error if no user is found with the provided username
                raise AuthenticationFailed('No account found with that username.')

        # Restrict access to only staff and admin accounts (checking if user is staff or admin)
        if not user.is_staff and not user.is_superuser:
            # Raise error if the user is neither staff nor admin
            raise AuthenticationFailed('Only staff and admin accounts are allowed to log in.')

        # Authenticate the user explicitly by checking if the username and password are correct
        user = authenticate(username=user.username, password=password)
        if not user:
            # Raise error if the authentication fails (invalid credentials)
            raise AuthenticationFailed('Invalid credentials.')

        # Call the parent class's `validate` method to generate tokens for the authenticated user
        data = super().validate({"username": user.username, "password": password})

        # Add custom claims to the token data
        data['username'] = user.username  # Add username to the token data
        data['email'] = user.email  # Add email to the token data
        if user.is_staff:
            data['is_staff'] = user.is_staff  # Add is_staff claim if the user is a staff member
        else:
            data['is_superuser'] = user.is_superuser  # Add is_superuser claim if the user is a superuser

        return data

class MmsPortSerializer(serializers.ModelSerializer):
    """
    Serializer to handle port details.
    Includes custom validation for required fields and data integrity.
    """

    class Meta:
        model = models.MmsPort  # The model associated with this serializer is MmsPort
        fields = [
            'portname', 'address', 'portcity', 'portstate', 'portcountry', 
            'nearestairport', 'parkingspots'
        ]
        
    def validate_portname(self, data):
        """
        Validate the portname field.
        - Ensures the port name is not empty.
        - Checks that the port name is unique.
        """
        if not data or data.strip() == "":
            # Raise error if portname is empty
            raise ValidationError("Port name cannot be empty.")
        if models.MmsPort.objects.filter(portname=data).exists():
            # Check if the portname already exists in the database
            raise ValidationError(f"A port with name {data} already exists.")
        return data

    def validate_address(self, data):
        """
        Validate the address field.
        - Ensures the address is not empty.
        """
        if not data or data.strip() == "":
            # Raise error if address is empty
            raise ValidationError("Address cannot be empty.")
        return data

    def validate_portcity(self, data):
        """
        Validate the portcity field.
        - Ensures the city is not empty.
        """
        if not data or data.strip() == "":
            # Raise error if portcity is empty
            raise ValidationError("Port city cannot be empty.")
        return data

    def validate_portstate(self, data):
        """
        Validate the portstate field.
        - Ensures the state is not empty.
        """
        if not data or data.strip() == "":
            # Raise error if portstate is empty
            raise ValidationError("Port state cannot be empty.")
        return data

    def validate_portcountry(self, data):
        """
        Validate the portcountry field.
        - Ensures the country is not empty.
        - Optionally, a check could be added to verify if the country is valid.
        """
        if not data or data.strip() == "":
            # Raise error if portcountry is empty
            raise ValidationError("Port country cannot be empty.")
        # Optional: Add a check here to validate against a list of countries if needed
        return data

    def validate_nearestairport(self, data):
        """
        Validate the nearestairport field.
        - Ensures the nearest airport is not empty.
        """
        if not data or data.strip() == "":
            # Raise error if nearestairport is empty
            raise ValidationError("Nearest airport cannot be empty.")
        return data

    def validate_parkingspots(self, data):
        """
        Validate the parkingspots field.
        - Ensures the number of parking spots is a non-negative integer.
        """
        if data < 0:
            # Raise error if parkingspots is a negative integer
            raise ValidationError("Parking spots must be a non-negative integer.")
        return data

    def validate(self, attrs):
        """
        Custom validation for the entire port.
        Ensures all the required fields are provided.
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
            # Raise an error if any of the fields are missing
            raise serializers.ValidationError("All port details are required.")
        return attrs

    def create(self, validated_data):
        """
        Create a new port with the validated data.
        """
        return models.MmsPort.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update an existing port with the validated data.
        - Iterates through the validated data and updates the instance.
        """
        for attr, value in validated_data.items():
            # Update each attribute of the instance with the new value
            setattr(instance, attr, value)
        # Save the updated instance
        instance.save()
        return instance
    
class MmsPortListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing the ports. This serializer is used for rendering data for the port list view.
    It includes all fields from the MmsPort model to represent port details.
    """

    class Meta:
        model = models.MmsPort  # Specifies the model that this serializer will use, which is MmsPort
        fields = '__all__'  # Includes all fields from the MmsPort model in the serialized data
            
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
        # Ensure the description is not empty or just whitespace
        if not data or data.strip() == "":
            raise ValidationError("Restaurant description cannot be empty.")
        
        # Ensure the description does not exceed the maximum length
        if len(data) > 300:
            raise ValidationError("Restaurant description must not exceed 300 characters.")
        
        if not re.match(r'^[a-zA-Z0-9.,!?\-]*$', data):
            raise ValidationError("Restaurant description contains invalid characters.")
        
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
        fields = ['stateroomtype', 'roomsize', 'numberofbeds', 'numberofbaths', 'numberofbalconies', 'roomtypedescription']
    
    
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
    
    def validate_roomtypedescription(self, data):
        # Ensure the description is not empty or just whitespace
        if not data or data.strip() == "":
            raise ValidationError("Room type description cannot be empty.")
        
        # Ensure the description does not exceed the maximum length
        if len(data) > 500:
            raise ValidationError("Room type description must not exceed 300 characters.")
        
        if not re.match(r'^[a-zA-Z0-9.,!? ]*$', data):
            raise ValidationError("Room type description contains invalid characters.")
        
        return data
        
    def create(self, validated_data):
        return models.MmsRoomType.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Update fields on the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class MmsRoomTypeListSerializer(serializers.ModelSerializer):
    # Nested serializer for related start port (via MmsPortStop and MmsPort)

    class Meta:
        model = models.MmsRoomType
        fields = '__all__'

class MmsRoomBaseSerializer(serializers.ModelSerializer):
    # Expecting IDs to be passed for stateroom type, location, and ship
    stateroomtypeid = serializers.IntegerField()
    locid = serializers.IntegerField()

    
    class Meta:
        model = models.MmsRoom
        fields = ['roomnumber', 'roomfloor', 'price', 'stateroomtypeid', 'locid']

    def validate_roomnumber(self, data):
        # Check if room number is valid (positive and unique)
        if data < 0:
            raise serializers.ValidationError("Room number must be a positive number.")
        
        if models.MmsRoom.objects.filter(roomnumber=data).exists():
            raise serializers.ValidationError("A room with this room number already exists.")
        
        return data
    
    def validate_roomfloor(self, data):
        # Validate floor number (positive and within valid range)
        if data < 0:
            raise serializers.ValidationError("Floor number cannot be negative.")
        if data > 20:
            raise serializers.ValidationError("Floor number cannot be more than 20.")
        
        return data
    
    def validate_price(self, data):
        # Validate price (positive and reasonable)
        if data < 0:
            raise serializers.ValidationError("Room price cannot be negative.")
        if data > 1000:
            raise serializers.ValidationError("Room price seems unrealistically high.")
        
        return data
            
    def validate_stateroomtypeid(self, data):
        # Ensure stateroomtypeid exists in the MmsRoomType table
        try:
            room_type = models.MmsRoomType.objects.get(stateroomtypeid=data)
        except models.MmsRoomType.DoesNotExist:
            raise serializers.ValidationError(f"Invalid stateroom type ID: {data}")
        
        return room_type  # Returning the room type object for the foreign key
    
    def validate_locid(self, data):
        # Ensure locid exists in the MmsRoomLoc table
        try:
            location = models.MmsRoomLoc.objects.get(locid=data)
        except models.MmsRoomLoc.DoesNotExist:
            raise serializers.ValidationError(f"Invalid location ID: {data}")
        
        return location  # Returning the location object for the foreign key
   
class MmsRoomCSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
    
    def validate_file(self, file):
        # Read and decode the uploaded CSV file
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        rows = []
        errors = {}
        for i, row in enumerate(reader, start=1):
            # Here we pass the row data to the room base serializer for validation
            room_serializer = MmsRoomBaseSerializer(data=row)
            if room_serializer.is_valid():
                rows.append(room_serializer.validated_data)
            else:
                # Capture errors along with the row number
                errors[i] = room_serializer.errors

        if errors:
            raise serializers.ValidationError({"row_errors": errors})

        return rows

    def create(self, validated_data):
        # Bulk create rooms after validation
        rooms_data = validated_data.get('file', [])
        rooms = [models.MmsRoom(**room_data) for room_data in rooms_data]
        created_rooms = models.MmsRoom.objects.bulk_create(rooms)
        return created_rooms
                                    
class MmsRoomsCreateSerializer(serializers.ModelSerializer):
    rooms = MmsRoomBaseSerializer(many=True, required=False)
    csv_file = serializers.FileField(write_only=True, required=False, allow_null=True)
    

    class Meta:
        model = models.MmsRoom
        fields = ['rooms', 'csv_file']

    '''def validate_shipid(self, data):
        """
        Ensure the ship exists before processing rooms.
        """
        try:
            ship = models.MmsShip.objects.get(shipid=data)
            #print(ship)
        except models.MmsShip.DoesNotExist:
            raise serializers.ValidationError("Ship with this ID does not exist.")
        return ship  # Return the ship instance for later use'''

    def validate(self, data):
        """
        Ensure that either `rooms` or `csv_file` is provided, but not both.
        """
        rooms = data.get('rooms', None)
        csv_file = data.get('csv_file', None)
        if not rooms and not csv_file:
            raise serializers.ValidationError("You must provide either `rooms` data or a `csv_file`.")
        if rooms and csv_file:
            raise serializers.ValidationError("You cannot provide both `rooms` data and a `csv_file`.")
        return data

    @transaction.atomic
    def create(self, validated_data):
        """
        Handles creation of rooms.
        """

        rooms_data = validated_data.get('rooms', [])
        csv_file = validated_data.get('csv_file', None)

        if rooms_data:
            # Handle nested room creation
            for room_data in rooms_data:
                models.MmsRoom.objects.create(**room_data)

        elif csv_file:
            # Handle CSV upload
            csv_serializer = MmsRoomCSVUploadSerializer(data={'file': csv_file})
            if csv_serializer.is_valid(raise_exception=True):
                validated_rows = csv_serializer.validated_data['file']
                for row in validated_rows:
                    models.MmsRoom.objects.create(**row)

        return {"message": "Rooms added successfully."}
        
class MmsRoomListSerializer(serializers.ModelSerializer):
    roomtype = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = models.MmsRoom
        fields = ['roomnumber', 'roomfloor', 'price', 'roomtype', 'location']
        
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
                                               
class MmsShipActivitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.MmsShipActivity
        fields = ['shipid', 'activityid']
        
    def validate(self, data):
        # Ensure unique combination of ship and activity
        if models.MmsShipActivity.objects.filter(shipid=data['shipid'], activityid=data['activityid']).exists():
            raise serializers.ValidationError(
                f"Activity {data['activityid'].activityname} already exists for ship {data['shipid'].shipname}."
            )
        return data

class MmsShipRestaurantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.MmsShipRestaurant
        fields = ['shipid', 'restaurantid']
        
    def validate(self, data):
        # Ensure unique combination of ship and activity
        if models.MmsShipRestaurant.objects.filter(shipid=data['shipid'], restaurantid=data['restaurantid']).exists():
            raise serializers.ValidationError(
                f"Activity {data['restaurantid'].restaurantname} already exists for ship {data['shipid'].shipname}."
            )
        return data

class MmsShipRoomsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.MmsShipRoom
        fields = ['shipid', 'roomnumber']
        
    def validate(self, data):
        # Ensure unique combination of ship and activity
        if models.MmsShipRoom.objects.filter(shipid=data['shipid'], roomnumber=data['roomnumber']).exists():
            raise serializers.ValidationError(
                f"Activity {data['roomnumber']} already exists for ship {data['shipid'].shipname}."
            )
        return data    
        
class MmsShipCreateSerializer(serializers.ModelSerializer):
    activities = serializers.ListField(child=serializers.DictField(), required=False)
    restaurants = serializers.ListField(child=serializers.DictField(), required=False)
    rooms = serializers.ListField(child=serializers.DictField(), required=False)
    
    class Meta:
        model = models.MmsShip
        fields = ['shipid', 'shipname', 'description', 'capacity', 'activities', 'restaurants', 'rooms']
        
    def validate_shipname(self, data):
        # Ensure portname is a non-empty string
        if not data or data.strip() == "":
            raise ValidationError("ship name cannot be empty.")
        
        if len(data) > 45:
            raise serializers.ValidationError("ship name cannot exceed 45 characters.")
        
        if models.MmsShip.objects.filter(shipname=data).exists():
            raise ValidationError(f"A ship with name {data} already exists.")
        return data 
    
    def validate_description(self, data):
        # Ensure the description is not empty or just whitespace
        if not data or data.strip() == "":
            raise ValidationError("Ship description cannot be empty.")
        
        # Ensure the description does not exceed the maximum length
        if len(data) > 150:
            raise ValidationError("Ship description must not exceed 150 characters.")
        
        if not re.match(r'^[a-zA-Z0-9.,!? \-]*$', data):
            raise ValidationError("Ship description contains invalid characters.")
        
        return data
    
    def validate_capacity(self, data):
        if data <= 0:
            raise serializers.ValidationError("Capacity must be a positive number.")
        return data
    
    def create_ship_activities(self, ship, activities):
        if activities:
            for activity in activities:
                activity_id = activity.get('activityid')
                if activity_id:  # Ensure ID is present
                    activity = models.MmsActivity.objects.get(activityid=activity_id)
                    models.MmsShipActivity.objects.create(shipid=ship, activityid=activity)

    def create_ship_restaurants(self, ship, restaurants):
        if restaurants:
            for restaurant in restaurants:
                restaurant_id = restaurant.get('restaurantid')
                if restaurant_id:  # Ensure ID is present
                    restaurant = models.MmsRestaurant.objects.get(restaurantid=restaurant_id)
                    models.MmsShipRestaurant.objects.create(shipid=ship, restaurantid=restaurant)
    
    def create_ship_rooms(self, ship, rooms):
        if rooms:
            for room in rooms:
                room_number = room.get('roomnumber')
                if room_number:  # Ensure room number is present
                    try:
                        room_instance = models.MmsRoom.objects.get(roomnumber=room_number)
                    except models.MmsRoom.DoesNotExist:
                        raise serializers.ValidationError(f"Room with number {room_number} does not exist.")
                    
                    models.MmsShipRoom.objects.create(shipid=ship, roomnumber=room_instance)
                    
    @transaction.atomic
    def create(self, validated_data): 
        activities = validated_data.pop('activities', [])
        restaurants = validated_data.pop('restaurants', [])
        rooms = validated_data.pop('rooms', [])
        # Save the ship first
        
        ship = models.MmsShip.objects.create(**validated_data)
        ship.save()

        self.create_ship_activities(ship, activities)
        self.create_ship_restaurants(ship, restaurants)
        self.create_ship_rooms(ship, rooms)
        
        return ship

class MmsShipListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.MmsShip
        fields = '__all__'  
         
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
        valid_types = ['hydration plus', 'cheers unlimited', 'connected traveler', 'internet freedom', 'gourmet feast']
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

    def create(self, validated_data):
        return models.MmsPackage.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Update fields on the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class MmsPackageListSerializer(serializers.ModelSerializer):
    # Nested serializer for related start port (via MmsPortStop and MmsPort)

    class Meta:
        model = models.MmsPackage
        fields = '__all__'
                                     
class MmsItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MmsPortStop
        fields = ['tripid', 'portid', 'arrivaltime', 'departuretime', 'orderofstop', 'isstartport', 'isendport', 'description']

    def validate_description(self, data):
        # Ensure the description is not empty or just whitespace
        if not data or data.strip() == "":
            raise ValidationError("Stop description cannot be empty.")
        
        # Ensure the description does not exceed the maximum length
        if len(data) > 300:
            raise ValidationError("Stop description must not exceed 300 characters.")
        
        if not re.match(r'^[a-zA-Z0-9.,!?\-]*$', data):
            raise ValidationError("Stop description contains invalid characters.")
        
        return data
    
    def validate_orderofstop(self, data):
        if data < 0:
            raise serializers.ValidationError("Stop number cannot be negative")
        return data
        
    def validate(self, data):
        # Validate the data
        self.validate_is_boolean(data)
        self.validate_arrival_before_departure(data)
        self.validate_order_of_stop(data)
        self.validate_trip_has_start_and_end_port(data)
        
        if data.get('isstartport'):
            if data.get('arrivaltime'):
                raise ValidationError("Arrival time is not needed for the start port.")
            if not data.get('departuretime'):
                raise ValidationError("Departure time is required for the start port.")

        # Validate end port conditions
        if data.get('isendport'):
            if data.get('departuretime'):
                raise ValidationError("Departure time is not needed for the end port.")
            if not data.get('arrivaltime'):
                raise ValidationError("Arrival time is required for the end port.")

        # Validate intermediate ports
        if not data.get('isstartport') and not data.get('isendport'):
            if not data.get('arrivaltime') or not data.get('departuretime'):
                raise ValidationError("Both arrival and departure times are required for intermediate ports.")

        return data

    def validate_is_boolean(self, data):
        """Ensure that `isstartport` and `isendport` are boolean values."""
        if not isinstance(data.get('isstartport'), bool):
            raise serializers.ValidationError("isstartport must be a boolean value.")
        if not isinstance(data.get('isendport'), bool):
            raise serializers.ValidationError("isendport must be a boolean value.")

    def validate_arrival_before_departure(self, data):
        """Ensure arrival time is before departure time."""
        if data.get('arrivaltime') and data.get('departuretime') and data['arrivaltime'] >= data['departuretime']:
            raise serializers.ValidationError("Arrival time must be before departure time.")

    def validate_order_of_stop(self, data):
    
        """Ensure `orderofstop` is sequential and does not skip numbers."""
        tripid = data['tripid']
        order_of_stop = data['orderofstop']
        
        # Check if this is the first stop being created for the trip
        existing_stops = models.MmsPortStop.objects.filter(tripid=tripid).order_by('orderofstop')
        existing_order_of_stop = [stop.orderofstop for stop in existing_stops]

        # Ensure that order of stops is sequential (1, 2, 3, ...)
        if order_of_stop != len(existing_order_of_stop) + 1:
            raise serializers.ValidationError(f"Order of stop must be sequential. Next available stop number is {len(existing_order_of_stop) + 1}.")

    def validate_trip_has_start_and_end_port(self, data):
        """Ensure every trip has both a start port and an end port."""
        tripid = data['tripid']
        
        # Check if this trip has a start port and an end port in the current port stops
        start_ports = models.MmsPortStop.objects.filter(tripid=tripid, isstartport=True)
        end_ports = models.MmsPortStop.objects.filter(tripid=tripid, isendport=True)
        
        # Ensure there is at least one start port and one end port
        if not start_ports.exists():
            raise serializers.ValidationError(f"Trip {tripid} must have a start port.")
        if not end_ports.exists():
            raise serializers.ValidationError(f"Trip {tripid} must have an end port.")

class MmsTrippackageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.MmsTripPackage
        fields = ['tripid', 'packageid']
        
    def validate_packageid(self, data):
        if not models.MmsPackage.objects.filter(packageid=data).exists():
            raise serializers.ValidationError(f"Package ID {data} doesn't exist.")
        
        
    def validate(self, data):
        # Ensure unique combination of ship and activity
        if models.MmsTripPackage.objects.filter(tripid=data['tripid'], packageid=data['packageid']).exists():
            raise serializers.ValidationError(
                f"Activity {data['packageid'].packagename} already exists for trip {data['tripid'].tripname}."
            )
        return data
            
class MmsTripCreateSerializer(serializers.ModelSerializer):
    stops = serializers.ListField(child=serializers.DictField(), required=False)
    packages = serializers.ListField(child=serializers.DictField(), required=False)
                                                       
    class Meta:
        model = models.MmsTrip
        fields = ['tripname', 'startdate', 'enddate', 'tripcostperperson', 'tripstatus', 'tripcapacity', 'cancellationpolicy', 
                  'tripdescription', 'finalbookingdate', 'shipid', 'stops', 'packages']

    def validate_tripname(self, data):
        # Trip name validation: Ensure it's not empty and within length limits
        if not data or data.strip() == "":
            raise ValidationError("Trip name cannot be empty.")
        
        if len(data) > 50:
            raise ValidationError("Trip name cannot exceed 100 characters.")
        
        return data

    def validate_startdate(self, data):
        # Ensure start date is not in the past
        if data < datetime.now().date():
            raise ValidationError("Start date cannot be in the past.")
        
        return data

    def validate_enddate(self, data):
        startdate = self.initial_data.get('startdate')
        if startdate and data < datetime.strptime(startdate, "%Y-%m-%d").date():
            raise ValidationError("End date cannot be before the start date.")
        
        if data < datetime.now().date():
            raise ValidationError("End date cannot be in the past.")
        
        return data

    def validate_tripcostperperson(self, data):
        # Ensure cost per person is a positive number
        if data <= 0:
            raise ValidationError("Trip cost per person must be a positive number.")
        
        return data

    def validate_tripstatus(self, data):
        # Ensure valid trip status
        valid_statuses = ['Scheduled', 'Completed', 'Cancelled', 'Postponed']
        if data not in valid_statuses:
            raise ValidationError(f"Trip status must be one of: {', '.join(valid_statuses)}.")
        
        return data

    def validate_tripcapacity(self, data):
        # Ensure capacity is a positive number
        if data <= 0:
            raise ValidationError("Capacity must be a positive number.")
        
        return data

    def validate_cancellationpolicy(self, data):
        # Ensure cancellation policy is not empty or just whitespace
        if not data or data.strip() == "":
            raise ValidationError("Cancellation policy cannot be empty.")
        
        # Optional: Additional checks for the format of cancellation policy (e.g., a valid text or specific string format)
        if len(data) > 300:
            raise ValidationError("Cancellation policy cannot exceed 500 characters.")
        
        return data

    def validate_tripdescription(self, data):
        # Ensure trip description is not empty and within length limits
        if not data or data.strip() == "":
            raise ValidationError("Trip description cannot be empty.")
        
        if len(data) > 300:
            raise ValidationError("Trip description cannot exceed 300 characters.")
        
        return data

    def validate_finalbookingdate(self, data):
        # Ensure final booking date is not in the past and is before the trip start date
        trip_start_date = self.initial_data.get('startdate')
        if data and data < datetime.now().date():
            raise ValidationError("Final booking date cannot be in the past.")
        
        if trip_start_date and data and data > datetime.strptime(trip_start_date, "%Y-%m-%d").date():
            raise ValidationError("Final booking date must be before the trip start date.")
        
        return data

    
     
    def validate_tripname_and_dates(self, data):
        tripname = data.get('tripname')
        startdate = data.get('startdate')
        enddate = data.get('enddate')

        # Ensure there are no overlapping trips with the same name
        overlapping_trips = models.MmsTrip.objects.filter(
            tripname=tripname,
            startdate__lt=enddate,
            enddate__gt=startdate
        )

        if overlapping_trips.exists():
            raise ValidationError(f"There's already an existing trip named '{tripname}' with overlapping dates.")
        
        return data
    
    def validate(self, data):
        self.validate_trip_start_and_end_dates(data)
        return data

    def validate_trip_start_and_end_dates(self, data):
        startdate = data.get('startdate')
        enddate = data.get('enddate')
        stops = data.get('stops', [])

        # Find start and end ports
        start_port = next((stop for stop in stops if stop.get('isstartport') == 1), None)
        end_port = next((stop for stop in stops if stop.get('isendport') == 1), None)

        if not start_port:
            raise ValidationError("A start port is required.")
        if not end_port:
            raise ValidationError("An end port is required.")
        
        # Validate start date matches start port departure date
        if 'departuretime' in start_port:
            start_departure = datetime.strptime(start_port['departuretime'], "%Y-%m-%dT%H:%M:%SZ").date()
            if startdate != start_departure:
                raise ValidationError(f"Start date must match the departure date of the start port ({start_departure}).")

        # Validate end date matches end port arrival date
        if 'arrivaltime' in end_port:
            end_arrival = datetime.strptime(end_port['arrivaltime'], "%Y-%m-%dT%H:%M:%SZ").date()
            if enddate != end_arrival:
                raise ValidationError(f"End date must match the arrival date of the end port ({end_arrival}).")

        return data
    
    def create_trip_stops(self, trip, stops):
        if stops:
            for stop in stops:
                port_id = stop.pop('portid')
                if port_id:  # Ensure ID is present
                    port = models.MmsPort.objects.get(portid=port_id)
                    order_of_stop = stop.get('orderofstop')
                    if order_of_stop is None:
                        raise ValidationError("Each stop must have an 'orderofstop' value.")
                    models.MmsPortStop.objects.create(tripid=trip, portid=port, **stop)

    def create_trip_packages(self, trip, packages):
        if packages:
            for package in packages:
                package_id = package.get('packageid')
                if package_id:  # Ensure ID is present
                    package_instance = models.MmsPackage.objects.get(packageid=package_id)
                    models.MmsTripPackage.objects.create(tripid=trip, packageid=package_instance)
    
    @transaction.atomic
    def create(self, validated_data): 
        packages = validated_data.pop('packages', [])
        stops = validated_data.pop('stops', [])
        print(validated_data)
        
        trip = models.MmsTrip.objects.create(**validated_data)
    
        self.create_trip_stops(trip, stops)
        self.create_trip_packages(trip, packages)
    
        return trip

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
           