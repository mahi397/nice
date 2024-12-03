from . import models
from django.db import transaction
from . import filters, serializers
from django.core.mail import send_mail
from . permissions import IsAdminOrStaff
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import mixins, generics, status
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated


'''class MmsTripListAPIView(APIView):
    permission_classes = [AllowAny]  # Or more specific permissions for passenger, staff, and admin

    def get(self, request, *args, **kwargs):
        # Get the user role
        user = self.request.user
        
        # Filter trips based on user role
        if user.is_staff or user.is_superuser:
            # Staff and admin see all trips
            queryset = MmsTrip.objects.all()
        else:
            # Passengers only see upcoming trips
            #queryset = MmsTrip.objects.filter(startdate__gte=now())  # Filter for upcoming trips
            queryset = MmsTrip.objects.all()
        
        # Apply the filters if any (using CruiseFilter)
        filtered_queryset = CruiseFilter(request.GET, queryset=queryset).qs
        
        # Serialize the filtered queryset
        serializer = MmsTripListSerializer(filtered_queryset, many=True)
        
        return Response(serializer.data)
'''

class AdminLoginView(TokenObtainPairView):
    """
    Custom Token Obtain View to handle login and issue JWT tokens.
    Uses the CustomTokenObtainPairSerializer to validate and generate tokens.
    """
    serializer_class = serializers.AdminLoginSerializer

class AdminLogoutView(APIView):
    """
    Logs out authenticated staff/admin users by blacklisting their refresh token.
    """
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def post(self, request):
        try:
            # Extract the refresh token from the request data
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Create a RefreshToken instance
            token = RefreshToken(refresh_token)

            # Blacklist the token to invalidate it
            token.blacklist()

            return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
                
class MmsPortCreateUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = models.MmsPort.objects.all()
    serializer_class = serializers.MmsPortSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'portid'  # Use URL to identify the resource
    
    def get_object(self):
        """
        Override the get_object method to check if the portid exists before proceeding with update.
        """
        portid = self.kwargs['portid']
        
        try:
            # Retrieve the port object or raise a NotFound exception if it doesn't exist
            return models.MmsPort.objects.get(portid=portid)
        except models.MmsPort.DoesNotExist:
            # Handle the case where the portid does not exist
            raise NotFound(f"Port with {portid} not found.")
    
    def post(self, request, *args, **kwargs):
        return self.create(request=request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request=request, *args, **kwargs)
        
class MmsPortListView(generics.ListAPIView):
    queryset = models.MmsPort.objects.all()
    serializer_class = serializers.MmsPortListSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.PortFilter
    search_fields = ['portname', 'portcity', 'portcountry', 'nearestairport']
    ordering_fields = ['portname', 'parkingspots']
    ordering = ['portname']

    '''def list(self):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({"detail": "No ports found matching the filters."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)'''
    
class MmsPortDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = models.MmsPort.objects.all()
    serializer_class = serializers.MmsPortSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'portid'  # Use URL to identify the resource
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()  # Retrieve the object to be deleted
        pid = instance.portname
        self.perform_destroy(instance)  # Perform the deletion
        return Response(
            {"message": f"{pid} deleted successfully from the database."},
            status=status.HTTP_200_OK
    )
        
class MmsRestaurantCreateUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = models.MmsRestaurant.objects.all()
    serializer_class = serializers.MmsRestaurantCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'restaurantid'  # Use URportidL to identify the resource
    
    def get_object(self):
        """
        Override the get_object method to check if the restaurantid exists before proceeding with update.
        """
        restaurantid = self.kwargs['restaurantid']
        
        try:
            # Retrieve the port object or raise a NotFound exception if it doesn't exist
            return models.MmsRestaurant.objects.get(restaurantid=restaurantid)
        except models.MmsRestaurant.DoesNotExist:
            # Handle the case where the portid does not exist
            raise NotFound(f"Restaurant with ID {restaurantid} not found.")
    
    def post(self, request, *args, **kwargs):
        return self.create(request=request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request=request, *args, **kwargs)

class MmsRestaurantListView(generics.ListAPIView):
    queryset = models.MmsRestaurant.objects.all()
    serializer_class = serializers.MmsRestaurantListSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.RestaurantFilter
    search_fields = ['restaurantname']
    ordering_fields = ['restaurantname']
    ordering = ['restaurantname']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({"detail": "No restaurants found matching the filters."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        
class MmsRestaurantDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = models.MmsRestaurant.objects.all()
    serializer_class = serializers.MmsRestaurantCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'restaurantid'  # Use URL to identify the resource
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()  # Retrieve the object to be deleted
        self.perform_destroy(instance)  # Perform the deletion
        return Response(
            {"message": f"Restaurant {instance.restaurantname} deleted successfully."},
            status=status.HTTP_200_OK
    )
    
class MmsActivityCreateUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = models.MmsActivity.objects.all()
    serializer_class = serializers.MmsActivityCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'activityid'  # Use URL to identify the resource
    
    def update(self, request, *args, **kwargs):
        # Extract `portid` from URL
        activityid = kwargs.get('activityid')

        # Validate the `portid` in the request body (if provided)
        if 'activityid' in request.data and str(request.data['activityid']) != str(activityid):
            return Response(
                {"detail": "Restaurant ID in the request body does not match the URL."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Call the parent class update method
        return super().update(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request=request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request=request, *args, **kwargs)

class MmsActivityListView(generics.ListAPIView):
    queryset = models.MmsActivity.objects.all()
    serializer_class = serializers.MmsActivityListSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.ActivityFilter
    search_fields = ['activityname']
    ordering_fields = ['activityname']
    ordering = ['activityname']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({"detail": "No activities found matching the filters."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)  
      
class MmsActivityDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = models.MmsActivity.objects.all()
    serializer_class = serializers.MmsActivityCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'activityid'  # Use URL to identify the resource
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()  # Retrieve the object to be deleted
        self.perform_destroy(instance)  # Perform the deletion
        return Response(
            {"message": f"Restaurant {instance.activityname} deleted successfully."},
            status=status.HTTP_200_OK
    )
        
class MmsRoomLocCreateUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = models.MmsRoomLoc.objects.all()
    serializer_class = serializers.MmsRoomLocCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'locid'  # Use URL to identify the resource
    
    def update(self, request, *args, **kwargs):
        # Extract `portid` from URL
        locid = kwargs.get('locid')

        # Validate the `portid` in the request body (if provided)
        if 'locid' in request.data and str(request.data['locid']) != str(locid):
            return Response(
                {"detail": "loc ID in the request body does not match the URL."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Call the parent class update method
        return super().update(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request=request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request=request, *args, **kwargs)

class MmsRoomLocListView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = models.MmsRoomLoc.objects.all()
    serializer_class = serializers.MmsRoomLocListSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get(self, request, *args, **kwargs):
        return self.list(request=request, *args, **kwargs)   
    
class MmsRoomLocDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = models.MmsRoomLoc.objects.all()
    serializer_class = serializers.MmsRoomLocCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'locid'  # Use URL to identify the resource
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()  # Retrieve the object to be deleted
        self.perform_destroy(instance)  # Perform the deletion
        return Response(
            {"message": f"Location {instance.location} deleted successfully."},
            status=status.HTTP_200_OK
    )

class MmsRoomTypeCreateUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = models.MmsRoomType.objects.all()
    serializer_class = serializers.MmsRoomTypeCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'stateroomtypeid'  # Use URL to identify the resource
    
    def update(self, request, *args, **kwargs):
        # Extract `portid` from URL
        stateroomtypeid = kwargs.get('stateroomtypeid')

        # Validate the `stateroomtypeid` in the request body (if provided)
        if 'stateroomtypeid' in request.data and str(request.data['stateroomtypeid']) != str(stateroomtypeid):
            return Response(
                {"detail": "stateroomtype ID in the request body does not match the URL."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Call the parent class update method
        return super().update(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request=request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request=request, *args, **kwargs)

class MmsRoomTypeListView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = models.MmsRoomType.objects.all()
    serializer_class = serializers.MmsRoomTypeListSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get(self, request, *args, **kwargs):
        return self.list(request=request, *args, **kwargs)   
    
class MmsRoomTypeDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):    
    queryset = models.MmsRoomType.objects.all()
    serializer_class = serializers.MmsRoomTypeCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'stateroomtypeid'  # Use URL to identify the resource
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()  # Retrieve the object to be deleted
        self.perform_destroy(instance)  # Perform the deletion
        return Response(
            {"message": f"State room type {instance.stateroomtype} deleted successfully."},
            status=status.HTTP_200_OK
    )    
        
class MmsRoomCreateUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = models.MmsRoom.objects.all()
    serializer_class = serializers.MmsRoomCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'roomnumber'  # Use URL to identify the resource
    
    def update(self, request, *args, **kwargs):
        # Extract `portid` from URL
        roomnumber = kwargs.get('roomnumber')

        # Validate the `stateroomtypeid` in the request body (if provided)
        if 'roomnumber' in request.data and str(request.data['roomnumber']) != str(roomnumber):
            return Response(
                {"detail": "roomnumber in the request body does not match the URL."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Call the parent class update method
        return super().update(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request=request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request=request, *args, **kwargs)

class MmsRoomBulkCSVCreateView(generics.CreateAPIView):
    serializer_class = serializers.MmsRoomCSVUploadSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def post(self, request, *args, **kwargs):
        # Handle CSV file upload and room creation
        file = request.FILES.get('file')
        if not file:
            return Response({"detail": "File is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data={'file': file})
        if serializer.is_valid():
            # Bulk create rooms from CSV
            created_rooms = serializer.create(serializer.validated_data)
            return Response({"detail": f"{len(created_rooms)} rooms created successfully."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MmsRoomBulkUpdateView(generics.GenericAPIView):
    serializer_class = serializers.MmsRoomBulkUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'roomnumber'  # Use URL to identify the resource

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            room_numbers = [room['roomnumber'] for room in serializer.validated_data]
            instances = models.MmsRoom.objects.filter(roomnumber__in=room_numbers)

            # Ensure all rooms exist
            existing_room_numbers = {room.roomnumber for room in instances}
            missing_room_numbers = set(room_numbers) - existing_room_numbers
            if missing_room_numbers:
                return Response(
                    {"detail": f"Rooms with room numbers {missing_room_numbers} do not exist."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Perform the bulk update
            updated_rooms = serializer.partial_update(instances, serializer.validated_data)
            return Response(
                {"detail": f"{len(updated_rooms)} rooms updated successfully."}, 
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MmsRoomListView(generics.ListAPIView):
    queryset = models.MmsRoom.objects.select_related('stateroomtypeid', 'locid').all()
    serializer_class = serializers.MmsRoomListSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.RoomFilter
    search_fields = ['roomnumber']
    ordering_fields = ['roomnumber', 'roomfloor', 'roombaseprice']
    ordering = ['roomnumber']  # Default ordering (earliest trips first)
    
class MmsRoomDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):    
    queryset = models.MmsRoom.objects.all()
    serializer_class = serializers.MmsRoomBaseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'roomnumber'  # Use URL to identify the resource
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()  # Retrieve the object to be deleted
        self.perform_destroy(instance)  # Perform the deletion (handled by DestroyModelMixin)
        return Response(
            {"message": f"Room {instance.roomnumber} deleted successfully."},
            status=status.HTTP_200_OK  # You can use 204 for no content
        )       
        
class MmsPackageCreateUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = models.MmsPackage.objects.all()
    serializer_class = serializers.MmsPackageCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'packageid'  # Use URL to identify the resource
    
    def update(self, request, *args, **kwargs):
        # Extract `portid` from URL
        packageid = kwargs.get('packageid')

        # Validate the `portid` in the request body (if provided)
        if 'packageid' in request.data and str(request.data['packageid']) != str(packageid):
            return Response(
                {"detail": "package ID in the request body does not match the URL."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Call the parent class update method
        return super().update(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request=request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request=request, *args, **kwargs)

class MmsPackageListView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = models.MmsPackage.objects.all()
    serializer_class = serializers.MmsPackageListSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get(self, request, *args, **kwargs):
        return self.list(request=request, *args, **kwargs)   
    
class MmsPackageDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = models.MmsPackage.objects.all()
    serializer_class = serializers.MmsPackageCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'locid'  # Use URL to identify the resource
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()  # Retrieve the object to be deleted
        self.perform_destroy(instance)  # Perform the deletion
        return Response(
            {"message": f"Package {instance.packagename} deleted successfully."},
            status=status.HTTP_200_OK
    )
                  
'''
class MmsTripAddUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = models.MmsTrip.objects.all()
    serializer_class = serializers.MmsTripAddUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure staff or superuser permission is enforced
    lookup_field = 'tripid'

    def post(self, request, *args, **kwargs):
        """Handle trip creation."""
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Handle trip update."""
        # Ensure the trip exists using tripid from the URL kwargs
        tripid = kwargs.get('tripid')
        try:
            trip_instance = self.get_object()  # This will automatically get the object based on tripid from the URL
        except models.MmsTrip.DoesNotExist:
            return Response({"detail": "Trip not found."}, status=status.HTTP_404_NOT_FOUND)

        # Proceed to update the trip with the serializer
        return self.update(request, *args, **kwargs)
        '''
        
class  MmsPortStopCreateUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = models.MmsPortStop.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    serializer_class = serializers.MmsPortStopCreateUpdateSerializer
    lookup_field = 'itineraryid'
    
    def update(self, request, *args, **kwargs):
        # Extract `itineraryid` from URL
        itineraryid = kwargs.get('itineraryid')

        # Validate the `tripid` in the request body (if provided)
        if 'itineraryid' in request.data and str(request.data['itineraryid']) != str(itineraryid):
            return Response(
                {"detail": "itinerary ID in the request body does not match the URL."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Call the parent class update method
        return super().update(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """
        Handles creating multiple port stops.
        The request should send a list of port stops (many=True).
        """
        # Initialize serializer with many=True to handle list of port stops
        serializer = self.get_serializer(data=request.data, many=True)
        
        # Validate the data
        serializer.is_valid(raise_exception=True)
        
        # Use the mixin's create method to save the data
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, *args, **kwargs):
        """
        Handles updating multiple port stops.
        The request should send a list of port stops (many=True).
        """
        # Initialize serializer with many=True to handle list of port stops
        serializer = self.get_serializer(data=request.data, many=True)
        
        # Validate the data
        serializer.is_valid(raise_exception=True)
        
        # Use the mixin's update method to save the data
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """
        Override this method to use the mixin's create functionality
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Override this method to use the mixin's update functionality
        """
        serializer.save()  
      
class MmsTripCreateUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = models.MmsTrip.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    serializer_class = serializers.MmsTripCreateUpdateSerializer
    lookup_field = 'tripid'  # Use URL to identify the resource
    
    def update(self, request, *args, **kwargs):
        # Extract `tripid` from URL
        tripid = kwargs.get('tripid')

        # Validate the `tripid` in the request body (if provided)
        if 'tripid' in request.data and str(request.data['tripid']) != str(tripid):
            return Response(
                {"detail": "trip ID in the request body does not match the URL."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Call the parent class update method
        return super().update(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request=request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request=request, *args, **kwargs)
        
class MmsTripListView(generics.ListAPIView):
    queryset = models.MmsTrip.objects.all()
    serializer_class = serializers.MmsTripListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.TripFilter
    ordering_fields = ['startdate', 'enddate', 'tripcostperperson', 'duration', 'tripname']
    ordering = ['startdate']  # Default ordering (earliest trips first)

    def get_queryset(self):
        """
        Customize the queryset to return all trips for staff/admin users,
        or only upcoming trips for regular users.
        """
        user = self.request.user
        base_queryset = models.MmsTrip.objects.prefetch_related('portstop__portid')  # Optimize port stop queries
        if user.is_staff or user.is_superuser:
            return base_queryset
        return base_queryset.filter(tripstatus__iexact='upcoming')

    def list(self, request, *args, **kwargs):
        """
        Apply filtering dynamically and handle cases where no results match.
        """
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({"detail": "No trips found matching the specified filters."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MmsTripDetailView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    queryset = models.MmsTrip.objects.all()
    serializer_class = serializers.MmsTripDetailSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class UserCreateView(generics.CreateAPIView):
    """
    User Registration View that handles the creation of a new user.
    - Validates input using UserRegistrationSerializer.
    - Creates a new user and returns the user data.
    """
        
    queryset = User.objects.all()
    serializer_class = serializers.UserCreateSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        # Call the serializer's create method
        user = serializer.save()

        # Custom workflow: Send a welcome email
        send_mail(
            subject="Welcome to NICE",
            message="Thank you for registering with NICE!",
            from_email="noreply@nice.com",
            recipient_list=[user.email],
            fail_silently=True,
        )
    
class UserUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = serializers.UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    
    def partial_update(self, request, *args, **kwargs):
        # Extract `portid` from URL
        userid = kwargs.get('id')

        # Validate the `userid` in the request body (if provided)
        if 'userid' in request.data and str(request.data['userid']) != str(userid):
            return Response(
                {"detail": "User ID in the request body does not match the URL."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Call the parent class update method
        return super().partial_update(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.partial_update(request=request, *args, **kwargs)
    
class UserDeleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        # Optional: Validate username and password before deletion
        username = request.user.username  # The current authenticated user
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

        return self.destroy(request, *args, **kwargs)

class LoginView(TokenObtainPairView):
    """
    Custom Token Obtain View to handle login and issue JWT tokens.
    Uses the CustomTokenObtainPairSerializer to validate and generate tokens.
    """
    serializer_class = serializers.LoginSerializer
    
class LogoutView(APIView):    
    """
    Logs the user out by blacklisting their refresh token.
    This effectively invalidates the session.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            # Extract the refresh token from the request data
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Create a RefreshToken instance
            token = RefreshToken(refresh_token)

            # Blacklist the token to invalidate it
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class CustomPasswordResetView(auth_views.PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    template_name = 'registration/password_reset_form.html'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
        