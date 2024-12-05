from . import models
from django.http import Http404
from . import filters, serializers
from django.core.mail import send_mail
from . permissions import IsAdminOrStaff
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema
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
    This view uses the `AdminLoginSerializer` to validate credentials
    and generate JWT tokens. Only staff and admin users are allowed to log in.
    """

    # Set the serializer class to use for validation and token generation
    serializer_class = serializers.AdminLoginSerializer

    @extend_schema(
        description="Endpoint for admin users to log in. It validates the user's credentials "
                    "(email/username and password) and returns JWT tokens for authenticated users.",
        request=serializers.AdminLoginSerializer,  # Specifies the expected request body format
        responses={
            200: {
                "description": "Successfully logged in. JWT tokens issued.",
                "content": {
                    "application/json": {
                        "example": {
                            "access": "JWT_ACCESS_TOKEN",   # The access token
                            "refresh": "JWT_REFRESH_TOKEN", # The refresh token
                            "username": "admin_user",       # Username of the authenticated user
                            "email": "admin@example.com",   # Email of the authenticated user
                            "is_staff": True                # Custom claim indicating if the user is a staff member
                        }
                    }
                }
            },
            400: {
                "description": "Invalid credentials or the account is not authorized to log in "
                               "(must be a staff or admin).",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "No account found with that email."  # Example error message
                        }
                    }
                }
            },
        },
        tags=["Authentication"],  # This endpoint is grouped under 'Authentication' in the API docs
    )
    def post(self, request, *args, **kwargs):
        """
        Override the post method to add custom behavior for the admin login.

        If additional custom logic is needed before returning the response, 
        you can handle it here.
        """
        return super().post(request, *args, **kwargs)

class AdminLogoutView(APIView):
    """
    Logs out authenticated staff/admin users by blacklisting their refresh token.
    Only users with staff or admin privileges can log out.
    """

    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensures that only authenticated staff/admin users can access this view

    @extend_schema(
        description="Endpoint for logging out authenticated staff/admin users by blacklisting their refresh token.",
        request=None,  # No request body needed, the refresh token is sent in the body of the POST request
        responses={
            205: {
                "description": "Successfully logged out. Refresh token is blacklisted.",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Successfully logged out."
                        }
                    }
                }
            },
            400: {
                "description": "Bad request. Either refresh token is missing or an error occurred while processing the request.",
                "content": {
                    "application/json": {
                        "example": {
                            "error": "Refresh token is required."
                        }
                    }
                }
            }
        },
        tags=["Authentication"],  # Grouping under 'Authentication' in the API documentation
    )
    def post(self, request):
        """
        Logs out the authenticated user by blacklisting their refresh token.
        This will invalidate the refresh token and prevent further use.
        """

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
            # If an error occurs during the process, return an error message
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
                
class MmsPortCreateUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    """
    View to create or update ports.
    Requires authentication and admin/staff permissions.
    The 'portid' is used as a lookup field to identify the resource for update.
    """
    
    queryset = models.MmsPort.objects.all()
    serializer_class = serializers.MmsPortSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'portid'  # Use URL to identify the resource

    def get_object(self):
        """
        Override the get_object method to check if the portid exists before proceeding with the update.
        The 'portid' from the URL is used to fetch the port.
        """
        portid = self.kwargs['portid']
        
        try:
            # Retrieve the port object or raise a NotFound exception if it doesn't exist
            return models.MmsPort.objects.get(portid=portid)
        except models.MmsPort.DoesNotExist:
            # Handle the case where the portid does not exist
            raise NotFound(f"Port with {portid} not found.")

    @extend_schema(
        description="Create a new port. Admins and staff can create a port with necessary details.",
        request=serializers.MmsPortSerializer,  # Specifies the request body format (port details)
        responses={
            201: {
                "description": "Port successfully created.",
                "content": {
                    "application/json": {
                        "example": {
                            "portname": "Port A",
                            "address": "123 Port St.",
                            "portcity": "City A",
                            "portstate": "State A",
                            "portcountry": "Country A",
                            "nearestairport": "Airport A",
                            "parkingspots": 50
                        }
                    }
                }
            },
            400: {
                "description": "Invalid data. Failed to create the port.",
                "content": {
                    "application/json": {
                        "example": {
                            "error": "Invalid port details provided."
                        }
                    }
                }
            }
        },
        tags=["Ports"],  # Grouping under 'Ports' in the API documentation
    )
    def post(self, request, *args, **kwargs):
        """
        Create a new port using the provided details.
        Only authenticated admin or staff users are allowed to create a port.
        """
        return self.create(request=request, *args, **kwargs)

    @extend_schema(
        description="Update an existing port by its portid. Only admins and staff can update port details.",
        request=serializers.MmsPortSerializer,  # Specifies the request body format (updated port details)
        responses={
            200: {
                "description": "Port successfully updated.",
                "content": {
                    "application/json": {
                        "example": {
                            "portname": "Updated Port A",
                            "address": "456 Updated Port St.",
                            "portcity": "Updated City A",
                            "portstate": "Updated State A",
                            "portcountry": "Updated Country A",
                            "nearestairport": "Updated Airport A",
                            "parkingspots": 100
                        }
                    }
                }
            },
            400: {
                "description": "Invalid data. Failed to update the port.",
                "content": {
                    "application/json": {
                        "example": {
                            "error": "Invalid port details provided."
                        }
                    }
                }
            },
            404: {
                "description": "Port with the specified portid not found.",
                "content": {
                    "application/json": {
                        "example": {
                            "error": "Port with {portid} not found."
                        }
                    }
                }
            }
        },
        tags=["Ports"],  # Grouping under 'Ports' in the API documentation
    )
    def put(self, request, *args, **kwargs):
        """
        Update the details of an existing port identified by the portid.
        Only authenticated admin or staff users are allowed to update a port.
        """
        return self.update(request=request, *args, **kwargs)
        
class MmsPortListView(generics.ListAPIView):
    """
    API view to retrieve a list of ports.
    This view supports filtering, searching, and ordering of port data.
    It uses the MmsPortListSerializer to return serialized port data.
    """

    # Specifies the queryset that will be used for retrieving port data.
    queryset = models.MmsPort.objects.all()
    
    # Specifies the serializer class to be used to convert queryset data into JSON.
    serializer_class = serializers.MmsPortListSerializer

    # Specifies the permission classes. Only authenticated users with staff/admin roles can access this view.
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    # Specifies the filter backends to be used for filtering, searching, and ordering.
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Specifies the filter set class to be used for filtering data.
    filterset_class = filters.PortFilter

    # Specifies the fields that can be searched via the 'search' query parameter.
    search_fields = ['portname', 'portcity', 'portcountry', 'nearestairport']

    # Specifies the fields by which the results can be ordered.
    ordering_fields = ['portname', 'parkingspots']
    
    # Specifies the default ordering of results if no ordering parameter is provided.
    ordering = ['portname']

    @extend_schema(
        description="Endpoint to retrieve a list of ports. Supports filtering by portname, city, country, and nearest airport, "
                    "searching by portname, city, country, and nearest airport, and ordering by portname or parkingspots.",
        responses={
            200: {
                "description": "A list of ports matching the search and filter criteria.",
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "portname": "Port of New York",
                                "address": "1234 Port St.",
                                "portcity": "New York",
                                "portstate": "NY",
                                "portcountry": "USA",
                                "nearestairport": "JFK",
                                "parkingspots": 100
                            },
                            {
                                "portname": "Port of Los Angeles",
                                "address": "5678 Dock Rd.",
                                "portcity": "Los Angeles",
                                "portstate": "CA",
                                "portcountry": "USA",
                                "nearestairport": "LAX",
                                "parkingspots": 150
                            }
                        ]
                    }
                }
            },
            404: {
                "description": "No ports found matching the filters or search criteria.",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "No ports found matching the filters."
                        }
                    }
                }
            }
        },
        tags=["Ports"],  # This groups the endpoint under "Ports" in the API documentation
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieves a list of ports. The list can be filtered by portname, portcity, portcountry, and nearest airport,
        and it can be searched or ordered based on the criteria specified in the query parameters.
        """
        # Applies filtering, searching, and ordering to the queryset based on request parameters.
        queryset = self.filter_queryset(self.get_queryset())

        # If no ports are found, return a 404 response indicating no matching results.
        if not queryset.exists():
            return Response({"detail": "No ports found matching the filters."}, status=status.HTTP_404_NOT_FOUND)

        # Serializes the queryset into JSON format.
        serializer = self.get_serializer(queryset, many=True)

        # Returns the serialized data in the response with a 200 OK status.
        return Response(serializer.data)
    
class MmsPortDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = models.MmsPort.objects.all()
    serializer_class = serializers.MmsPortSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'portid'  # Use URL to identify the resource
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            # Customize the error response
            raise NotFound({"message": "Port not found."})
    
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
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            # Customize the error response
            raise NotFound({"message": "Restaurant not found."})
    
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
    
    def get_object(self):
        """
        Override the get_object method to check if the restaurantid exists before proceeding with update.
        """
        activityid = self.kwargs['activityid']
        
        try:
            # Retrieve the port object or raise a NotFound exception if it doesn't exist
            return models.MmsActivity.objects.get(activityid=activityid)
        except models.MmsActivity.DoesNotExist:
            # Handle the case where the portid does not exist
            raise NotFound(f"Activity with ID {activityid} not found.")
    
    def post(self, request, *args, **kwargs):
        return self.create(request=request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request=request, *args, **kwargs)

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
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            # Customize the error response
            raise NotFound({"message": "Activity not found."})
    
    def delete(self, request, *args, **kwargs):

        instance = self.get_object()  # Retrieve the object to be deleted
        self.perform_destroy(instance)  # Perform the deletion
        return Response(
            {"message": f"Activity {instance.activityname} deleted successfully."},
            status=status.HTTP_200_OK
    )
        
class MmsRoomLocCreateUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = models.MmsRoomLoc.objects.all()
    serializer_class = serializers.MmsRoomLocCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'locid'  # Use URL to identify the resource
    
    def get_object(self):
        """
        Override the get_object method to check if the locid exists before proceeding with update.
        """
        locid = self.kwargs['locid']
        
        try:
            # Retrieve the port object or raise a NotFound exception if it doesn't exist
            return models.MmsRoomLoc.objects.get(locid=locid)
        except models.MmsRoomLoc.DoesNotExist:
            # Handle the case where the portid does not exist
            raise NotFound(f"location with ID {locid} not found.")
    
    def post(self, request, *args, **kwargs):
        return self.create(request=request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request=request, *args, **kwargs)

class MmsRoomLocListView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = models.MmsRoomLoc.objects.all()
    serializer_class = serializers.MmsRoomLocListSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response(
                {"message": "No room locations found."},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
            
    def get(self, request, *args, **kwargs):
        return self.list(request=request, *args, **kwargs)   
    
class MmsRoomLocDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = models.MmsRoomLoc.objects.all()
    serializer_class = serializers.MmsRoomLocCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'locid'  # Use URL to identify the resource
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            # Customize the error response
            raise NotFound({"message": "Room location not found."})
    
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
    
    def get_object(self):
        """
        Override the get_object method to check if the restaurantid exists before proceeding with update.
        """
        stateroomtypeid = self.kwargs['stateroomtypeid']
        
        try:
            # Retrieve the port object or raise a NotFound exception if it doesn't exist
            return models.MmsRoomType.objects.get(stateroomtypeid=stateroomtypeid)
        except models.MmsRoomType.DoesNotExist:
            # Handle the case where the portid does not exist
            raise NotFound(f"stateroomtype with ID {stateroomtypeid} not found.")
    
    def post(self, request, *args, **kwargs):
        return self.create(request=request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request=request, *args, **kwargs)

class MmsRoomTypeListView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = models.MmsRoomType.objects.all()
    serializer_class = serializers.MmsRoomTypeListSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response(
                {"message": "No room types found."},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        return self.list(request=request, *args, **kwargs)   
    
class MmsRoomTypeDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):    
    queryset = models.MmsRoomType.objects.all()
    serializer_class = serializers.MmsRoomTypeCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'stateroomtypeid'  # Use URL to identify the resource
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            # Customize the error response
            raise NotFound({"message": "Room type not found."})
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()  # Retrieve the object to be deleted
        self.perform_destroy(instance)  # Perform the deletion
        return Response(
            {"message": f"State room type {instance.stateroomtype} deleted successfully."},
            status=status.HTTP_200_OK
    )    

class MmsRoomCreateView(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = models.MmsRoom.objects.all()
    serializer_class = serializers.MmsRoomsCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    
    '''def create(self, request, *args, **kwargs):
        # Extract `shipid` from the URL
        shipid = kwargs.get('shipid')
        if not shipid:
            return Response(
                {"detail": "Ship ID is required in the URL."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Ensure the ship exists before proceeding
        try:
            ship = models.MmsShip.objects.get(shipid=shipid)
        except models.MmsShip.DoesNotExist:
            return Response(
                {"detail": f"Ship with ID {shipid} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Add the `shipid` to the request data before passing it to the serializer
        request.data['shipid'] = ship.shipid
        print(request.data)
        
        # Call the parent class's create method
        return super().create(request, *args, **kwargs)'''

    def post(self, request, *args, **kwargs):
        # Directly call the create method, as validation is handled in the serializer
        return self.create(request=request, *args, **kwargs)

class MmsRoomListView(generics.ListAPIView):
    queryset = models.MmsRoom.objects.select_related('stateroomtypeid', 'locid').all()
    serializer_class = serializers.MmsRoomListSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.RoomFilter
    search_fields = ['roomnumber']
    ordering_fields = ['roomnumber', 'roomfloor', 'price']
    ordering = ['roomnumber']  
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({"detail": "No rooms found matching the filters."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
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
                           
'''

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

'''    
   
class MmsShipCreateView(generics.CreateAPIView):
    
    serializer_class = serializers.MmsShipCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    
    def post(self, request, *args, **kwargs):
        return self.create(request=request, *args, **kwargs)

class MmsShipListView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = models.MmsShip.objects.all()
    serializer_class = serializers.MmsShipListSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response(
                {"message": "No ships found."},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        return self.list(request=request, *args, **kwargs)   
                
class MmsShipDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):    
    queryset = models.MmsShip.objects.all()
    serializer_class = serializers.MmsShipCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'shipid'  # Use URL to identify the resource
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            # Customize the error response
            raise NotFound({"message": "Ship not found."})
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()  # Retrieve the object to be deleted
        self.perform_destroy(instance)  # Perform the deletion
        return Response(
            {"message": f"Ship {instance.shipname} deleted successfully."},
            status=status.HTTP_200_OK
    )     

class MmsPackageCreateUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = models.MmsPackage.objects.all()
    serializer_class = serializers.MmsPackageCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'packageid'  # Use URL to identify the resource
    
    def post(self, request, *args, **kwargs):
        return self.create(request=request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request=request, *args, **kwargs)

class MmsPackageListView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = models.MmsPackage.objects.all()
    serializer_class = serializers.MmsPackageListSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response(
                {"message": "No packages found."},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        return self.list(request=request, *args, **kwargs)   
    
class MmsPackageDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = models.MmsPackage.objects.all()
    serializer_class = serializers.MmsPackageCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'packageid'  # Use URL to identify the resource
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            # Customize the error response
            raise NotFound({"message": "Package not found."})
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()  # Retrieve the object to be deleted
        self.perform_destroy(instance)  # Perform the deletion
        return Response(
            {"message": f"Package {instance.packagename} deleted successfully."},
            status=status.HTTP_200_OK
    )
                  
class MmsTripAddView(generics.GenericAPIView, mixins.CreateModelMixin):
    
    serializer_class = serializers.MmsTripCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure staff or superuser permission is enforced
    

    def post(self, request, *args, **kwargs):
        """Handle trip creation."""
        return self.create(request=request, *args, **kwargs)

           
class MmsTripCreateUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = models.MmsTrip.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    serializer_class = serializers.MmsTripCreateSerializer
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
        