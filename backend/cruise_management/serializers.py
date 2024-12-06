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
    """
    Serializer for creating and updating restaurant data.
    Includes validation for restaurant-specific fields such as name, description, and operational times.
    """
    
    class Meta:
        # Specify the model and fields to include in the serializer
        model = models.MmsRestaurant
        fields = ['restaurantname', 'floornumber', 'openingtime', 'closingtime', 'servesbreakfast',
                  'serveslunch', 'servesdinner', 'servesalcohol', 'restaurant_description']
    
    def validate_restaurantname(self, data):
        """
        Custom validation for the restaurant name.
        Ensures the name is not empty and that the restaurant name is unique.
        """
        # Ensure restaurant name is a non-empty string
        if not data or data.strip() == "":
            raise ValidationError("Restaurant name cannot be empty.")
        
        # Ensure the restaurant name is unique, excluding the current instance for update
        if models.MmsRestaurant.objects.filter(restaurantname=data).exclude(restaurantname=data).exists():
            raise ValidationError(f"A restaurant with name {data} already exists.")
        
        return data
        
    def validate_floornumber(self, data):
        """
        Custom validation for the floor number.
        Ensures the floor number is non-negative.
        """
        if data < 0:
            raise serializers.ValidationError("Floor number cannot be negative.")
        return data

    def validate_restaurant_description(self, data):
        """
        Custom validation for the restaurant description.
        Ensures the description is non-empty, does not exceed 300 characters, 
        and only contains valid characters (letters, numbers, and punctuation).
        """
        # Ensure the description is not empty or just whitespace
        if not data or data.strip() == "":
            raise ValidationError("Restaurant description cannot be empty.")
        
        # Ensure the description does not exceed the maximum length
        if len(data) > 300:
            raise ValidationError("Restaurant description must not exceed 300 characters.")
        
        # Ensure description contains only valid characters
        if not re.match(r'^[a-zA-Z0-9.,!? ]*$', data):
            raise ValidationError("Restaurant description contains invalid characters.")
        
        return data
    
    def validate(self, data):
        """
        General validation for restaurant data.
        Ensures that opening time exists, closing time is later than opening time (if provided),
        and at least one meal service is enabled.
        """
        openingtime = data.get('openingtime')
        closingtime = data.get('closingtime')

        # Validate that opening time is provided
        if not openingtime:
            raise serializers.ValidationError("Opening time is required.")
        
        # Handle optional closing time and ensure it's later than the opening time
        if closingtime:
            if openingtime >= closingtime:
                raise serializers.ValidationError(
                    "Opening time must be earlier than closing time unless the restaurant operates 24 hours."
                )
        
        # Ensure at least one meal service is 'Y' (breakfast, lunch, or dinner)
        if not any([
            data.get('servesbreakfast') == 'Y',
            data.get('serveslunch') == 'Y',
            data.get('servesdinner') == 'Y'
        ]):
            raise serializers.ValidationError("At least one meal service (breakfast, lunch, or dinner) must be 'Y'.")
        
        return data

    def create(self, validated_data):
        """
        Create a new restaurant instance using the validated data.
        """
        return models.MmsRestaurant.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update an existing restaurant instance with the validated data.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class MmsRestaurantListSerializer(serializers.ModelSerializer):
    # Serializer for listing restaurant data. It includes all fields from the MmsRestaurant model.
    # You can customize this by adding specific fields or nested serializers if needed.

    class Meta:
        model = models.MmsRestaurant  # Specifies the model to be serialized (MmsRestaurant).
        fields = '__all__'  # Includes all fields from the MmsRestaurant model in the serialized data. 
        
class MmsActivityCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating or updating activity entries.
    It includes validation logic for activity fields like name, type, description, floor, and capacity.
    """

    class Meta:
        model = models.MmsActivity
        fields = ['activitytype', 'activityname', 'activitydescription', 'floor', 'capacity']
    
    def validate_activityname(self, data):
        """
        Validate the activity name to ensure it's not empty, does not exceed 100 characters,
        and that an activity with the same name doesn't already exist in the database.
        """
        if not data or data.strip() == "":
            raise ValidationError("Activity name cannot be empty.")
        
        if len(data) > 100:
            raise serializers.ValidationError("Activity name cannot exceed 100 characters.")
        
        if models.MmsActivity.objects.filter(activityname=data).exists():
            raise ValidationError(f"An activity with name {data} already exists.")
        return data

    def validate_activitytype(self, data):
        """
        Validate the activity type to ensure it's one of the predefined valid types.
        """
        valid_types = ['sports', 'leisure', 'entertainment']
        if data.lower() not in valid_types:
            raise serializers.ValidationError(f"Invalid activity type. Must be one of {valid_types}.")
        return data
    
    def validate_activitydescription(self, data):
        """
        Validate the activity description to ensure it's not empty, does not exceed 300 characters,
        and does not contain invalid characters.
        """
        if not data or data.strip() == "":
            raise ValidationError("Activity description cannot be empty.")
        
        if len(data) > 300:
            raise ValidationError("Activity description must not exceed 300 characters.")
        
        if not re.match(r'^[a-zA-Z0-9.,!? ]*$', data):
            raise ValidationError("Activity description contains invalid characters.")
        
        return data
    
    def validate_floor(self, data):
        """
        Validate the floor number to ensure it's non-negative and does not exceed 20.
        """
        if data < 0:
            raise serializers.ValidationError("Floor number cannot be negative.")
        if data > 20:
            raise serializers.ValidationError("Floor number cannot exceed 20.")
        return data

    def validate_capacity(self, data):
        """
        Validate the activity's capacity to ensure it's a positive number.
        """
        if data <= 0:
            raise serializers.ValidationError("Capacity must be a positive number.")
        return data

    def validate(self, data):
        """
        Additional validation to ensure the activity's type and capacity are compatible.
        For entertainment activities, the capacity cannot exceed 300. For sports, the capacity cannot exceed 100.
        """
        activitytype = data.get('activitytype')
        capacity = data.get('capacity')

        if activitytype == 'entertainment' and capacity > 300:
            raise serializers.ValidationError("Entertainment activities cannot exceed a capacity of 300.")
        if activitytype == 'sports' and capacity > 100:
            raise serializers.ValidationError("Sports activities cannot exceed a capacity of 100.")
        
        return data
    
    def create(self, validated_data):
        """
        Create a new activity using the validated data.
        """
        return models.MmsActivity.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update an existing activity using the validated data.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class MmsActivityListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing MmsActivity objects.
    This serializer formats the data for the activity list view, 
    including all fields of the MmsActivity model.
    """
    
    class Meta:
        model = models.MmsActivity  # The model to serialize data from
        fields = '__all__'  # Include all fields from the MmsActivity model in the serialization

class MmsRoomLocCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating MmsRoomLoc (room location) instances.
    This serializer handles the validation and transformation of input data 
    for the 'location' field, ensuring it's one of the predefined valid types.
    """
    
    class Meta:
        model = models.MmsRoomLoc  # The model to serialize data from
        fields = ['locid','location']  # Only the 'location' field is included for creation/updating
    
    def validate_location(self, data):
        if data == '' or not data.strip():
            raise serializers.ValidationError("Location field cannot be blank.")
        if models.MmsRoomLoc.objects.filter(location=data).exists():
            raise serializers.ValidationError("The given room location already exists.")
        
        valid_types = ['bow', 'stern', 'port side', 'starboard side']  # Valid location types
        if data.lower() not in valid_types:
            raise serializers.ValidationError(f"Location must be one of {valid_types}.")
        
        return data
    
    @transaction.atomic
    def create(self, validated_data):
        """
        Create a new MmsRoomLoc instance using the validated data.
        """
        return models.MmsRoomLoc.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update an existing MmsRoomLoc instance with the validated data.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class MmsRoomLocListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing MmsRoomLoc instances. This serializer will 
    serialize all fields of MmsRoomLoc, including related fields like 
    foreign keys if present.
    """
    
    class Meta:
        model = models.MmsRoomLoc
        fields = '__all__'  # Serialize all fields of the model
       
class MmsRoomTypeCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating MmsRoomType instances.
    It validates fields such as stateroom type, room size, number of beds/baths, and descriptions.
    """
    
    class Meta:
        model = models.MmsRoomType
        fields = ['stateroomtype', 'roomsize', 'numberofbeds', 'numberofbaths', 'numberofbalconies', 'roomtypedescription', 'baseprice']
    
    def validate_stateroomtype(self, data):
        """
        Validate that the stateroom type is not empty and is a valid type.
        """
        if not data.strip():
            raise serializers.ValidationError("Stateroom type cannot be empty or whitespace.")
        
        if models.MmsRoomType.objects.filter(stateroomtype=data).exists():
            raise serializers.ValidationError("The given room type already exists.")
        pass
        valid_types = ['the haven suite', 'club balcony suite', 'family large balcony', 'family balcony', 'oceanview window', 'inside stateroom', 'studio stateroom']
        
        if data.lower() not in valid_types:
            raise serializers.ValidationError(f"Invalid stateroom type. Must be one of {valid_types}.")
        
        return data
    
    def validate_roomsize(self, data):
        """
        Validate room size to ensure it's a positive value within reasonable limits.
        """
        if data <= 0:
            raise serializers.ValidationError("Room size must be a positive value.")
        if data > 10000:  # Arbitrary upper limit for room size
            raise serializers.ValidationError("Room size seems unrealistically large.")
        return data

    def validate_numberofbeds(self, data):
        """
        Validate that the number of beds is realistic (between 1 and 10).
        """
        if data <= 0:
            raise serializers.ValidationError("Number of beds must be at least 1.")
        if data > 10:
            raise serializers.ValidationError("Number of beds seems unrealistically high.")
        return data
    
    def validate_numberofbaths(self, data):
        """
        Validate the number of bathrooms to ensure realistic values.
        """
        if data <= 0:
            raise serializers.ValidationError("Number of bathrooms must be at least 0.5.")
        if data > 5:
            raise serializers.ValidationError("Number of bathrooms seems unrealistically high.")
        return data

    def validate_numberofbalconies(self, data):
        """
        Validate the number of balconies to ensure they are non-negative and realistic.
        """
        if data < 0:
            raise serializers.ValidationError("Number of balconies cannot be negative.")
        if data > 3:
            raise serializers.ValidationError("Number of balconies seems unrealistically high.")
        return data
    
    def validate_roomtypedescription(self, data):
        """
        Ensure the room type description is not empty, doesn't exceed length limits, and contains valid characters.
        """
        if not data or data.strip() == "":
            raise serializers.ValidationError("Room type description cannot be empty.")
        
        if len(data) > 500:
            raise serializers.ValidationError("Room type description must not exceed 500 characters.")
        
        if not re.match(r'^[a-zA-Z0-9.,!? ]*$', data):
            raise serializers.ValidationError("Room type description contains invalid characters.")
        
        return data
    
    def validate_basepirce(self, data):
        """
        Validates the room price.
        Ensures that the price is a positive value and does not exceed a high limit (1000 in this case).
        """
        if data <= 0:
            raise serializers.ValidationError("Room type price cannot be zero or a negative number.")  
        
        if data > 1000:
            raise serializers.ValidationError("Room price seems unrealistically high.")
        
        return data
        
    def create(self, validated_data):
        """
        Create a new room type instance with validated data.
        """
        return models.MmsRoomType.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update the existing room type instance with validated data.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class MmsRoomTypeListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing MmsRoomType instances. This serializer will serialize
    all fields of the MmsRoomType model, including related fields if present.
    """
    
    class Meta:
        model = models.MmsRoomType
        fields = '__all__'  # Serialize all fields of the model

class MmsRoomBaseSerializer(serializers.ModelSerializer):
    """
    Serializer for handling room details.
    This serializer expects IDs to be passed for stateroom type, location, and ship.
    It validates the room number, floor, and ensures the associated stateroom type and location IDs are valid.
    """
    
    # Expecting IDs to be passed for stateroom type, location, and ship
    stateroomtypeid = serializers.IntegerField()
    locid = serializers.IntegerField()

    class Meta:
        model = models.MmsRoom
        fields = ['roomnumber', 'roomfloor', 'stateroomtypeid', 'locid']
    
    def validate_roomnumber(self, data):
        """
        Validates the room number to ensure it is positive and unique.
        Raises a validation error if the room number is negative or already exists in the database.
        """
        if data < 0:
            raise serializers.ValidationError("Room number must be a positive number.")
        
        # Check if room number already exists in the database
        if models.MmsRoom.objects.filter(roomnumber=data).exists():
            raise serializers.ValidationError("A room with this room number already exists.")
        
        return data
    
    def validate_roomfloor(self, data):
        """
        Validates the room floor number.
        Ensures that the floor number is not negative and doesn't exceed a reasonable limit (20 in this case).
        """
        if data < 0:
            raise serializers.ValidationError("Floor number cannot be negative.")
        if data > 20:
            raise serializers.ValidationError("Floor number cannot be more than 20.")
        
        return data
            
    def validate_stateroomtypeid(self, data):
        """
        Validates the stateroom type ID to ensure it exists in the MmsRoomType table.
        Raises a validation error if the provided ID doesn't match any existing stateroom type.
        """
        try:
            room_type = models.MmsRoomType.objects.get(stateroomtypeid=data)
        except models.MmsRoomType.DoesNotExist:
            raise serializers.ValidationError(f"Invalid stateroom type ID: {data}")
        
        return room_type  # Returning the room type object for the foreign key
    
    def validate_locid(self, data):
        """
        Validates the location ID to ensure it exists in the MmsRoomLoc table.
        Raises a validation error if the provided ID doesn't match any existing location.
        """
        try:
            location = models.MmsRoomLoc.objects.get(locid=data)
        except models.MmsRoomLoc.DoesNotExist:
            raise serializers.ValidationError(f"Invalid location ID: {data}")
        
        return location  # Returning the location object for the foreign key
       
class MmsRoomCSVUploadSerializer(serializers.Serializer):
    """
    Serializer to handle the upload and validation of CSV files for room data.
    This serializer reads the uploaded CSV file, validates the data for each room, 
    and allows for bulk creation of valid room entries in the database.
    """
    
    # A file field to handle the CSV file upload. It is not required, hence `required=False`.
    file = serializers.FileField(required=False)
    
    def validate_file(self, file):
        """
        Validate the uploaded CSV file.
        Reads the file, decodes it into lines, and validates each row using the MmsRoomBaseSerializer.
        If any validation errors are found, it collects them and raises a validation error.
        """
        # Read and decode the uploaded CSV file
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        rows = []  # To store validated room data
        errors = {}  # To store errors along with row numbers
        
        # Loop through each row in the CSV file
        for i, row in enumerate(reader, start=1):
            # Pass each row to the MmsRoomBaseSerializer for validation
            room_serializer = MmsRoomBaseSerializer(data=row)
            
            if room_serializer.is_valid():
                # If the row is valid, add the validated data to rows
                rows.append(room_serializer.validated_data)
            else:
                # If the row is invalid, capture the errors along with the row number
                errors[i] = room_serializer.errors

        # If there are errors, raise a validation error with the details
        if errors:
            raise serializers.ValidationError({"row_errors": errors})

        return rows  # Return the validated room data
    
    def create(self, validated_data):
        """
        Create room instances in bulk using the validated data from the CSV file.
        This method is called after the data is validated and the `validate_file` method 
        has returned the rows of validated data.
        """
        # Retrieve room data from the validated CSV content
        rooms_data = validated_data.get('file', [])
        
        # Prepare a list of room instances to be created in bulk
        rooms = [models.MmsRoom(**room_data) for room_data in rooms_data]
        
        # Bulk create rooms and return the created room instances
        created_rooms = models.MmsRoom.objects.bulk_create(rooms)
        return created_rooms
                                    
class MmsRoomsCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating multiple room entries.
    It allows for both nested room data and CSV file uploads as input.
    The validation ensures that either `rooms` data or a `csv_file` is provided, but not both.
    """

    # Field for accepting nested room data (list of rooms).
    rooms = MmsRoomBaseSerializer(many=True, required=False)
    
    # Field for accepting a CSV file for room data upload.
    csv_file = serializers.FileField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = models.MmsRoom
        fields = ['rooms', 'csv_file']

    def validate(self, data):
        """
        Ensure that either `rooms` or `csv_file` is provided, but not both.
        This is a custom validation logic to ensure consistency in input data.
        """
        rooms = data.get('rooms', None)
        csv_file = data.get('csv_file', None)

        # Ensure that at least one of `rooms` or `csv_file` is provided
        if not rooms and not csv_file:
            raise serializers.ValidationError("You must provide either `rooms` data or a `csv_file`.")

        # Ensure that both `rooms` and `csv_file` are not provided simultaneously
        if rooms and csv_file:
            raise serializers.ValidationError("You cannot provide both `rooms` data and a `csv_file`.")

        return data

    @transaction.atomic
    def create(self, validated_data):
        """
        Handles the creation of rooms from either `rooms` data or a `csv_file`.
        Uses a transaction to ensure atomicity—either all rooms are created, 
        or none are if an error occurs.
        """
        rooms_data = validated_data.get('rooms', [])
        csv_file = validated_data.get('csv_file', None)
        created_rooms = []

        if rooms_data:
            # If room data is provided, create rooms from the nested data
            for room_data in rooms_data:
                created_rooms.append(models.MmsRoom.objects.create(**room_data))

        elif csv_file:
            # If a CSV file is provided, process it using the MmsRoomCSVUploadSerializer
            csv_serializer = MmsRoomCSVUploadSerializer(data={'file': csv_file})
            if csv_serializer.is_valid(raise_exception=True):
                # Get the validated rows from the CSV
                validated_rows = csv_serializer.validated_data['file']
                # Create rooms from each row in the CSV file
                for row in validated_rows:
                    created_rooms.append(models.MmsRoom.objects.create(**row))

        # Serialize the created rooms before returning
        #room_serializer = MmsRoomBaseSerializer(created_rooms, many=True)
        return created_rooms
        
class MmsRoomListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing room information, including details about room type and location.
    It provides custom methods to retrieve related room type and location fields.
    """
    
    # Custom method field for retrieving the room type based on the related stateroom type.
    roomtype = serializers.SerializerMethodField()
    
    # Custom method field for retrieving the location based on the related location data.
    location = serializers.SerializerMethodField()
    
    class Meta:
        model = models.MmsRoom
        fields = ['roomnumber', 'roomfloor','roomtype', 'location']
        
    def get_roomtype(self, obj):
        """
        Retrieve the room type from the related stateroom type table.
        This method extracts the stateroom type description from the related MmsRoomType model.
        If no stateroom type is related, it returns None.
        """
        return obj.stateroomtypeid.stateroomtype if obj.stateroomtypeid else None
    
    def get_location(self, obj):
        """
        Retrieve the location from the related location table.
        This method extracts the location from the related MmsRoomLoc model.
        If no location is related, it returns None.
        """
        return obj.locid.location if obj.locid else None
                                                 
class MmsShipActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for managing the relationship between ships and activities.
    This serializer ensures that a ship can be assigned an activity only once.
    """
    
    class Meta:
        model = models.MmsShipActivity
        fields = ['shipid', 'activityid']
    
    def validate_activityid(self, data):
        """
        Validate that the activity exists.
        """
        
        if not models.MmsActivity.objects.filter(activityid=data):
            raise serializers.ValidationError(f"Actvity you are trying to add to ship doesn't exist.")
        
        return data
            
    def validate(self, data):
        """
        Validate that the combination of ship and activity is unique.
        Ensures that an activity is not assigned to the same ship more than once.
        If the combination of `shipid` and `activityid` already exists, a validation error is raised.
        """
        
        if models.MmsShipActivity.objects.filter(shipid=data['shipid'], activityid=data['activityid']).exists():
            raise serializers.ValidationError(
                f"Activity {data['activityid'].activityname} already exists for ship {data['shipid'].shipname}."
            )
        return data

class MmsShipRestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer for managing the relationship between ships and restaurants.
    This serializer ensures that a ship can be assigned a restaurant only once.
    """
    
    class Meta:
        model = models.MmsShipRestaurant
        fields = ['shipid', 'restaurantid']
        
    def validate(self, data):
        """
        Validate that the combination of ship and restaurant is unique.
        Ensures that a restaurant is not assigned to the same ship more than once.
        If the combination of `shipid` and `restaurantid` already exists, a validation error is raised.
        """
        
        if not models.MmsRestaurant.objects.filter(restaurantid=data['restaurantid']):
            raise serializers.ValidationError(f"Restaurant you are trying to add to ship {data['shipname']} doesn't exist.")

        
        if models.MmsShipRestaurant.objects.filter(shipid=data['shipid'], restaurantid=data['restaurantid']).exists():
            raise serializers.ValidationError(
                f"Restaurant {data['restaurantid'].restaurantname} already exists for ship {data['shipid'].shipname}."
            )
        return data

class MmsShipRoomsSerializer(serializers.ModelSerializer):
    """
    Serializer for managing the relationship between ships and rooms.
    This serializer ensures that a ship can be assigned a room only once.
    """
    
    class Meta:
        model = models.MmsShipRoom
        fields = ['shipid', 'roomnumber']
        
    def validate(self, data):
        """
        Validate that the combination of ship and room number is unique.
        Ensures that a room is not assigned to the same ship more than once.
        If the combination of `shipid` and `roomnumber` already exists, a validation error is raised.
        """
        if models.MmsShipRoom.objects.filter(shipid=data['shipid'], roomnumber=data['roomnumber']).exists():
            raise serializers.ValidationError(
                f"Room {data['roomnumber']} already exists for ship {data['shipid'].shipname}."
            )
        return data
           
class MmsShipCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating ships along with related activities, restaurants, and rooms.
    This serializer allows creating a ship and associating it with multiple activities, restaurants, and rooms.
    """
    activities = serializers.ListField(child=serializers.DictField(), required=False)
    restaurants = serializers.ListField(child=serializers.DictField(), required=False)
    rooms = serializers.ListField(child=serializers.DictField(), required=False)
    
    class Meta:
        model = models.MmsShip
        fields = ['shipid', 'shipname', 'description', 'capacity', 'activities', 'restaurants', 'rooms']
        
    def validate_shipname(self, data):
        """
        Validate the ship's name to ensure it is not empty, exceeds 45 characters, and is unique.
        """
        if not data or data.strip() == "":
            raise ValidationError("Ship name cannot be empty.")
        
        if len(data) > 45:
            raise serializers.ValidationError("Ship name cannot exceed 45 characters.")
        
        if models.MmsShip.objects.filter(shipname=data).exists():
            raise ValidationError(f"A ship with name {data} already exists.")
        return data 

    def validate_description(self, data):
        """
        Validate the ship's description to ensure it is not empty, does not exceed 150 characters, 
        and contains only valid characters.
        """
        if not data or data.strip() == "":
            raise ValidationError("Ship description cannot be empty.")
        
        if len(data) > 150:
            raise ValidationError("Ship description must not exceed 150 characters.")
        
        if not re.match(r'^[a-zA-Z0-9.,!? \-]*$', data):
            raise ValidationError("Ship description contains invalid characters.")
        
        return data
    
    def validate_capacity(self, data):
        """
        Ensure that the ship's capacity is a positive number.
        """
        if data <= 0:
            raise serializers.ValidationError("Capacity must be a positive number.")
        return data
    
    def create_ship_activities(self, ship, activities):
        """
        Create the ship's associated activities.
        If activities are provided, each activity is linked to the ship.
        """
        if activities:
            for activity in activities:
                activity_id = activity.get('activityid')
                if activity_id:  # Ensure ID is present
                    activity = models.MmsActivity.objects.get(activityid=activity_id)
                    models.MmsShipActivity.objects.create(shipid=ship, activityid=activity)

    def create_ship_restaurants(self, ship, restaurants):
        """
        Create the ship's associated restaurants.
        If restaurants are provided, each restaurant is linked to the ship.
        """
        if restaurants:
            for restaurant in restaurants:
                restaurant_id = restaurant.get('restaurantid')
                if restaurant_id:  # Ensure ID is present
                    restaurant = models.MmsRestaurant.objects.get(restaurantid=restaurant_id)
                    models.MmsShipRestaurant.objects.create(shipid=ship, restaurantid=restaurant)
    
    def create_ship_rooms(self, ship, rooms):
        """
        Create the ship's associated rooms.
        If rooms are provided, each room is linked to the ship.
        """
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
        """
        Create a new ship and associate it with activities, restaurants, and rooms.
        Handles the entire creation process, ensuring all related data is created.
        """
        activities = validated_data.pop('activities', [])
        restaurants = validated_data.pop('restaurants', [])
        rooms = validated_data.pop('rooms', [])
        
        # Create the ship object
        ship = models.MmsShip.objects.create(**validated_data)
        ship.save()

        # Create associated activities, restaurants, and rooms
        self.create_ship_activities(ship, activities)
        self.create_ship_restaurants(ship, restaurants)
        self.create_ship_rooms(ship, rooms)
        
        return ship

class MmsShipListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing ships and retrieving their full details.
    This serializer is used to serialize the list of ships, providing all the details from the MmsShip model.
    """
    
    class Meta:
        model = models.MmsShip
        fields = '__all__'  # Include all fields from the MmsShip model in the serialized data
         
class MmsPackageCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating or updating package data.
    This serializer validates package details and ensures that certain constraints are met.
    It also includes validation for unique package IDs and names, and other fields like base price and package details.
    """
    
    class Meta:
        model = models.MmsPackage
        fields = '__all__'  # Include all fields from the MmsPackage model in the serialized data
    
    def validate_packageid(self, data):
        """
        Validate that the package ID is unique, ensuring no other package has the same ID.
        This method allows the current object to keep the same package ID during updates.
        """
        if models.MmsPackage.objects.filter(packageid=data).exclude(packageid=data).exists():
            raise serializers.ValidationError("A package with this package ID already exists.")
        
        return data
        
    def validate_packagename(self, data):
        """
        Validate the package name against a predefined set of valid types.
        Ensure the package name matches one of the allowed values, and that it is unique.
        """
        valid_types = ['hydration plus', 'cheers unlimited', 'connected traveler', 'internet freedom', 'gourmet feast']
        if data.lower() not in valid_types:
            raise serializers.ValidationError(f"Package has to be one of {valid_types}")
        
        if models.MmsPackage.objects.filter(packagename=data).exists():
            raise serializers.ValidationError("A package with this package name already exists.")
        
        return data
    
    def validate_base_price(self, data):
        """
        Validate that the base price is a positive value and does not exceed an acceptable maximum.
        """
        if data <= 0:
            raise ValidationError("Base price must be a positive value.")
        
        if data > 1000:
            raise ValidationError("Base price seems unrealistically high.")
        
        return data
    
    def validate_packagedetails(self, data):
        """
        Validate the length of the package details.
        Ensure the details are neither too short nor too long.
        """
        if len(data) < 10:
            raise ValidationError("Package details must be at least 10 characters long.")
        
        if len(data) > 150:
            raise ValidationError("Package details must be less than 150 characters long.")
        
        return data

    def create(self, validated_data):
        """
        Create a new package instance in the database.
        This method handles the creation of a new MmsPackage based on the validated data.
        """
        return models.MmsPackage.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update an existing package instance with new validated data.
        This method updates the fields of the current package and saves the changes.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class MmsPackageListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing package data.
    This serializer includes all fields from the MmsPackage model for retrieval purposes.
    """

    class Meta:
        model = models.MmsPackage
        fields = '__all__'  # Include all fields from the MmsPackage model in the serialized data
                                     
class MmsItinerarySerializer(serializers.ModelSerializer):
    """
    Serializer for managing and validating itinerary data.
    Handles the creation, update, and validation of port stop information for a specific trip.
    """

    class Meta:
        model = models.MmsPortStop
        fields = ['tripid', 'portid', 'arrivaltime', 'departuretime', 'orderofstop', 'isstartport', 'isendport', 'description']

    def validate_description(self, data):
        """
        Validate the description field to ensure it is not empty, within length limits, and contains only valid characters.
        """
        if not data or data.strip() == "":
            raise ValidationError("Stop description cannot be empty.")
        
        if len(data) > 300:
            raise ValidationError("Stop description must not exceed 300 characters.")
        
        if not re.match(r'^[a-zA-Z0-9.,!?\-]*$', data):
            raise ValidationError("Stop description contains invalid characters.")
        
        return data
    
    def validate_orderofstop(self, data):
        """
        Validate that the order of stop is not negative.
        """
        if data < 0:
            raise serializers.ValidationError("Stop number cannot be negative")
        return data
        
    def validate(self, data):
        """
        Perform additional custom validation for various fields.
        This includes ensuring boolean values for ports, arrival/departure times, and sequential stops.
        """
        self.validate_is_boolean(data)
        self.validate_arrival_before_departure(data)
        self.validate_order_of_stop(data)
        self.validate_trip_has_start_and_end_port(data)
        
        if data.get('isstartport'):
            # Start port-specific validation
            if data.get('arrivaltime'):
                raise ValidationError("Arrival time is not needed for the start port.")
            if not data.get('departuretime'):
                raise ValidationError("Departure time is required for the start port.")

        if data.get('isendport'):
            # End port-specific validation
            if data.get('departuretime'):
                raise ValidationError("Departure time is not needed for the end port.")
            if not data.get('arrivaltime'):
                raise ValidationError("Arrival time is required for the end port.")

        if not data.get('isstartport') and not data.get('isendport'):
            # Intermediate port-specific validation
            if not data.get('arrivaltime') or not data.get('departuretime'):
                raise ValidationError("Both arrival and departure times are required for intermediate ports.")

        return data

    def validate_is_boolean(self, data):
        """
        Ensure that `isstartport` and `isendport` are boolean values.
        """
        if not isinstance(data.get('isstartport'), bool):
            raise serializers.ValidationError("isstartport must be a boolean value.")
        if not isinstance(data.get('isendport'), bool):
            raise serializers.ValidationError("isendport must be a boolean value.")

    def validate_arrival_before_departure(self, data):
        """
        Ensure arrival time is before departure time.
        """
        if data.get('arrivaltime') and data.get('departuretime') and data['arrivaltime'] >= data['departuretime']:
            raise serializers.ValidationError("Arrival time must be before departure time.")

    def validate_order_of_stop(self, data):
        """
        Ensure that `orderofstop` is sequential and does not skip numbers.
        """
        tripid = data['tripid']
        order_of_stop = data['orderofstop']
        
        # Check if this is the first stop being created for the trip
        existing_stops = models.MmsPortStop.objects.filter(tripid=tripid).order_by('orderofstop')
        existing_order_of_stop = [stop.orderofstop for stop in existing_stops]

        # Ensure that order of stops is sequential (1, 2, 3, ...)
        if order_of_stop != len(existing_order_of_stop) + 1:
            raise serializers.ValidationError(f"Order of stop must be sequential. Next available stop number is {len(existing_order_of_stop) + 1}.")

    def validate_trip_has_start_and_end_port(self, data):
        """
        Ensure every trip has both a start port and an end port.
        """
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
    """
    Serializer for managing and validating trip-package relationships.
    This serializer ensures that a specific trip can be associated with a valid package,
    and checks for duplicate trip-package combinations.
    """
    
    class Meta:
        model = models.MmsTripPackage
        fields = ['tripid', 'packageid']
        
    def validate_packageid(self, data):
        """
        Validate that the provided package ID exists in the MmsPackage model.
        Raises a validation error if the package ID does not exist.
        """
        if not models.MmsPackage.objects.filter(packageid=data).exists():
            raise serializers.ValidationError(f"Package ID {data} doesn't exist.")
        
        return data
        
    def validate(self, data):
        """
        Ensure that the combination of trip ID and package ID is unique.
        This prevents the same package from being associated with a trip more than once.
        """
        # Check if the combination of trip ID and package ID already exists in MmsTripPackage
        if models.MmsTripPackage.objects.filter(tripid=data['tripid'], packageid=data['packageid']).exists():
            raise serializers.ValidationError(
                f"Package {data['packageid'].packagename} already exists for trip {data['tripid'].tripname}."
            )
        
        return data

class MmsTripRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MmsTripRoom
        fields = [
            'tripid',  
            'roomnumber', 
            'baseprice', 
            'isbooked', 
            'dynamicprice'
        ]
        read_only_fields = ['tripid', 'roomnumber', 'baseprice', 'dynamicprice', 'isbooked', 'roomtype', 'location']
           
class MmsTripCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and validating new trips.
    It includes validation for required fields like trip dates, cost, capacity, and associated stops and packages.
    """
    stops = serializers.ListField(child=serializers.DictField(), required=False)
    packages = serializers.ListField(child=serializers.DictField(), required=False)
    
    class Meta:
        model = models.MmsTrip
        fields = [
            'tripid', 'tripname', 'startdate', 'enddate', 'tripcostperperson', 'tripstatus', 'tripcapacity', 
            'cancellationpolicy', 'tripdescription', 'finalbookingdate', 'shipid', 'stops', 'packages'
        ]

    # Validate that tripname is not empty or too long
    def validate_tripname(self, data):
        if not data or data.strip() == "":
            raise ValidationError("Trip name cannot be empty.")
        if len(data) > 50:
            raise ValidationError("Trip name cannot exceed 50 characters.")
        return data

    # Validate that startdate is not in the past
    def validate_startdate(self, data):
        if data < datetime.now().date():
            raise ValidationError("Start date cannot be in the past.")
        return data

    # Validate that enddate is not before the startdate
    def validate_enddate(self, data):
        startdate = self.initial_data.get('startdate')
        if startdate and data < datetime.strptime(startdate, "%Y-%m-%d").date():
            raise ValidationError("End date cannot be before the start date.")
        if data < datetime.now().date():
            raise ValidationError("End date cannot be in the past.")
        return data

    # Validate that trip cost per person is a positive value
    def validate_tripcostperperson(self, data):
        if data <= 0:
            raise ValidationError("Trip cost per person must be a positive number.")
        return data

    # Validate that trip status is one of the allowed values
    def validate_tripstatus(self, data):
        valid_statuses = ['Scheduled', 'Completed', 'Cancelled', 'Postponed']
        if data not in valid_statuses:
            raise ValidationError(f"Trip status must be one of: {', '.join(valid_statuses)}.")
        return data

    # Validate that trip capacity is a positive number
    def validate_tripcapacity(self, data):
        if data <= 0:
            raise ValidationError("Capacity must be a positive number.")
        return data

    # Validate cancellation policy: not empty or too long
    def validate_cancellationpolicy(self, data):
        if not data or data.strip() == "":
            raise ValidationError("Cancellation policy cannot be empty.")
        if len(data) > 300:
            raise ValidationError("Cancellation policy cannot exceed 300 characters.")
        return data

    # Validate that trip description is not empty and within length limits
    def validate_tripdescription(self, data):
        if not data or data.strip() == "":
            raise ValidationError("Trip description cannot be empty.")
        if len(data) > 300:
            raise ValidationError("Trip description cannot exceed 300 characters.")
        return data

    # Validate that final booking date is not in the past and before the trip start date
    def validate_finalbookingdate(self, data):
        trip_start_date = self.initial_data.get('startdate')
        if data and data < datetime.now().date():
            raise ValidationError("Final booking date cannot be in the past.")
        if trip_start_date and data and data > datetime.strptime(trip_start_date, "%Y-%m-%d").date():
            raise ValidationError("Final booking date must be before the trip start date.")
        return data

    def validate(self, data):
        tripname = data.get('tripname')
        startdate = data.get('startdate')
        enddate = data.get('enddate')
        stops = data.get('stops', [])

        overlapping_trips = models.MmsTrip.objects.filter(tripname=tripname,startdate=startdate,enddate=enddate)
        overlapping_start_date = models.MmsTrip.objects.filter(tripname=tripname,startdate=startdate)
        overlapping_end_date = models.MmsTrip.objects.filter(tripname=tripname,enddate=enddate)
        

        if overlapping_trips.exists() or overlapping_end_date.exists() or overlapping_start_date.exists():
            raise ValidationError(f"There's already an existing trip named '{tripname}' with overlapping dates.")
        
        start_port = next((stop for stop in stops if stop.get('isstartport') == 1), None)
        end_port = next((stop for stop in stops if stop.get('isendport') == 1), None)

        if not start_port:
            raise ValidationError("A start port is required.")
        if not end_port:
            raise ValidationError("An end port is required.")
        
        # Check that start date matches the start port's departure time
        if 'departuretime' in start_port:
            start_departure = datetime.strptime(start_port['departuretime'], "%Y-%m-%dT%H:%M:%SZ").date()
            if startdate != start_departure:
                raise ValidationError(f"Start date must match the departure date of the start port ({start_departure}).")

        # Check that end date matches the end port's arrival time
        if 'arrivaltime' in end_port:
            end_arrival = datetime.strptime(end_port['arrivaltime'], "%Y-%m-%dT%H:%M:%SZ").date()
            if enddate != end_arrival:
                raise ValidationError(f"End date must match the arrival date of the end port ({end_arrival}).")
        
        return data
    
    # Create the trip stops from validated data
    def create_trip_stops(self, trip, stops):
        if stops:
            for stop in stops:
                port_id = stop.pop('portid')
                if port_id:
                    port = models.MmsPort.objects.get(portid=port_id)
                    order_of_stop = stop.get('orderofstop')
                    if order_of_stop is None:
                        raise ValidationError("Each stop must have an 'orderofstop' value.")
                    models.MmsPortStop.objects.create(tripid=trip, portid=port, **stop)

    # Create the trip packages from validated data
    def create_trip_packages(self, trip, packages):
        if packages:
            for package in packages:
                package_id = package.get('packageid')
                if package_id:
                    package_instance = models.MmsPackage.objects.get(packageid=package_id)
                    models.MmsTripPackage.objects.create(tripid=trip, packageid=package_instance)

    # Automatically populate trip rooms
    def populate_trip_rooms(self, trip):
        """
        Populates TripRoom table based on rooms linked to the ship.
        """
        # Fetch rooms linked to the ship
        ship_rooms = models.MmsShipRoom.objects.filter(shipid=trip.shipid)

        # Create TripRoom entries
        trip_rooms = []
        for room in ship_rooms:
            trip_rooms.append(
                models.MmsTripRoom(
                    tripid=trip,
                    roomnumber=room.roomnumber,
                    isbooked=False,
                    dynamicprice=room.roomnumber.stateroomtypeid.baseprice,
                    baseprice=room.roomnumber.stateroomtypeid.baseprice,
                    roomtype=room.roomnumber.stateroomtypeid.stateroomtype,
                    location=room.roomnumber.locid.location
                )
            )
        # Bulk create TripRoom entries for efficiency
        models.MmsTripRoom.objects.bulk_create(trip_rooms)
        
    # Create the trip and its related stops and packages within a transaction
    @transaction.atomic
    def create(self, validated_data): 
        packages = validated_data.pop('packages', [])
        stops = validated_data.pop('stops', [])

        trip = models.MmsTrip.objects.create(**validated_data)
        self.create_trip_stops(trip, stops)
        self.create_trip_packages(trip, packages)
        self.populate_trip_rooms(trip)

        return trip

class MmsRoomSummarySerializer(serializers.Serializer):
    """
    Serializer to handle the grouped room data, splitting roomtype and location details into separate dictionaries.
    """
    roomtype = serializers.DictField()  # Dictionary for roomtype data
    location = serializers.DictField()  # Dictionary for location data

    def to_representation(self, instance):
        """
        Map the grouped dictionary to the required structure.
        """
        return {
            "roomtype": {
                "name": instance.get("stateroomtypeid__stateroomtype"),
                "price": instance.get("stateroomtypeid__baseprice"),
                "count": instance.get("roomtypecount"),
            },
            "location": {
                "name": instance.get("locid__location"),
                "count": instance.get("locationcount"),
            }
        }

class MmsTripRoomPriceUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer to handle updates to dynamic pricing for rooms in MmsTripRoom.
    Supports updating prices for specific room types or locations.
    """
    roomtype = serializers.CharField(required=False, write_only=True)
    location = serializers.CharField(required=False, write_only=True)
    dynamicprice = serializers.DecimalField(max_digits=6, decimal_places=2, required=True, write_only=True)

    class Meta:
        model = models.MmsTripRoom
        fields = ['roomtype', 'location', 'dynamicprice']

    def validate(self, attrs):
        """
        Validate the input for dynamic price updates.
        Ensures that at least one filter (roomtype or location) is provided, and checks for conflicts.
        """
        roomtype = attrs.get('roomtype')
        location = attrs.get('location')
        dynamicprice = attrs.get('dynamicprice')

        # Ensure dynamic price is within acceptable range
        if dynamicprice < 150 or dynamicprice > 5000:  # Example price range validation
            raise serializers.ValidationError("Dynamic price must be between $150 and $5,000.")

        # Ensure that only one of roomtype or location is provided
        if not roomtype and not location:
            raise serializers.ValidationError("Provide either 'roomtype' or 'location' to update prices.")

        # Handle conflicting updates (both room type and location provided)
        if roomtype and location:
            raise serializers.ValidationError(
                "Cannot update price for both room type and location simultaneously. Choose one filter."
            )

        return attrs

class MmsTripListSerializer(serializers.ModelSerializer):
    # Nested serializer for related start port (via MmsPortStop and MmsPort)
    port_stops = serializers.SerializerMethodField()
    shipname = serializers.SerializerMethodField()

    class Meta:
        model = models.MmsTrip
        fields = ['tripid', 'tripname', 'startdate', 'enddate', 'tripcostperperson', 'tripdescription', 'shipname', 'port_stops']
    
    
    def get_shipname(self, obj):
        """
        Fetch the name of the ship assigned for this trip

        """  
        return obj.shipid.shipname if obj.shipid else None
    
    def get_port_stops(self, obj):
        """
        Fetch all port stops with their details and order them.
        Optimized using `select_related` to avoid multiple queries for `MmsPort` data.
        """
        port_stops = obj.portstops.select_related('portid').order_by('orderofstop')
        
        port_stop_details = []
        for stop in port_stops:
            port_data = stop.portid  # MmsPort object
            
            # Prepare the dictionary with port stop details
            port_stop_details.append({
                "port_name": port_data.portname if port_data else None,
                "city": port_data.portcity if port_data else None,
                "country": port_data.portcountry if port_data else None,
                "order_of_stop": stop.orderofstop,
                "is_start_port": stop.isstartport == True,
                "is_end_port": stop.isendport == True,
            })
        
        return port_stop_details
           
class MmsAdminTripListSerializer(MmsTripListSerializer):  
    class Meta(MmsTripListSerializer.Meta):  # Extend Meta from the parent filter
        model = MmsTripListSerializer.Meta.model
        fields = MmsTripListSerializer.Meta.fields + ['tripstatus']  # Include parent fields and any new ones
                     
# User related features
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MmsUserProfile
        fields = ['phonenumber', 'dateofbirth']  # Include phone number and date of birth fields in the serialized data
        
    def validate_phonenumber(self, value):
        """
        Validate phone number to ensure it only contains digits and follows a specific format.
        
        The phone number must:
        - Be in the E.164 international format (e.g., +1234567890 or 1234567890).
        - Contain only digits and optionally start with a plus sign.
        """
        # Regular expression checks for valid phone number format in E.164 standard
        if not re.fullmatch(r'\+?[1-9]\d{1,14}', value):  # E.164 format: starting with an optional '+' followed by digits
            raise ValidationError("Phone number must be valid and follow international standards.")
        return value

    def validate_dateofbirth(self, value):
        """
        Validate date of birth to ensure it's not in the future and that the user is at least 13 years old.
        
        The date of birth must:
        - Not be in the future.
        - Represent an age of at least 13 years.
        """
        # Ensure the date of birth is not a future date
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        
        # Calculate the user's age based on their date of birth
        age = (date.today() - value).days // 365  # Approximate age in years
        if age < 18:  # Check if the age is less than 13 years
            raise ValidationError("User must be at least 18 years old.")
        
        return value

class UserCreateSerializer(serializers.ModelSerializer):
    # Nested serializer for user profile, it's optional (required=False)
    profile = UserProfileSerializer(required=False)

    # Password and confirm password fields are required, should be written in 'password' input type
    password = serializers.CharField(write_only=True, required=True, min_length=8, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'profile']
        extra_kwargs = {"password": {"write_only": True}}  # Password field should not be read in response

    def validate_username(self, value):
        """
        Validate the username to ensure it is not reserved and is unique.

        - 'admin' is a reserved username, so we prevent its use.
        - Check if the username already exists in the database (ensure uniqueness).
        - Return the username in lowercase to make the check case-insensitive.
        """
        if value.lower() == "admin":
            raise serializers.ValidationError("Username 'admin' is reserved. Please choose a different username.")
        
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists. Please choose a different username.")
        
        return value.lower()

    def validate_email(self, value):
        """
        Validate the email address to ensure it is in a valid format and is unique.
        
        - Check if the email matches a standard email format using a regex.
        - Ensure the email does not already exist in the database (uniqueness).
        - Return the email in lowercase to ensure case-insensitive comparison.
        """
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("Enter a valid email address.")
        
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email address already registered. Please use a different email.")
        
        return value.lower()

    def validate_password(self, value):
        """
        Validate the password to ensure it meets certain security criteria.
        
        - Password should be at least 8 characters long.
        - Password must contain at least one digit.
        - Password must contain at least one uppercase letter.
        - Password must contain at least one special character from a set.
        """
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        if not re.search(r"\d", value):  # Check for at least one digit
            raise serializers.ValidationError("Password must contain at least one digit.")
        
        if not re.search(r"[A-Z]", value):  # Check for at least one uppercase letter
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):  # Check for at least one special character
            raise serializers.ValidationError("Password must contain at least one special character.")
        
        return value

    def validate(self, data):
        """
        Validate that the password and confirm password fields match.

        - If passwords do not match, raise a validation error.
        - Remove the confirm_password field from the data since it is not needed in the final model.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        
        # Remove confirm_password as it is not stored in the database
        data.pop('confirm_password')
        
        return data

    @transaction.atomic
    def create(self, validated_data):
        """
        Create a new user and their profile (if provided).
        
        - Pop out the password and profile data for special handling.
        - Use `create_user` to create the user, which ensures the password is hashed.
        - If profile data is provided, create the user profile linked to the user.
        - Save the user instance and return the user object.
        """
        # Pop password from validated data as it needs special handling
        password = validated_data.pop('password')
        profile_data = validated_data.pop('profile', None)  # Get profile data if provided, otherwise None
        
        # Create the user instance without the profile data
        user = User.objects.create_user(**validated_data)
        
        # Set the password (it gets hashed here)
        user.set_password(password)
        
        # If profile data is provided, create the user profile instance
        if profile_data:
            models.MmsUserProfile.objects.create(userid=user.pk, **profile_data)
        
        # Save the user instance after setting the password
        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    # Nested serializer for the user profile, optional (required=False)
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile']  # Only updatable fields are included

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Update the user instance and related profile if provided.
        
        - Updates the user's first name and last name.
        - If profile data is provided, updates the user's profile.
        - Uses atomic transactions to ensure consistency of changes (either all changes succeed or none).
        """
        # Update the user's first name and last name if new data is provided
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        # Extract profile data from validated_data (if provided)
        profile_data = validated_data.pop('profile', None)
        if profile_data:
            try:
                # Try to find the user's profile and update fields
                profile_instance = models.MmsUserProfile.objects.get(userid=instance.id)  # Get the profile by user ID
                profile_instance.phonenumber = profile_data.get('phonenumber', profile_instance.phonenumber)
                profile_instance.save()  # Save the profile instance with updated data
            except models.MmsUserProfile.DoesNotExist:
                # If profile does not exist, handle it (optional based on business rules)
                pass

        # Save the updated user instance
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Customize the serialized output to include the related profile data.
        
        - This method customizes the serialized response to include user profile data in the final response.
        - If the profile exists, it adds the serialized profile data; otherwise, it adds `None`.
        """
        # Call the default 'to_representation' method from the parent serializer
        representation = super().to_representation(instance)

        # Add the profile data manually to the representation
        try:
            # Fetch the user's profile instance
            profile_instance = models.MmsUserProfile.objects.get(user_id=instance.id)
            # Serialize the profile and add it to the output representation
            representation['profile'] = UserProfileSerializer(profile_instance).data
        except models.MmsUserProfile.DoesNotExist:
            # If the profile does not exist, set 'profile' to None in the output
            representation['profile'] = None

        return representation

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        """
        Validate the login credentials (either username or email) and authenticate the user.
        
        - The identifier can be either a username or an email.
        - The password is checked against the provided username or email.
        - If authentication is successful, a JWT token pair is generated.
        - Additional claims are added to the token data.
        """
        # Extract username or email and password from the input
        identifier = attrs.get('username')  # Can be either email or username
        password = attrs.get('password')

        user = None

        # Check if the identifier is an email format using a regular expression
        if re.match(r"[^@]+@[^@]+\.[^@]+", identifier):
            try:
                # Try to fetch the user by email
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                # Raise an error if no user is found by email
                raise AuthenticationFailed('No account found with that email.')
        else:
            try:
                # Try to fetch the user by username
                user = User.objects.get(username=identifier)
            except User.DoesNotExist:
                # Raise an error if no user is found by username
                raise AuthenticationFailed('No account found with that username.')
        
        # Restrict access to staff and admin accounts (only regular users can log in)
        if user.is_staff or user.is_superuser:
            raise AuthenticationFailed('Only regular users are allowed to log in.')

        # Authenticate the user using the provided username and password
        user = authenticate(username=user.username, password=password)
        if not user:
            # Raise an error if authentication fails (invalid credentials)
            raise AuthenticationFailed('Invalid credentials.')

        # Call the parent method (TokenObtainPairSerializer) to generate JWT tokens
        data = super().validate({"username": user.username, "password": password})

        # Add additional claims to the token data
        data['username'] = user.username
        data['email'] = user.email

        return data

class PasswordResetRequestSerializer(serializers.Serializer):
    # Email field for password reset request
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Validate that the email provided exists in the database.
        
        - If no user is associated with the provided email, a validation error is raised.
        - If the email exists, it is returned as valid.
        """
        # Check if the email exists in the database
        if not User.objects.filter(email=value).exists():
            # Raise an error if no user is found with this email
            raise serializers.ValidationError("No user found with this email address.")
        return value

class MmsTripDetailSerializer(MmsTripListSerializer):
    # Nested serializer for related start port (via MmsPortStop and MmsPort)
    # Additional fields for trip description, cancellation policy, additional fees, etc.
    port_times = serializers.SerializerMethodField()  # Method to fetch port arrival and departure times
    restaurants = serializers.SerializerMethodField()  # Method to fetch restaurant details
    activities = serializers.SerializerMethodField()  # Method to fetch activity details

    class Meta(MmsTripListSerializer.Meta):
        # Include the fields from MmsTripListSerializer and the new detailed fields
        fields = MmsTripListSerializer.Meta.fields + [
            'tripdescription', 
            'cancellationpolicy',
            'finalbookingdate',   
            'port_times',
            'restaurants',
            'activities'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the `port_stops` field inherited from the parent serializer
        self.fields.pop('port_stops', None)
        
    def get_port_times(self, obj):
        """
        Get arrival and departure times for each port in the trip.
        - This method collects the details of each port stop for the given trip,
        - including the port name, arrival time, and departure time.
        """
        port_times = []  # List to hold port time data
        
        # Iterate through the port stops for the current trip, ordered by the order of stop
        for port_stop in obj.portstops.all().order_by('orderofstop'):
            port = port_stop.portid  # Fetch the port related to the current port stop
            port_time_data = {
                "port_name": port.portname if port else None,  # Get the port name
                "port_city": port.portcity,
                "arrival_time": port_stop.arrivaltime,  # Get the arrival time for the port stop
                "departure_time": port_stop.departuretime,  # Get the departure time for the port stop
            }
            # Append the port time data to the list
            port_times.append(port_time_data)
        
        # If no port times were found, return an empty list
        return port_times if port_times else []

    def get_restaurants(self, obj):
        """
        Fetch detailed restaurant information linked to the ship associated with this trip.
        """
        # Ensure the ship is linked to the trip
        if not obj.shipid:
            return []

        # Use `select_related` to prefetch restaurant details efficiently
        ship_restaurants = models.MmsShipRestaurant.objects.filter(shipid=obj.shipid).select_related('restaurantid')

        # Prepare the response with relevant details
        return [
            {
                "restaurant_name": restaurant.restaurantid.restaurantname,
                "breakfast": restaurant.restaurantid.servesbreakfast,
                "lunch": restaurant.restaurantid.serveslunch,
                "dinner": restaurant.restaurantid.servesdinner,
                "alcohol": restaurant.restaurantid.servesalcohol,
            }
            for restaurant in ship_restaurants
        ]

    def get_activities(self, obj):
        """
        Fetch detailed activity information linked to the ship associated with this trip.
        """
        if not obj.shipid:
            return []

        ship_activities = models.MmsShipActivity.objects.filter(shipid=obj.shipid).select_related('activityid')

        return [
            {
                "activity_name": activity.activityid.activityname,
                "description": activity.activityid.activitydescription,
                "capacity": activity.activityid.capacity,
            }
            for activity in ship_activities
        ]
    