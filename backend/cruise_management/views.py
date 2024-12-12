import re
import uuid
import random
from . import models
from decimal import Decimal
from datetime import datetime
from django.http import Http404
from django.conf import settings
from django.db.models import Count
from . import filters, serializers
from django.utils.timezone import now
from django.core.mail import send_mail
from . permissions import IsAdminOrStaff
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import mixins, generics, status
from django.contrib.auth import views as auth_views
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse


class AdminLoginView(TokenObtainPairView):
    """
    Custom Token Obtain View to handle login and issue JWT tokens.
    This view uses the `AdminMmsLoginSerializer` to validate credentials
    and generate JWT tokens. Only staff and admin users are allowed to log in.
    """

    # Set the serializer class to use for validation and token generation
    serializer_class = serializers.AdminMmsLoginSerializer

    @extend_schema(
        description="Endpoint for admin users to log in. It validates the user's credentials "
                    "(email/username and password) and returns JWT tokens for authenticated users.",
        request=serializers.AdminMmsLoginSerializer,  # Specifies the expected request body format
        responses={
            200: {
                "description": "Successfully logged in. JWT tokens issued.",
                "examples": {
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
                "examples": {
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
                "examples": {
                    "application/json": {
                        "example": {
                            "message": "Successfully logged out."
                        }
                    }
                }
            },
            400: {
                "description": "Bad request. Either refresh token is missing or an error occurred while processing the request.",
                "examples": {
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

            return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_examples)
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
                "examples": {
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
                "examples": {
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
                "examples": {
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
                "examples": {
                    "application/json": {
                        "example": {
                            "error": "Invalid port details provided."
                        }
                    }
                }
            },
            404: {
                "description": "Port with the specified portid not found.",
                "examples": {
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
                "examples": {
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
                "examples": {
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
    """
    API view to delete a port entry.
    The port is identified by the 'portid' in the URL.
    Only authenticated users with staff or admin permissions can delete a port.
    """
    
    # Define the queryset and serializer class for the delete operation
    queryset = models.MmsPort.objects.all()
    serializer_class = serializers.MmsPortSerializer

    # Define the required permissions (only authenticated users who are admins or staff)
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    # Define the lookup field to use in the URL for identifying the resource
    lookup_field = 'portid'  # Use URL parameter 'portid' to identify the resource

    def get_object(self):
        """
        Custom method to retrieve the port object based on the provided 'portid' from the URL.
        If the object does not exist, a custom 'NotFound' error response is raised.
        """
        try:
            # Use the parent method to get the object (based on 'portid')
            return super().get_object()
        except Http404:
            # If the port object is not found, raise a NotFound error with a custom message
            raise NotFound({"message": "Port not found."})

    @extend_schema(
        description="Endpoint to delete a port by its unique 'portid'. Only authenticated users with admin or staff permissions can perform the deletion.",
        request=None,  # No request body required for this operation
        responses={
            200: {
                "description": "Port successfully deleted.",
                "examples": {
                    "application/json": {
                        "example": {
                            "message": "PortName deleted successfully from the database."
                        }
                    }
                }
            },
            404: {
                "description": "Port not found.",
                "examples": {
                    "application/json": {
                        "example": {
                            "message": "Port not found."
                        }
                    }
                }
            },
            400: {
                "description": "Bad request or insufficient permissions.",
                "examples": {
                    "application/json": {
                        "example": {
                            "detail": "Authentication credentials were not provided."
                        }
                    }
                }
            }
        },
        tags=["Port Management"],  # Tag for grouping the endpoint in documentation
    )
    def delete(self, request, *args, **kwargs):
        """
        Handle the DELETE request to delete a specific port.
        Upon successful deletion, returns a success message with the deleted port's name.
        """
        instance = self.get_object()  # Retrieve the port instance to delete
        pid = instance.portname  # Store the port name for the success message

        # Perform the actual deletion using the 'perform_destroy' method from DestroyModelMixin
        self.perform_destroy(instance)

        # Return a response indicating that the port was successfully deleted
        return Response(
            {"message": f"{pid} deleted successfully from the database."},
            status=status.HTTP_200_OK  # HTTP status code 200 OK for successful deletion
        )
                   
class MmsRestaurantCreateUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    """
    API view to create or update a restaurant entry.
    The restaurant is identified by the 'restaurantid' in the URL.
    Only authenticated users with staff or admin permissions can create or update a restaurant.
    """
    
    queryset = models.MmsRestaurant.objects.all()  # The queryset for the restaurant model
    serializer_class = serializers.MmsRestaurantCreateUpdateSerializer  # Serializer for creating/updating restaurants
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure the user is authenticated and an admin or staff member
    lookup_field = 'restaurantid'  # Use the 'restaurantid' URL parameter to identify the resource

    def get_object(self):
        """
        Override the get_object method to retrieve the restaurant object based on 'restaurantid'.
        If the restaurant does not exist, a NotFound exception is raised with a custom error message.
        """
        restaurantid = self.kwargs['restaurantid']  # Extract restaurantid from the URL kwargs
        
        try:
            # Try to get the restaurant by 'restaurantid'
            return models.MmsRestaurant.objects.get(restaurantid=restaurantid)
        except models.MmsRestaurant.DoesNotExist:
            # If the restaurant does not exist, raise a NotFound error
            raise NotFound(f"Restaurant with ID {restaurantid} not found.")

    @extend_schema(
        description="Create a new restaurant entry. Only accessible to authenticated users with staff or admin permissions.",
        request=serializers.MmsRestaurantCreateUpdateSerializer,  # Serializer to validate request data for creating a restaurant
        responses={
            201: {
                "description": "Successfully created a new restaurant.",
                "examples": {
                    "application/json": {
                        "example": {
                            "restaurantname": "Restaurant A",
                            "floornumber": 1,
                            "openingtime": "08:00",
                            "closingtime": "22:00",
                            "servesbreakfast": "Y",
                            "serveslunch": "Y",
                            "servesdinner": "Y",
                            "servesalcohol": "Y",
                            "restaurant_description": "A great place for all meals."
                        }
                    }
                }
            },
            400: {
                "description": "Invalid data or missing required fields.",
                "examples": {
                    "application/json": {
                        "example": {
                            "detail": "Missing required fields or invalid values."
                        }
                    }
                }
            }
        },
        tags=["Restaurant Management"],  # API group for restaurant-related operations
    )
    def post(self, request, *args, **kwargs):
        """
        Handle the POST request to create a new restaurant.
        Uses the serializer to validate and create the restaurant entry.
        """
        return self.create(request=request, *args, **kwargs)  # Call the 'create' method from CreateModelMixin

    @extend_schema(
        description="Update an existing restaurant entry. Only accessible to authenticated users with staff or admin permissions.",
        request=serializers.MmsRestaurantCreateUpdateSerializer,  # Serializer to validate request data for updating a restaurant
        responses={
            200: {
                "description": "Successfully updated the restaurant.",
                "examples": {
                    "application/json": {
                        "example": {
                            "restaurantname": "Updated Restaurant A",
                            "floornumber": 2,
                            "openingtime": "09:00",
                            "closingtime": "23:00",
                            "servesbreakfast": "Y",
                            "serveslunch": "Y",
                            "servesdinner": "Y",
                            "servesalcohol": "Y",
                            "restaurant_description": "Updated description for restaurant."
                        }
                    }
                }
            },
            400: {
                "description": "Invalid data or missing required fields.",
                "examples": {
                    "application/json": {
                        "example": {
                            "detail": "Missing required fields or invalid values."
                        }
                    }
                }
            },
            404: {
                "description": "Restaurant not found for the provided restaurantid.",
                "examples": {
                    "application/json": {
                        "example": {
                            "message": "Restaurant with ID X not found."
                        }
                    }
                }
            }
        },
        tags=["Restaurant Management"],  # API group for restaurant-related operations
    )
    def put(self, request, *args, **kwargs):
        """
        Handle the PUT request to update an existing restaurant.
        Uses the serializer to validate and update the restaurant entry.
        """
        return self.update(request=request, *args, **kwargs)  # Call the 'update' method from UpdateModelMixin

class MmsRestaurantListView(generics.ListAPIView):
    """
    API view to retrieve a list of restaurants with optional filtering, searching, and ordering.
    This view allows authenticated users with staff or admin permissions to list all restaurants
    and apply filters or search criteria.
    """

    queryset = models.MmsRestaurant.objects.all()  # The queryset for the restaurant model
    serializer_class = serializers.MmsRestaurantListSerializer  # Serializer to transform restaurant data into JSON
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure the user is authenticated and has the correct permissions
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]  # Enable filtering, searching, and ordering
    filterset_class = filters.RestaurantFilter  # Define custom filters for the restaurant list
    search_fields = ['restaurantname']  # Allow searching by the restaurant name
    ordering_fields = ['restaurantname']  # Allow ordering by restaurant name
    ordering = ['restaurantname']  # Default ordering by restaurant name

    @extend_schema(
        description="Retrieve a list of all restaurants with optional filtering, searching, and ordering.",
        responses={
            200: {
                "description": "Successfully retrieved the list of restaurants.",
                "examples": {
                    "application/json": {
                        "example": [
                            {
                                "restaurantname": "Restaurant A",
                                "floornumber": 1,
                                "openingtime": "08:00",
                                "closingtime": "22:00",
                                "servesbreakfast": "Y",
                                "serveslunch": "Y",
                                "servesdinner": "Y",
                                "servesalcohol": "Y",
                                "restaurant_description": "A great place for all meals."
                            },
                            {
                                "restaurantname": "Restaurant B",
                                "floornumber": 2,
                                "openingtime": "07:00",
                                "closingtime": "23:00",
                                "servesbreakfast": "N",
                                "serveslunch": "Y",
                                "servesdinner": "Y",
                                "servesalcohol": "Y",
                                "restaurant_description": "Best place for dinner."
                            }
                        ]
                    }
                }
            },
            404: {
                "description": "No restaurants found matching the applied filters or search criteria.",
                "examples": {
                    "application/json": {
                        "example": {
                            "detail": "No restaurants found matching the filters."
                        }
                    }
                }
            }
        },
        tags=["Restaurant Management"],  # API group for restaurant-related operations
    )
    def list(self, request, *args, **kwargs):
        """
        Handle the GET request to retrieve the list of restaurants.
        Applies filtering, searching, and ordering based on the request parameters.
        """
        queryset = self.filter_queryset(self.get_queryset())  # Apply any filters to the queryset
        if not queryset.exists():  # Check if any restaurants exist after filtering
            return Response({"detail": "No restaurants found matching the filters."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset, many=True)  # Serialize the queryset into JSON
        return Response(serializer.data)  # Return the serialized data in the response
        
class MmsRestaurantDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    """
    API view to delete a restaurant entry by its 'restaurantid'.
    Only authenticated users with staff or admin permissions can delete a restaurant.
    """

    queryset = models.MmsRestaurant.objects.all()  # The queryset for the restaurant model
    serializer_class = serializers.MmsRestaurantCreateUpdateSerializer  # Serializer for restaurant data
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure the user is authenticated and has staff/admin permissions
    lookup_field = 'restaurantid'  # Use the 'restaurantid' URL parameter to identify the resource


    def get_object(self):
        """
        Override the get_object method to retrieve the restaurant object based on 'restaurantid'.
        If the restaurant does not exist, a NotFound exception is raised with a custom error message.
        """
        try:
            return super().get_object()  # Attempt to get the restaurant object
        except Http404:
            # If the restaurant does not exist, raise a NotFound exception with a custom message
            raise NotFound({"message": "Restaurant not found."})

    @extend_schema(
        description="Handle the DELETE request to delete a restaurant entry.",
        responses={
            200: {
                "description": "Successfully deleted the restaurant.",
                "examples": {
                    "application/json": {
                        "example": {
                            "message": "Restaurant Restaurant A deleted successfully."
                        }
                    }
                }
            },
            404: {
                "description": "Restaurant not found for the provided restaurantid.",
                "examples": {
                    "application/json": {
                        "example": {
                            "message": "Restaurant with ID X not found."
                        }
                    }
                }
            }
        },
        tags=["Restaurant Management"],  # API group for restaurant-related operations
    )
    def delete(self, request, *args, **kwargs):
        """
        Handle the DELETE request to delete a restaurant entry.
        Deletes the restaurant from the database and returns a success message.
        """
        instance = self.get_object()  # Retrieve the restaurant object to be deleted
        self.perform_destroy(instance)  # Perform the deletion
        return Response(
            {"message": f"Restaurant {instance.restaurantname} deleted successfully."},
            status=status.HTTP_200_OK  # Return 200 OK if the deletion is successful
        )
    
class MmsActivityCreateUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    """
    API view to create or update an activity entry.
    The activity is identified by the 'activityid' in the URL.
    Only authenticated users with staff or admin permissions can create or update an activity.
    """
    
    queryset = models.MmsActivity.objects.all()  # The queryset for the activity model
    serializer_class = serializers.MmsActivityCreateUpdateSerializer  # Serializer for creating/updating activities
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure the user is authenticated and has staff/admin permissions
    lookup_field = 'activityid'  # Use 'activityid' as the identifier for the resource in the URL

    @extend_schema(
        description="Create a new activity entry. Only accessible to authenticated users with staff or admin permissions.",
        request=serializers.MmsActivityCreateUpdateSerializer,  # Serializer to validate request data for creating an activity
        responses={
            201: {
                "description": "Successfully created a new activity.",
                "examples": {
                    "application/json": {
                        "example": {
                            "activitytype": "sports",
                            "activityname": "Basketball",
                            "activitydescription": "An exciting basketball game.",
                            "floor": 1,
                            "capacity": 50
                        }
                    }
                }
            },
            400: {
                "description": "Invalid data or missing required fields.",
                "examples": {
                    "application/json": {
                        "example": {
                            "detail": "Missing required fields or invalid values."
                        }
                    }
                }
            }
        },
        tags=["Activity Management"],  # API group for activity-related operations
    )
    def post(self, request, *args, **kwargs):
        """
        Handle the POST request to create a new activity.
        Uses the serializer to validate and create the activity entry.
        """
        return self.create(request=request, *args, **kwargs)  # Call the 'create' method from CreateModelMixin

    @extend_schema(
        description="Update an existing activity entry. Only accessible to authenticated users with staff or admin permissions.",
        request=serializers.MmsActivityCreateUpdateSerializer,  # Serializer to validate request data for updating an activity
        responses={
            200: {
                "description": "Successfully updated the activity.",
                "examples": {
                    "application/json": {
                        "example": {
                            "activitytype": "sports",
                            "activityname": "Updated Basketball",
                            "activitydescription": "Updated description for basketball game.",
                            "floor": 1,
                            "capacity": 60
                        }
                    }
                }
            },
            400: {
                "description": "Invalid data or missing required fields.",
                "examples": {
                    "application/json": {
                        "example": {
                            "detail": "Missing required fields or invalid values."
                        }
                    }
                }
            },
            404: {
                "description": "Activity not found for the provided activityid.",
                "examples": {
                    "application/json": {
                        "example": {
                            "message": "Activity with ID X not found."
                        }
                    }
                }
            }
        },
        tags=["Activity Management"],  # API group for activity-related operations
    )
    def put(self, request, *args, **kwargs):
        """
        Handle the PUT request to update an existing activity.
        Uses the serializer to validate and update the activity entry.
        """
        return self.update(request=request, *args, **kwargs)  # Call the 'update' method from UpdateModelMixin

class MmsActivityListView(generics.ListAPIView):
    """
    API view to retrieve a list of activities.
    It supports filtering, searching, and ordering based on activity name.
    Only accessible by authenticated users with staff or admin permissions.
    """
    
    queryset = models.MmsActivity.objects.all()  # The queryset to retrieve the activities
    serializer_class = serializers.MmsActivityListSerializer  # Serializer to format the response data
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Restrict access to authenticated users with staff/admin permissions
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]  # Enable filtering, search, and ordering
    filterset_class = filters.ActivityFilter  # Custom filter for activities
    search_fields = ['activityname']  # Allow searching by activity name
    ordering_fields = ['activityname']  # Allow ordering by activity name
    ordering = ['activityname']  # Default ordering by activity name

    @extend_schema(
        description="Retrieve a list of activities. Supports filtering, searching, and ordering.",
        responses={
            200: {
                "description": "List of activities.",
                "examples": {
                    "application/json": {
                        "example": [
                            {
                                "activitytype": "sports",
                                "activityname": "Basketball",
                                "activitydescription": "An exciting basketball game.",
                                "floor": 1,
                                "capacity": 50
                            },
                            {
                                "activitytype": "entertainment",
                                "activityname": "Movie Night",
                                "activitydescription": "Watch the latest blockbuster.",
                                "floor": 2,
                                "capacity": 100
                            }
                        ]
                    }
                }
            },
            404: {
                "description": "No activities found matching the filters.",
                "examples": {
                    "application/json": {
                        "example": {
                            "detail": "No activities found matching the filters."
                        }
                    }
                }
            }
        },
        tags=["Activity Management"]  # API grouping for activity-related operations
    )
    def list(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve a list of activities.
        Filters and paginates the queryset based on request parameters.
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        if not queryset.exists():
            return Response({"detail": "No activities found matching the filters."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset, many=True)  # Serialize the filtered queryset
        return Response(serializer.data)  # Return the serialized data in the response

class MmsActivityDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    """
    API view to delete an activity entry by its ID.
    Only accessible by authenticated users with staff or admin permissions.
    """

    queryset = models.MmsActivity.objects.all()  # The queryset to retrieve the activities
    serializer_class = serializers.MmsActivityCreateUpdateSerializer  # Serializer used for the response
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Restrict access to authenticated users with staff/admin permissions
    lookup_field = 'activityid'  # The identifier to locate the activity in the URL

    @extend_schema(
        description="Delete an activity by its ID.",
        responses={
            200: {
                "description": "Successfully deleted the activity.",
                "examples": {
                    "application/json": {
                        "example": {
                            "message": "Activity Basketball deleted successfully."
                        }
                    }
                }
            },
            404: {
                "description": "Activity not found for the provided ID.",
                "examples": {
                    "application/json": {
                        "example": {
                            "message": "Activity not found."
                        }
                    }
                }
            }
        },
        tags=["Activity Management"]  # API grouping for activity-related operations
    )
    def delete(self, request, *args, **kwargs):
        """
        Handles DELETE requests to delete an activity by its ID.
        Deletes the activity from the database and returns a success message.
        """
        instance = self.get_object()  # Retrieve the activity object based on the provided ID
        self.perform_destroy(instance)  # Perform the deletion of the activity
        return Response(
            {"message": f"Activity {instance.activityname} deleted successfully."},
            status=status.HTTP_200_OK
        )

class MmsRoomLocCreateUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    """
    API view to create or update MmsRoomLoc (room location) entries.
    The location is identified by the 'locid' in the URL.
    Only authenticated users with staff or admin permissions can create or update room locations.
    """
    
    queryset = models.MmsRoomLoc.objects.all()  # The queryset for the MmsRoomLoc model
    serializer_class = serializers.MmsRoomLocCreateUpdateSerializer  # Serializer to validate input data
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure the user is authenticated and has required permissions
    lookup_field = 'locid'  # Use 'locid' URL parameter to identify the resource

    def get_object(self):
        """
        Override the get_object method to retrieve the MmsRoomLoc object based on 'locid'.
        If the object does not exist, raise a NotFound exception with a custom error message.
        """
        locid = self.kwargs['locid']  # Extract locid from the URL kwargs
        
        try:
            return models.MmsRoomLoc.objects.get(locid=locid)  # Try to retrieve the object by locid
        except models.MmsRoomLoc.DoesNotExist:
            # If the object does not exist, raise a NotFound error
            raise NotFound(f"Location with ID {locid} not found.")

    @extend_schema(
        description="Create a new room location entry. Only accessible to authenticated users with staff or admin permissions.",
        request=serializers.MmsRoomLocCreateUpdateSerializer,  # Serializer to validate request data for creating a room location
        responses={
            201: {
                "description": "Successfully created a new room location.",
                "examples": {
                    "application/json": {
                        "example": {
                            "location": "bow"
                        }
                    }
                }
            },
            400: {
                "description": "Invalid data or missing required fields.",
                "examples": {
                    "application/json": {
                        "example": {
                            "detail": "Missing required fields or invalid values."
                        }
                    }
                }
            }
        },
        tags=["Room Location Management"],  # API group for room location-related operations
    )
    def post(self, request, *args, **kwargs):
        """
        Handle the POST request to create a new room location.
        Uses the serializer to validate and create the room location entry.
        """
        return self.create(request=request, *args, **kwargs)

    @extend_schema(
        description="Update an existing room location entry. Only accessible to authenticated users with staff or admin permissions.",
        request=serializers.MmsRoomLocCreateUpdateSerializer,  # Serializer to validate request data for updating a room location
        responses={
            200: {
                "description": "Successfully updated the room location.",
                "examples": {
                    "application/json": {
                        "example": {
                            "location": "stern"
                        }
                    }
                }
            },
            400: {
                "description": "Invalid data or missing required fields.",
                "examples": {
                    "application/json": {
                        "example": {
                            "detail": "Missing required fields or invalid values."
                        }
                    }
                }
            },
            404: {
                "description": "Room location not found for the provided locid.",
                "examples": {
                    "application/json": {
                        "example": {
                            "message": "Location with ID X not found."
                        }
                    }
                }
            }
        },
        tags=["Room Location Management"],  # API group for room location-related operations
    )
    def put(self, request, *args, **kwargs):
        """
        Handle the PUT request to update an existing room location.
        Uses the serializer to validate and update the room location entry.
        """
        return self.update(request=request, *args, **kwargs)

class MmsRoomLocListView(generics.GenericAPIView, mixins.ListModelMixin):
    """
    API view to list all room locations.
    The view allows filtering and pagination of the room locations.
    Only authenticated users with staff or admin permissions can access this view.
    """
    
    queryset = models.MmsRoomLoc.objects.all()  # Queryset to retrieve all MmsRoomLoc objects
    serializer_class = serializers.MmsRoomLocListSerializer  # Serializer to serialize room location data
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure the user is authenticated and has required permissions

    @extend_schema(
        description="Retrieve a list of all room locations.",
        responses={
            200: {
                "description": "Successfully retrieved the list of room locations.",
                "examples": {
                    "application/json": {
                        "example": [
                            {"location": "bow"},
                            {"location": "stern"},
                            {"location": "port side"}
                        ]
                    }
                }
            },
            404: {
                "description": "No room locations found matching the filters.",
                "examples": {
                    "application/json": {
                        "example": {
                            "message": "No room locations found."
                        }
                    }
                }
            }
        },
        tags=["Room Location Management"]  # API group for room location-related operations
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieve and return a list of room locations. If no room locations exist,
        a 404 message is returned.
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        if not queryset.exists():
            return Response(
                {"message": "No room locations found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to list room locations.
        This method calls the list method to retrieve and return room locations.
        """
        return self.list(request=request, *args, **kwargs)
   
class MmsRoomLocDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    """
    View to delete a room location based on the `locid` provided in the URL.
    This view allows only authenticated admin or staff users to delete room locations.
    
    - The view handles the deletion of a room location identified by the `locid`.
    - Upon successful deletion, a message confirming the deletion is returned.
    - If the resource (room location) is not found, a custom error message is returned.
    """
    
    # Queryset to fetch all room locations
    queryset = models.MmsRoomLoc.objects.all()
    
    # Serializer class to validate the data if needed, but it's not used in this delete operation
    serializer_class = serializers.MmsRoomLocCreateUpdateSerializer
    
    # Permission classes to ensure only authenticated admin or staff users can access this view
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    
    # URL parameter name used to identify the resource
    lookup_field = 'locid'

    
    def get_object(self):
        """
        Retrieve the room location object based on the `locid` URL parameter.
        If the object does not exist, raise a `NotFound` exception with a custom message.
        """
        try:
            return super().get_object()
        except Http404:
            # Customize the error response if the object is not found
            raise NotFound({"message": "Room location not found."})

    @extend_schema(
        description="Endpoint to delete a room location based on `locid`.",
        responses={
            200: OpenApiResponse(
                description="Room location deleted successfully.",
                examples={
                    "application/json": {
                        "message": "Location [location_name] deleted successfully."
                    }
                }
            ),
            404: OpenApiResponse(
                description="Room location not found.",
                examples={
                    "application/json": {
                        "message": "Room location not found."
                    }
                }
            ),
        },
        tags=["Room Location Management"],  # Organize the endpoint under 'Room Location Management'
    )
    def delete(self, request, *args, **kwargs):
        """
        Handle the DELETE request for removing a room location from the database.
        - Retrieves the object using the `get_object` method.
        - Deletes the object from the database and returns a success message.
        - If the room location is not found, an error message is returned.
        """
        instance = self.get_object()  # Retrieve the object to be deleted
        self.perform_destroy(instance)  # Perform the deletion of the object
        return Response(
            {"message": f"Location {instance.location} deleted successfully."},
            status=status.HTTP_200_OK
        )

class MmsRoomTypeCreateUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    """
    View to create or update a Room Type (stateroom type) in the system.
    This view allows authenticated users with admin or staff permissions to create or update a room type.
    The room type is identified using the `stateroomtypeid` from the URL.
    """
    
    queryset = models.MmsRoomType.objects.all()
    serializer_class = serializers.MmsRoomTypeCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'stateroomtypeid'  # Use URL to identify the resource
    
    def get_object(self):
        """
        Override the `get_object` method to retrieve a specific room type (stateroom type) by its ID.
        If the object doesn't exist, raise a `NotFound` exception with a custom error message.
        """
        stateroomtypeid = self.kwargs['stateroomtypeid']  # Fetch the stateroomtypeid from the URL
        
        try:
            # Attempt to retrieve the room type object based on the provided ID
            return models.MmsRoomType.objects.get(stateroomtypeid=stateroomtypeid)
        except models.MmsRoomType.DoesNotExist:
            # Handle the case when the room type doesn't exist and return a custom error
            raise NotFound(f"stateroomtype with ID {stateroomtypeid} not found.")
    
    @extend_schema(
        description="Create a new room type. Authenticated users with admin or staff permissions can create a new room type.",
        request=serializers.MmsRoomTypeCreateUpdateSerializer,  # Request body format for creating a new room type
        responses={
            201: OpenApiResponse(
                description="Successfully created a new room type.",
                examples={"application/json": {"example": {"stateroomtypeid": 1, "name": "Deluxe", "description": "A luxurious room type."}}}
            ),
            400: OpenApiResponse(
                description="Invalid request data, validation errors.",
                examples={"application/json": {"example": {"detail": "Invalid data."}}}
            ),
        },
        tags=["Room Type Management"]
    )
    def post(self, request, *args, **kwargs):
        """
        Handle the POST request to create a new room type. It utilizes the `create` method from `CreateModelMixin`.
        """
        return self.create(request=request, *args, **kwargs)
    
    @extend_schema(
        description="Update an existing room type by its ID. Only authenticated admin or staff users can update room types.",
        request=serializers.MmsRoomTypeCreateUpdateSerializer,  # Request body format for updating an existing room type
        responses={
            200: OpenApiResponse(
                description="Successfully updated the room type.",
                examples={"application/json": {"example": {"stateroomtypeid": 1, "name": "Deluxe Updated", "description": "Updated description for the room."}}}
            ),
            400: OpenApiResponse(
                description="Invalid request data, validation errors.",
                examples={"application/json": {"example": {"detail": "Invalid data."}}}
            ),
            404: OpenApiResponse(
                description="Room type not found.",
                examples={"application/json": {"example": {"detail": "stateroomtype with ID 1 not found."}}}
            ),
        },
        tags=["Room Type Management"]
    )
    def put(self, request, *args, **kwargs):
        """
        Handle the PUT request to update an existing room type. It utilizes the `update` method from `UpdateModelMixin`.
        """
        return self.update(request=request, *args, **kwargs)
    
class MmsRoomTypeListView(generics.GenericAPIView, mixins.ListModelMixin):
    """
    View to list all room types (stateroom types) in the system.
    """
    queryset = models.MmsRoomType.objects.all()
    serializer_class = serializers.MmsRoomTypeListSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def list(self, request, *args, **kwargs):
        """
        Retrieve the list of room types (stateroom types).
        """
        queryset = self.filter_queryset(self.get_queryset())  # Apply filters
        if not queryset.exists():
            return Response({"message": "No room types found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        description="Retrieve a list of all room types. Authenticated users with admin or staff permissions can view the list.",
        responses={
            200: OpenApiResponse(
                description="List of room types successfully retrieved.",
                examples={"application/json": {"example": [{"stateroomtypeid": 1, "name": "Deluxe", "description": "A luxurious room type."}]}},
            ),
            404: OpenApiResponse(description="No room types found."),
        },
        tags=["Room Type Management"]
    )
    def get(self, request, *args, **kwargs):
        """
        Handle GET request to retrieve room types.
        """
        return self.list(request=request, *args, **kwargs)

class MmsRoomTypeDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    """
    API view to delete a specific room locattypeion.
    The room type is identified by its 'stateroomtypeid' in the URL path.
    Only authenticated users with staff or admin permissions can delete room locations.
    """
    
    queryset = models.MmsRoomType.objects.all()  # Queryset to retrieve all MmsRoomLoc objects
    serializer_class = serializers.MmsRoomTypeCreateUpdateSerializer  # Serializer used for object deletion
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure the user is authenticated and has required permissions
    lookup_field = 'stateroomtypeid'  # The field to look up the object to be deleted (via locid)

    def get_object(self):
        """
        Override the get_object method to retrieve a specific room type
        based on the 'typeid' from the URL.
        If the room type is not found, a NotFound error is raised.
        """
        try:
            return super().get_object()  # Attempt to retrieve the object
        except Http404:
            # Customize the error response if the room type is not found
            raise NotFound({"message": "Room type not found."})

    @extend_schema(
        description="Delete a specific room type by its stateroomtypeid.",
        responses={
            200: OpenApiResponse(
                description="Successfully deleted the room type.",
                examples={
                    "application/json": {
                        "example": {
                            "message": "Room type The Haven Suite deleted successfully."
                        }
                    }
                }
            ),
            404: OpenApiResponse(
                description="Room type not found for the given stateroomtypeid.",
                examples={
                    "application/json": {
                        "example": {
                            "message": "Room type not found."
                        }
                    }
                }
            )
        },
        tags=["Room Management"]  # API group for room location-related operations
    )
    def delete(self, request, *args, **kwargs):
        """
        Handle the DELETE request to remove a room type.
        This method first retrieves the room type object and then deletes it.
        """
        instance = self.get_object()  # Retrieve the object to be deleted
        self.perform_destroy(instance)  # Perform the deletion
        return Response(
            {"message": f"Room Type {instance.stateroomtype} deleted successfully."},  # Confirmation message
            status=status.HTTP_200_OK  # HTTP status code for successful deletion
        )

class MmsRoomCreateView(generics.GenericAPIView, mixins.CreateModelMixin):
    """
    API view to create a new room.
    Only authenticated users with staff or admin permissions can create a room.
    """
    
    queryset = models.MmsRoom.objects.all()  # Queryset to retrieve all MmsRoom objects
    serializer_class = serializers.MmsRoomsCreateSerializer  # Serializer used for room creation
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure the user is authenticated and has required permissions

    @extend_schema(
        description="Create a new room.",
        request=serializers.MmsRoomsCreateSerializer,  # Specifies the expected request body format
        responses={
            201: OpenApiResponse(
                description="Successfully created a new room.",
                examples={
                    "application/json": {
                        "example": {
                            "message": "Room created successfully.",
                            "roomid": 123,  # Example room ID
                            "location": "Deck 5",  # Example room location
                        }
                    }
                }
            ),
            400: OpenApiResponse(
                description="Invalid request or missing required data.",
                examples={
                    "application/json": {
                        "example": {
                            "detail": "Some required field is missing."
                        }
                    }
                }
            ),
        },
        tags=["Room Management"]  # API group for room-related operations
    )
    def post(self, request, *args, **kwargs):
        """
        Handle the POST request to create a new room.
        The room creation logic is handled by the serializer.
        """
        return self.create(request=request, *args, **kwargs)

class MmsRoomListView(generics.ListAPIView):
    """
    API view to retrieve a list of rooms.
    Supports filtering, searching, and ordering of room data.
    Only authenticated users with staff or admin permissions can access this list.
    """
    
    queryset = models.MmsRoom.objects.select_related('stateroomtypeid', 'locid').all()
    serializer_class = serializers.MmsRoomListSerializer  # Serializer used for room listing
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure the user is authenticated and has required permissions
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]  # Enable filtering, searching, and ordering
    filterset_class = filters.RoomFilter  # Apply custom filterset
    search_fields = ['roomnumber']  # Enable search by room number
    ordering_fields = ['roomnumber', 'roomfloor', 'price']  # Allow ordering by specific fields
    ordering = ['roomnumber']  # Default ordering by room number

    @extend_schema(
        description="Retrieve a list of rooms with optional filtering, searching, and ordering.",
        responses={
            200: OpenApiResponse(
                description="List of rooms retrieved successfully.",
                examples={
                    "application/json": {
                        "example": [
                            {
                                "roomid": 123,
                                "roomnumber": "101",
                                "roomfloor": 1,
                                "price": 200,
                                "location": "Deck 5",
                                "stateroomtype": "Single"
                            },
                            {
                                "roomid": 124,
                                "roomnumber": "102",
                                "roomfloor": 1,
                                "price": 250,
                                "location": "Deck 5",
                                "stateroomtype": "Double"
                            }
                        ]
                    }
                }
            ),
            404: OpenApiResponse(
                description="No rooms found matching the filters.",
                examples={
                    "application/json": {
                        "example": {
                            "detail": "No rooms found matching the filters."
                        }
                    }
                }
            ),
        },
        tags=["Room Management"]  # API group for room-related operations
    )
    def list(self, request, *args, **kwargs):
        """
        Handle the GET request to list rooms.
        Applies the filters, search, and ordering before returning the results.
        """
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({"detail": "No rooms found matching the filters."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class MmsRoomDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    """
    API view to delete a specific room.
    The room is identified by its 'roomnumber' in the URL path.
    Only authenticated users with staff or admin permissions can delete rooms.
    """
    
    queryset = models.MmsRoom.objects.all()  # Queryset to retrieve all MmsRoom objects
    serializer_class = serializers.MmsRoomBaseSerializer  # Serializer used for room deletion
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure the user is authenticated and has required permissions
    lookup_field = 'roomnumber'  # The field to look up the object to be deleted (via roomnumber)
    
    @extend_schema(
        description="Delete a specific room by its roomnumber.",
        responses={
            200: OpenApiResponse(
                description="Successfully deleted the room.",
                examples={
                    "application/json": {
                        "example": {
                            "message": "Room 101 deleted successfully."
                        }
                    }
                }
            ),
            404: OpenApiResponse(
                description="Room not found for the given roomnumber.",
                examples={
                    "application/json": {
                        "example": {
                            "detail": "Room with roomnumber 101 not found."
                        }
                    }
                }
            ),
        },
        tags=["Room Management"]  # API group for room-related operations
    )
    def delete(self, request, *args, **kwargs):
        """
        Handle the DELETE request to remove a room.
        This method retrieves the room object and deletes it.
        """
        instance = self.get_object()  # Retrieve the object to be deleted
        self.perform_destroy(instance)  # Perform the deletion (handled by DestroyModelMixin)
        return Response(
            {"message": f"Room {instance.roomnumber} deleted successfully."},
            status=status.HTTP_200_OK  # 200 for success, can also use 204 for no examples
        )                
   
class MmsShipCreateView(generics.CreateAPIView):
    """
    API view to create a new ship.
    Only authenticated users with staff or admin permissions can create ships.
    """
    
    serializer_class = serializers.MmsShipCreateSerializer  # Serializer used for ship creation
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure the user is authenticated and has required permissions
    
    @extend_schema(
        description="Create a new ship. The request body should contain the ship details, and a new ship will be created.",
        responses={
            201: OpenApiResponse(
                description="Successfully created the ship.",
                examples={
                    "application/json": {
                        "example": {
                            "shipid": 1,
                            "shipname": "Titanic",
                            "description": "Luxury cruise ship",
                            "capacity": 2500,
                            "activities": "Swimming, Dining, Shopping",
                            "restaurants": "Fine Dining, Buffet",
                            "rooms": "500"
                        }
                    }
                }
            ),
            400: OpenApiResponse(
                description="Bad request, possibly invalid data in the request body.",
                examples={
                    "application/json": {
                        "example": {
                            "detail": "Invalid data provided."
                        }
                    }
                }
            ),
        },
        tags=["Ship Management"]  # API group for ship-related operations
    )
    def post(self, request, *args, **kwargs):
        """
        Handle the POST request to create a new ship.
        This method uses the provided data and the serializer to create a new ship.
        """
        return self.create(request=request, *args, **kwargs)

class MmsShipListView(generics.GenericAPIView, mixins.ListModelMixin):
    """
    API view to list all ships.
    Only authenticated users with staff or admin permissions can view the list of ships.
    """

    queryset = models.MmsShip.objects.all()  # Queryset for retrieving ships
    serializer_class = serializers.MmsShipListSerializer  # Serializer used for ship listing
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure the user is authenticated and has required permissions
    
    @extend_schema(
        description="List all ships. The response includes details such as ship name, capacity, activities, and more.",
        responses={
            200: OpenApiResponse(
                description="Successfully retrieved the list of ships.",
                examples={
                    "application/json": {
                        "example": [
                            {
                                "shipid": 1,
                                "shipname": "Titanic",
                                "description": "Luxury cruise ship",
                                "capacity": 2500,
                                "activities": "Swimming, Dining, Shopping",
                                "restaurants": "Fine Dining, Buffet",
                                "rooms": 500
                            }
                        ]
                    }
                }
            ),
            404: OpenApiResponse(
                description="No ships found.",
                examples={
                    "application/json": {
                        "example": {
                            "message": "No ships found."
                        }
                    }
                }
            ),
        },
        tags=["Ship Management"]  # API group for ship-related operations
    )
    def list(self, request, *args, **kwargs):
        """
        Handle the GET request to retrieve the list of ships.
        This method retrieves all ships and applies filters if needed.
        """
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
    """
    API view to delete a specific ship.
    The ship is identified by its 'shipid' in the URL path.
    Only authenticated users with staff or admin permissions can delete ships.
    """
    
    queryset = models.MmsShip.objects.all()  # Queryset to retrieve all MmsShip objects
    serializer_class = serializers.MmsShipCreateSerializer  # Serializer used for deletion (may use a different serializer for response)
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure the user is authenticated and has required permissions
    lookup_field = 'shipid'  # Use URL to identify the resource
    
    @extend_schema(
        description="Delete a specific ship identified by 'shipid'. Only admins or staff can delete ships.",
        responses={
            200: OpenApiResponse(
                description="Successfully deleted the ship.",
                examples={
                    "application/json": {
                        "example": {
                            "message": "Ship Titanic deleted successfully."
                        }
                    }
                }
            ),
            404: OpenApiResponse(
                description="Ship not found for the given 'shipid'.",
                examples={
                    "application/json": {
                        "example": {
                            "message": "Ship not found."
                        }
                    }
                }
            ),
        },
        tags=["Ship Management"]  # API group for ship-related operations
    )
    def delete(self, request, *args, **kwargs):
        """
        Handle the DELETE request to remove a specific ship.
        This method first retrieves the ship object and then deletes it.
        """
        instance = self.get_object()  # Retrieve the object to be deleted
        self.perform_destroy(instance)  # Perform the deletion (handled by DestroyModelMixin)
        return Response(
            {"message": f"Ship {instance.shipname} deleted successfully."},
            status=status.HTTP_200_OK
        )
        
class MmsPackageCreateUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    """
    API view to create or update a package.
    The package is identified by its 'packageid' in the URL for update operations.
    Only authenticated users with staff or admin permissions can create or update packages.
    """
    queryset = models.MmsPackage.objects.all()  # Queryset for retrieving packages
    serializer_class = serializers.MmsPackageCreateUpdateSerializer  # Serializer used for package creation and update
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure the user is authenticated and has required permissions
    lookup_field = 'packageid'  # Use URL to identify the resource
    
    @extend_schema(
        description="Create or update a package. The 'packageid' is used to identify the package for updates.",
        responses={
            200: OpenApiResponse(
                description="Successfully created or updated the package.",
                examples={
                    "application/json": {
                        "example": {
                            "packageid": 1,
                            "packagename": "Luxury Cruise",
                            "base_price": "199.99",
                            "packagedetails": "A luxurious cruise with all-inclusive meals and entertainment."
                        }
                    }
                }
            ),
            400: OpenApiResponse(
                description="Invalid data provided.",
                examples={
                    "application/json": {
                        "example": {
                            "message": "Invalid input data."
                        }
                    }
                }
            ),
        },
        tags=["Package Management"]  # API group for package-related operations
    )
    def post(self, request, *args, **kwargs):
        return self.create(request=request, *args, **kwargs)
    
    @extend_schema(
        description="Update a package. The 'packageid' is used to identify the package to be updated.",
        responses={
            200: OpenApiResponse(
                description="Successfully updated the package.",
                examples={
                    "application/json": {
                        "example": {
                            "packageid": 1,
                            "packagename": "Luxury Cruise Updated",
                            "base_price": "249.99",
                            "packagedetails": "Updated details of the luxurious cruise package."
                        }
                    }
                }
            ),
            404: OpenApiResponse(
                description="Package not found for the given 'packageid'.",
                examples={
                    "application/json": {
                        "example": {
                            "message": "Package not found."
                        }
                    }
                }
            ),
        },
        tags=["Package Management"]  # API group for package-related operations
    )
    def put(self, request, *args, **kwargs):
        return self.update(request=request, *args, **kwargs)

class MmsPackageListView(generics.GenericAPIView, mixins.ListModelMixin):
    """
    API view to list all packages.
    Only authenticated users with staff or admin permissions can view the list of packages.
    """

    queryset = models.MmsPackage.objects.all()  # Queryset for retrieving packages
    serializer_class = serializers.MmsPackageListSerializer  # Serializer used for listing packages
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure the user is authenticated and has required permissions
    
    @extend_schema(
        description="List all available packages. The response includes details such as package name, price, and details.",
        responses={
            200: OpenApiResponse(
                description="Successfully retrieved the list of packages.",
                examples={
                    "application/json": {
                        "example": [
                            {
                                "packageid": 1,
                                "packagename": "Luxury Cruise",
                                "base_price": "199.99",
                                "packagedetails": "A luxurious cruise with all-inclusive meals and entertainment."
                            },
                            {
                                "packageid": 2,
                                "packagename": "Economy Cruise",
                                "base_price": "99.99",
                                "packagedetails": "A budget-friendly cruise option with basic amenities."
                            }
                        ]
                    }
                }
            ),
            404: OpenApiResponse(
                description="No packages found.",
                examples={
                    "application/json": {
                        "example": {
                            "message": "No packages found."
                        }
                    }
                }
            ),
        },
        tags=["Package Management"]  # API group for package-related operations
    )
    def list(self, request, *args, **kwargs):
        """
        Handle the GET request to retrieve the list of packages.
        This method retrieves all packages and applies filters if needed.
        """
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
    """
    API view to delete a specific package.
    The package is identified by its 'packageid' in the URL path.
    Only authenticated users with staff or admin permissions can delete packages.
    """
    
    queryset = models.MmsPackage.objects.all()  # Queryset for retrieving packages
    serializer_class = serializers.MmsPackageCreateUpdateSerializer  # Serializer used for deletion (may use a different serializer for response)
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure the user is authenticated and has required permissions
    lookup_field = 'packageid'  # Use URL to identify the resource
    
    @extend_schema(
        description="Delete a specific package identified by 'packageid'. Only admins or staff can delete packages.",
        responses={
            200: OpenApiResponse(
                description="Successfully deleted the package.",
                examples={
                    "application/json": {
                        "example": {
                            "message": "Package Luxury Cruise deleted successfully."
                        }
                    }
                }
            ),
            404: OpenApiResponse(
                description="Package not found for the given 'packageid'.",
                examples={
                    "application/json": {
                        "example": {
                            "message": "Package not found."
                        }
                    }
                }
            ),
        },
        tags=["Package Management"]  # API group for package-related operations
    )
    def delete(self, request, *args, **kwargs):
        """
        Handle the DELETE request to remove a specific package.
        This method first retrieves the package object and then deletes it.
        """
        instance = self.get_object()  # Retrieve the object to be deleted
        self.perform_destroy(instance)  # Perform the deletion (handled by DestroyModelMixin)
        return Response(
            {"message": f"Package {instance.packagename} deleted successfully."},
            status=status.HTTP_200_OK
        )
                 
class MmsTripAddView(generics.GenericAPIView, mixins.CreateModelMixin):
    """
    API view to create a new trip.
    Only authenticated users with admin or staff permissions can create trips.
    """
    serializer_class = serializers.MmsTripCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure staff or superuser permission is enforced
    
    @extend_schema(
        description="Create a new trip. The request body must contain details about the trip.",
        responses={
            201: OpenApiResponse(
                description="Successfully created the trip.",
                examples={
                    "application/json": {
                        "example": {
                            "tripid": 1,
                            "tripname": "Caribbean Adventure",
                            "startdate": "2024-06-01",
                            "enddate": "2024-06-15",
                            "tripcostperperson": "799.99",
                            "tripstatus": "upcoming",
                            "tripcapacity": 200,
                            "cancellationpolicy": "Full refund 30 days before trip",
                            "tripdescription": "An exciting trip to the Caribbean!",
                            "finalbookingdate": "2024-05-01",
                            "shipid": 1,
                            "stops": [1, 2],
                            "packages": [1, 2]
                        }
                    }
                }
            ),
            400: OpenApiResponse(
                description="Invalid data provided.",
                examples={
                    "application/json": {
                        "example": {
                            "message": "Invalid input data."
                        }
                    }
                }
            ),
        },
        tags=["Trip Management"]
    )
    def post(self, request, *args, **kwargs):
        """Handle trip creation."""
        return self.create(request=request, *args, **kwargs)

'''class MmsRoomSummaryListView(generics.ListAPIView): 
    """
    API view to retrieve a list of rooms grouped by room type and location.
    Supports filtering, searching, and ordering of room data.
    Only authenticated users with staff or admin permissions can access this list.
    """
    
    queryset = models.MmsRoom.objects.select_related('stateroomtypeid', 'locid').all()
    serializer_class = serializers.MmsRoomSummarySerializer  # Use the summary serializer here
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure the user is authenticated and has required permissions
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Enable filtering, searching
    filterset_class = filters.RoomFilter  # Apply custom filterset
    search_fields = ['roomnumber']  # Enable search by room number
    
    def get_queryset(self):
        """
        Group rooms by room type and location, and annotate with count and base price.
        """
        room_details = models.MmsRoom.objects.select_related('stateroomtypeid', 'locid')
        
        # Group by room type and location, and fetch base price from room type
        room_summary = room_details.values(
            'stateroomtypeid__stateroomtype',  # Group by room type
            'stateroomtypeid__baseprice',     # Fetch room type price
            'locid__location'                 # Group by location
        ).annotate(
            roomtypecount=Count('roomnumber'),  # Count of rooms for each room type
            locationcount=Count('roomnumber')  # Count of rooms for each location
        )
        
        return room_summary
    
    def list(self, request, *args, **kwargs):
        """
        Handle the GET request to list rooms grouped by room type and location.
        """
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({"detail": "No rooms found matching the filters."}, status=status.HTTP_404_NOT_FOUND)
        
        # Pass the queryset (which is a list of dictionaries) to the serializer
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
'''

class MmsRoomSummaryListView(generics.ListAPIView):
    """
    API view to retrieve a list of rooms for a particular trip, grouped by room type and location.
    Supports filtering, searching, and ordering of room data.
    Only authenticated users with staff or admin permissions can access this list.
    """
    
    serializer_class = serializers.MmsRoomSummarySerializer  # Use the summary serializer here
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Ensure the user is authenticated and has required permissions
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Enable filtering, searching
    filterset_class = filters.RoomSummaryFilter  # Apply custom filterset
    search_fields = ['roomnumber']  # Enable search by room number
    
    def get_queryset(self):
        """
        Group rooms by room type and location for a particular trip, and annotate with count.
        """
        trip_id = self.kwargs.get('tripid')  # Get the trip_id from URL parameters
        
        if not trip_id:
            return Response({"detail": "Trip ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        print(trip_id)
        # Query MmsTripRoom for the specified trip_id
        room_details = models.MmsTripRoom.objects.filter(tripid=trip_id).all()
        print(room_details)
        # Group by room type and location, and count the number of rooms for each group
        room_summary = room_details.values(
            'roomtype',  # Group by room type name
            'baseprice',  # Fetch room type price
            'location'    # Group by location name
        ).annotate(
            roomtypecount=Count('roomnumber'),  # Count of rooms for each room type
            locationcount=Count('roomnumber')  # Count of rooms for each location
        )
        
        return room_summary
    
    def list(self, request, *args, **kwargs):
        """
        Handle the GET request to list rooms for a specific trip, grouped by room type and location.
        """
        queryset = self.get_queryset()
       
        if not queryset.exists():
            return Response({"detail": "No rooms found for the specified trip."}, status=status.HTTP_404_NOT_FOUND)
        
        # Pass the queryset (which is a list of dictionaries) to the serializer
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class MmsTripRoomPriceUpdateView(generics.GenericAPIView):
    """
    View to handle price updates for rooms in MmsTripRoom.
    Supports updating prices based on room type or location.
    """
    queryset = models.MmsTripRoom.objects.all()
    serializer_class = serializers.MmsTripRoomPriceUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = "tripid"

    def put(self, request, *args, **kwargs):
        """
        Handle updating the dynamic price for rooms based on roomtype or location.
        """
        # Validate the incoming data using the serializer
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Extract the filters and dynamic price from validated data
        roomtype = serializer.validated_data.get('roomtype')
        location = serializer.validated_data.get('location')
        dynamicprice = serializer.validated_data.get('dynamicprice')

        # Fetch rooms based on the filters
        queryset = models.MmsTripRoom.objects.filter(tripid=kwargs['tripid'])

        if roomtype:
            queryset = queryset.filter(roomtype=roomtype)
        if location:
            queryset = queryset.filter(location=location)

        # Update the dynamic price for all matching rooms
        updated_count = queryset.update(dynamicprice=dynamicprice)

        if updated_count > 0:
            return Response({"detail": f"{updated_count} room(s) updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No rooms updated, please check your filters."}, status=status.HTTP_404_NOT_FOUND)
       
class MmsAdminTripListView(generics.ListAPIView):
    """
    API view to list all trips.
    Staff or admin can view all trips, while regular users can only view upcoming trips.
    """
    queryset = models.MmsTrip.objects.all()
    serializer_class = serializers.MmsAdminTripListSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.AdminTripFilter
    ordering_fields = ['startdate', 'enddate', 'tripcostperperson', 'duration', 'tripname']
    ordering = ['startdate']  # Default ordering (earliest trips first)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({"detail": "No trips found matching the specified filters."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MmsAdminTripDetailView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    """
    API view to retrieve details of a specific trip.
    Accessible to all users, regardless of permissions.
    """
    queryset = models.MmsTrip.objects.all()
    serializer_class = serializers.MmsTripDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'tripid'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class MmsTripDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    """
    API View to delete a trip from the system. 
    Uses DRF's DestroyModelMixin to perform deletion operations.
    """
    queryset = models.MmsTrip.objects.all()
    serializer_class = serializers.MmsTripCreateSerializer
    lookup_field = 'tripid'  # Field used to lookup the trip in the URL

    
    def get_object(self):
        """
        Get the trip instance based on the URL parameter.
        """
        tripid = self.kwargs['tripid']
        return models.MmsTrip.objects.get(tripid=tripid)
    
    @extend_schema(
        operation_id="delete_trip",
        summary="Delete a trip",
        description="Deletes a trip identified by its `tripid`. This action is irreversible. Ensure no dependent entities exist before deletion.",
        responses={
            204: OpenApiResponse(description="Trip deleted successfully."),
            400: OpenApiResponse(description="Invalid trip ID or request."),
            404: OpenApiResponse(description="Trip not found.")
        }
    )
    def delete(self, request, *args, **kwargs):
        """
        Delete a trip by its ID.
        Validates if the trip exists before performing deletion.
        """
        try:
            # Fetch the object
            trip = self.get_object()
        except models.MmsTrip.DoesNotExist:
            raise serializers.ValidationError({"detail": "Trip not found."}, code=status.HTTP_404_NOT_FOUND)

        # Perform deletion
        self.perform_destroy(trip)

        return Response({"detail": "Trip deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class MmsUserCreateView(generics.CreateAPIView):
    """
    User Registration View that handles the creation of a new user.
    - Validates input using UserRegistrationSerializer.
    - Creates a new user and returns the user data.
    """
        
    queryset = User.objects.all()
    serializer_class = serializers.MmsUserCreateSerializer
    permission_classes = [AllowAny]
    
    @extend_schema(
    description="User registration endpoint to create a new user account. The user provides their personal details, including password, which is hashed securely.",
    responses={
        201: OpenApiResponse(
            description="Successfully created a new user. A welcome email is sent to the provided email address.",
            examples={
                "application/json": {
                    "example": {
                        "id": 1,
                        "username": "john_doe",
                        "email": "john@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "profile": "http://example.com/profiles/john_doe/"
                    }
                }
            }
        ),
        400: OpenApiResponse(
            description="Bad Request. Validation error for the input data.",
            examples={
                "application/json": {
                    "example": {
                        "detail": "Passwords do not match."
                    }
                }
            }
        )
    },
    tags=["User Management"]
    )
    def perform_create(self, serializer):
        # Call the serializer's create method
        user = serializer.save()

        # Custom workflow: Send a welcome email
        send_mail(
            subject="Welcome to NICE",
            message="Thank you for registering with NICE!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=True,
        )

class MmsUserProfileCreateView(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = models.MmsUserProfile.objects.all()
    serializer_class = serializers.MmsUserProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Override perform_create to associate the authenticated user with the profile.
        """
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        POST method to create a user profile.
        """
        return self.create(request, *args, **kwargs)
    
class MmsUserUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = serializers.MmsUserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Retrieve the authenticated user instance.
        """
        return self.request.user

    def patch(self, request, *args, **kwargs):
        """
        Handle partial updates for the authenticated user.
        """
        return self.partial_update(request, *args, **kwargs)
        
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

class MmsLoginView(TokenObtainPairView):
    """
    Custom Token Obtain View to handle login and issue JWT tokens.
    Uses the CustomTokenObtainPairSerializer to validate and generate tokens.
    """
    serializer_class = serializers.MmsLoginSerializer
    
    @extend_schema(
        request=serializers.MmsLoginSerializer,
        responses={
            200: OpenApiResponse(
                description="Login successful. Returns JWT access and refresh tokens.",
                examples={"application/json": serializers.TokenObtainPairSerializer},
            ),
            400: OpenApiResponse(description="Invalid credentials provided."),
        }
    )
    def post(self, request, *args, **kwargs):
        """Handle user login and issue JWT tokens."""
        return super().post(request, *args, **kwargs)
    
class MmsLogoutView(APIView):
    """
    Logs the user out by blacklisting their refresh token. 
    This effectively invalidates the session and makes the refresh token unusable.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,  # No body examples needed for this request
        responses={
            205: OpenApiResponse(description="Successfully logged out. Refresh token blacklisted."),
            400: OpenApiResponse(description="Invalid request. Refresh token required or error occurred."),
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_examples)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class MmsCustomPasswordResetView(auth_views.PasswordResetView):
    """
    Custom view for password reset requests. 
    This view handles the process of requesting a password reset by sending an email to the user with a reset link.
    """
    email_template_name = 'registration/password_reset_email.html'
    template_name = 'registration/password_reset_form.html'

    @extend_schema(
        request=serializers.MmsPasswordResetRequestSerializer,
        responses={
            200: OpenApiResponse(description="Password reset email sent successfully."),
            400: OpenApiResponse(description="Email address not found or error occurred."),
        }
    )
    def post(self, request, *args, **kwargs):
        """Handle password reset request and send email."""
        return super().post(request, *args, **kwargs)

class MmsCustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """
    Custom view for confirming the password reset. 
    This view allows the user to set a new password after clicking the reset link sent to their email.
    """
    template_name = 'registration/password_reset_confirm.html'

    @extend_schema(
        request=serializers.MmsPasswordResetRequestSerializer,
        responses={
            200: OpenApiResponse(description="Password has been reset successfully."),
            400: OpenApiResponse(description="Invalid reset token or passwords do not match."),
        }
    )
    def post(self, request, *args, **kwargs):
        """Handle the reset of the user's password."""
        return super().post(request, *args, **kwargs)

class MmsTripListView(generics.ListAPIView):
    """
    API view to list all trips.
    Staff or admin can view all trips, while regular users can only view upcoming trips.
    """
    queryset = models.MmsTrip.objects.all()
    serializer_class = serializers.MmsTripListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.TripFilter
    ordering_fields = ['startdate', 'enddate', 'tripcostperperson', 'duration', 'tripname']
    ordering = ['startdate']  # Default ordering (earliest trips first)

    @extend_schema(
        description="Retrieve a list of trips. Admins/staff can view all trips; regular users only view upcoming trips.",
        responses={
            200: OpenApiResponse(
                description="Successfully retrieved the list of trips.",
                examples={
                    "application/json": {
                        "example": [
                            {
                                "tripid": 1,
                                "tripname": "Caribbean Adventure",
                                "startdate": "2024-06-01",
                                "enddate": "2024-06-15",
                                "tripcostperperson": "799.99",
                                "tripstatus": "upcoming",
                                "tripcapacity": 200,
                                "cancellationpolicy": "Full refund 30 days before trip",
                                "tripdescription": "An exciting trip to the Caribbean!",
                                "finalbookingdate": "2024-05-01",
                                "shipid": 1,
                                "stops": [1, 2],
                                "packages": [1, 2]
                            }
                        ]
                    }
                }
            ),
            404: OpenApiResponse(
                description="No trips found matching the filters.",
                examples={
                    "application/json": {
                        "example": {
                            "message": "No trips found matching the specified filters."
                        }
                    }
                }
            ),
        },
        tags=["Trip Management"]
    )
    def get_queryset(self):
        """
        Customize the queryset to return all trips for staff/admin users,
        or only upcoming trips for regular users.
        """
        user = self.request.user
        base_queryset = models.MmsTrip.objects.prefetch_related('portstops__portid')  # Optimize port stop queries
        if user.is_staff or user.is_superuser:
            return base_queryset
        return base_queryset.filter(tripstatus__iexact='upcoming')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({"detail": "No trips found matching the specified filters."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class MmsTripDetailView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    """
    API view to retrieve details of a specific trip.
    Accessible to all users, regardless of permissions.
    """
    queryset = models.MmsTrip.objects.all()
    serializer_class = serializers.MmsTripDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'tripid'

    @extend_schema(
        description="Retrieve details of a specific trip by 'tripid'.",
        responses={
            200: OpenApiResponse(
                description="Successfully retrieved trip details.",
                examples={
                    "application/json": {
                        "example": {
                            "tripid": 1,
                            "tripname": "Caribbean Adventure",
                            "startdate": "2024-06-01",
                            "enddate": "2024-06-15",
                            "tripcostperperson": "799.99",
                            "tripstatus": "upcoming",
                            "tripcapacity": 200,
                            "cancellationpolicy": "Full refund 30 days before trip",
                            "tripdescription": "An exciting trip to the Caribbean!",
                            "finalbookingdate": "2024-05-01",
                            "shipid": 1,
                            "stops": [1, 2],
                            "packages": [1, 2]
                        }
                    }
                }
            ),
            404: OpenApiResponse(
                description="Trip not found.",
                examples={
                    "application/json": {
                        "example": {
                            "message": "Trip not found."
                        }
                    }
                }
            ),
        },
        tags=["Trip Management"]
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

@extend_schema(
        description="Retrieve trip details along with available rooms, room categories, and packages for booking.",
        responses={
            200: OpenApiResponse(
                description="Successfully retrieved trip booking details.",
                examples={
                    "application/json": {
                        "trip_details": {
                            "tripid": 1,
                            "tripname": "Caribbean Adventure",
                            "startdate": "2024-06-01",
                            "enddate": "2024-06-15",
                            "tripcostperperson": "799.99",
                            "tripcapacityremaining": 150
                        },
                        "available_rooms": [
                            {
                                "roomnumber": "A101",
                                "isbooked": False,
                                "dynamicprice": "100.00",
                                "roomtype": "Deluxe",
                                "location": "Deck 1"
                            },
                            {
                                "roomnumber": "A102",
                                "isbooked": False,
                                "dynamicprice": "120.00",
                                "roomtype": "Suite",
                                "location": "Deck 1"
                            }
                        ],
                        "available_room_categories": ["Deluxe", "Suite"],
                        "available_packages": [
                            {
                                "packageid": 1,
                                "tripid": 1,
                                "package_details": {
                                    "package_name": "Luxury Package",
                                    "price": "499.99",
                                    "description": "Includes premium meals and excursions."
                                }
                            }
                        ]
                    }
                }
            ),
            404: OpenApiResponse(
                description="Trip not found for the given trip ID.",
                examples={
                    "application/json": {
                        "detail": "Trip with the given ID does not exist."
                    }
                }
            ),
        },
        tags=["Booking Management"]
    )
class MmsStartBookingView(generics.RetrieveAPIView):
    queryset = models.MmsTrip.objects.all()
    serializer_class = serializers.MmsStartBookingSerializer
    permission_classes = [IsAuthenticated]

    def get_trip(self, tripid):
        """
        Helper method to retrieve the trip based on the tripid.
        """
        try:
            trip = models.MmsTrip.objects.get(tripid=tripid)
            return trip
        except models.MmsTrip.DoesNotExist:
            raise serializers.ValidationError("Trip not found.")
    

    def get(self, request, *args, **kwargs):
        """
        Override GET to ensure context is correctly passed.
        """
        tripid = self.kwargs.get('tripid')  # Get the tripid from the URL
        trip = self.get_trip(tripid)  # Retrieve the trip object
        serializer = self.get_serializer(instance=trip)
        trip_data = serializer.data
    
        # Store relevant data from serializer directly into session
        request.session['trip_details'] = {
            'trip_id': trip_data['trip_details']['tripid'],
            'trip_capacity_remaining': trip_data['trip_details']['tripcapacityremaining'],
            'trip_cost_per_person': float(trip_data['trip_details']['tripcostperperson']),  # Convert to float for math operations
            'available_room_categories': [
            {  # Parse available room categories into structured objects
                'room_type': room['stateroomtype'],
                'room_size': float(room['roomsize']),
                'number_of_beds': float(room['numberofbeds']),
                'number_of_baths': float(room['numberofbaths']),
                'number_of_balconies': float(room['numberofbalconies']),
                'room_type_description': room['roomtypedescription']
            }
            for room in trip_data['available_room_categories']
            ],  # Ensure it's a proper list
            'available_packages': [
                {  # Parse available packages into structured objects
                    'package_id': pkg['packageid'],
                    'name': pkg['package_details']['package_name'],
                    'price': float(pkg['package_details']['price']),
                    'description': pkg['package_details']['description'],
                }
                for pkg in trip_data['available_packages']
            ],
        }
        return Response(serializer.data)
        
class MmsTemporaryCapacityReservationView(generics.GenericAPIView):
    """
    API view to temporarily reserve capacity for a trip.
    This ensures that no other users can book the same capacity while the user is in the process of selecting rooms.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.MmsTemporaryCapacityReservationSerializer

    def get_trip(self, tripid):
        """
        Helper method to retrieve the trip based on the tripid.
        """
        try:
            trip = models.MmsTrip.objects.get(tripid=tripid)
            return trip
        except models.MmsTrip.DoesNotExist:
            raise serializers.ValidationError("Trip not found.")

    def patch(self, request, *args, **kwargs):
        """
        Handle PATCH request to temporarily reserve capacity for a trip.
        This method will reduce the trip's remaining capacity based on the user's room and people selection.
        """
        tripid = self.kwargs.get('tripid')  # Get the tripid from the URL
        trip = self.get_trip(tripid)  # Retrieve the trip object
        serializer = self.get_serializer(data=request.data, context={'trip': trip})

        # Validate the input data and reduce trip capacity if validation passes
        if serializer.is_valid():
            rooms = serializer.validated_data['rooms']
            
            # Store room details in the session
            request.session['booking_details'] = {
                'rooms': rooms,  # List of rooms with their room numbers and number of people
                'number_of_passengers': sum(room['number_of_people'] for room in rooms),  # Total number of people
                'room_details': [
                    {'room_number': room['room_number'], 'number_of_people': room['number_of_people']}
                    for room in rooms
                ],  # Storing detailed room info
            }

            # Reduce the trip capacity by temporarily marking it
            trip = serializer.reduce_trip_capacity(trip, rooms)

            # Return the updated trip details
            return Response({
                "message": "Capacity temporarily reserved.",
                "trip_capacity_remaining": trip.tripcapacityremaining,
                "temporary_reserved": trip.tempcapacityreserved,
                "reservation_timestamp": trip.tempreservationtimestamp
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MmsRoomCategorySelectionView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.MmsRoomCategorySelectionSerializer
    
    def get_trip(self, tripid):
        """
        Helper method to retrieve the trip based on the tripid.
        """
        try:
            trip = models.MmsTrip.objects.get(tripid=tripid)
            return trip
        except models.MmsTrip.DoesNotExist:
            raise serializers.ValidationError("Trip not found.")

    def patch(self, request, *args, **kwargs):
        
        tripid = self.kwargs.get('tripid')  # Get the tripid from the URL
        trip = self.get_trip(tripid)  # Retrieve the trip object
        serializer = self.get_serializer(data=request.data, context={'trip': trip})
        
        
        room_selections = request.data.get('room_selections')  # Expecting a list of {room_type, number_of_rooms}
        user_id = request.user.id  # Assuming the user is authenticated

        try:
            trip = models.MmsTrip.objects.get(tripid=tripid)
        except models.MmsTrip.DoesNotExist:
            return Response({"error": "Trip not found."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize and validate the input data
        serializer = serializers.MmsRoomCategorySelectionSerializer(
            data=request.data,
            context={'trip': trip, 'user_id': user_id}
        )

        if serializer.is_valid():
            # Reserve rooms temporarily
            reserved_rooms = serializer.reserve_rooms(trip, room_selections, user_id)
            
            # Store the room selection details in the session
            request.session['room_selection_details'] = {
                'room_selections': [
                    {
                        'room_type': room['room_type'],
                        'number_of_rooms': room['number_of_rooms'],
                    }
                    for room in room_selections
                ],
                'reserved_rooms': [
                    {
                        'room_number': reserved_room['roomnumber'],
                        'dynamic_price': float(reserved_room['dynamicprice']),
                        'location': reserved_room['location'],
                        'room_type': reserved_room['roomtype'],
                    }
                    for reserved_room in reserved_rooms
                ],
            }
            
            return Response({
                "message": "Rooms temporarily reserved successfully.",
                "reserved_rooms": reserved_rooms  # Return details of the reserved rooms
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MmsAddPassengerView(APIView):
    """
    View to add a passenger's information to the session.
    This does not store data in the database until booking confirmation.
    """
    
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST request to add passenger details to session.
        """
        #print(request.session.items())
        try:
            num_passengers = request.session.get('booking_details', {}).get('number_of_passengers')
            if num_passengers is None:
                raise KeyError("number_of_passengers key is missing in session.")
        except (KeyError, TypeError) as e:
            # Handle session expiration or missing key gracefully
            num_passengers = 0  # Set default value, or you can redirect to an error page or show a message
            # Optionally, log the error or notify the user
            print(f"Error retrieving number_of_passengers from session: {str(e)}")
        
        if num_passengers == 0:
            return Response({"error": "No passengers added yet."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a list if it doesn't exist in the session
        if 'passengers' not in request.session:
            request.session['passengers'] = []

        # Validate the passenger data
        serializer = serializers.MmsPassengerGetSerializer(data=request.data, context={'num_passengers': num_passengers})
        if serializer.is_valid():
            # Add the passenger to the session
            passenger_data = serializer.validated_data
            passenger_data = passenger_data['passengers']  # Access the list of passengers

            request.session['passengers'] = [
                {
                    'first_name': passenger['firstname'],
                    'last_name': passenger['lastname'],
                    'date_of_birth': passenger['dateofbirth'].isoformat(),  # Convert date to ISO format string
                    'gender': passenger['gender'],
                    'contact_number': passenger['contactnumber'],
                    'email_address': passenger['emailaddress'],
                    'address': {
                        'street': passenger['streetaddr'],
                        'city': passenger['city'],
                        'state': passenger['state'],
                        'country': passenger['country'],
                        'zip_code': passenger['zipcode'],
                    },
                    'nationality': passenger['nationality'],
                    'passport_number': passenger['passportnumber'],
                    'emergency_contact': {
                        'name': passenger['emergencycontactname'],
                        'number': passenger['emergencycontactnumber'],
                    },
                }
                for passenger in passenger_data
            ]
            request.session.modified = True  # Ensure the session is updated
            
            # Update the number of passengers added
            #request.session['num_passengers'] += 1

            return Response({"message": "Passenger added to session.", "passenger_data": passenger_data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MmsTripPackageListView(generics.GenericAPIView, mixins.ListModelMixin):
    """
    API view to list all packages for a specific trip.
    Only authenticated users with staff or admin permissions can view the list of packages.
    """

    queryset = models.MmsTripPackage.objects.all()  # Queryset for retrieving packages
    serializer_class = serializers.MmsTripPackageListSerializer  # Serializer used for listing packages
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated and has required permissions
    
    def get_queryset(self):
        """
        Override to filter packages by tripid passed in the URL.
        """
        tripid = self.kwargs.get('tripid')  # Access tripid from URL kwargs
        return models.MmsTripPackage.objects.filter(tripid=tripid)  # Filter packages for the specific trip

    @extend_schema(
        description="List all available packages. The response includes details such as package name, price.",
        responses={
            200: OpenApiResponse(
                description="Successfully retrieved the list of packages.",
                examples={
                    "application/json": {
                        "example": [
                            {
                                "packageid": 1,
                                "packagename": "Water Package",
                                "base_price": "199.99"
                            },
                            {
                                "packageid": 2,
                                "packagename": "Economy Cruise",
                                "base_price": "99.99"
                            }
                        ]
                    }
                }
            ),
            404: OpenApiResponse(
                description="No packages found for the specified trip.",
                examples={
                    "application/json": {
                        "example": {
                            "message": "No packages found."
                        }
                    }
                }
            ),
        },
        tags=["Booking Management"]  # API group for package-related operations
    )
    def get(self, request, *args, **kwargs):
        return self.list(request=request, *args, **kwargs)
    
class MmsAddPackageView(APIView):
    """
    View to add a passenger's information to the session.
    This does not store data in the database until booking confirmation.
    """
    
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST request to add package details to session.
        """
        #print(request.session.items())
        try:
            num_passengers = request.session.get('booking_details', {}).get('number_of_passengers')
            if num_passengers is None:
                raise KeyError("number_of_passengers key is missing in session.")
        except (KeyError, TypeError) as e:
            # Handle session expiration or missing key gracefully
            num_passengers = 0  # Set default value, or you can redirect to an error page or show a message
            print(f"Error retrieving number_of_passengers from session: {str(e)}")
        
        if num_passengers == 0:
            return Response({"error": "No passengers added yet."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a list if it doesn't exist in the session
        if not 'packages' in request.session:
            request.session['packages'] = []
        

        # Validate the package data
        serializer = serializers.MmsTripPackageAddSerializer(data=request.data, context={'num_passengers': num_passengers})
        if serializer.is_valid():
            # Add the validated package data to the session
            package_data = serializer.validated_data
            print(package_data)
            request.session['packages'] = [{
                'package_id': package['packageid'],
                'package_name': package['packagename'],
                'quantity': package['quantity'],
            } for package in package_data['packages']]
            request.session.modified = True  # Ensure the session is updated
            print(request.session.get('packages'))
            return Response({"message": "Package added to session.", "package_data": package_data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MmsBookingSummaryView(APIView):
    """
    View to handle booking confirmation.
    Retrieves selected details and calculates the total price.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handle GET request to display booking summary.
        """
        tripid_from_url = kwargs.get('tripid')
        # Retrieve details from session
        trip_details = request.session.get('trip_details', {})
        booking_details = request.session.get('booking_details', {})
        room_selection_details = request.session.get('room_selection_details', {})
        passengers = request.session.get('passengers', [])
        package_selections = request.session.get('packages', [])

        
        # Validate session data existence
        if not trip_details or not booking_details or not room_selection_details or not passengers:
            return Response({"error": "Missing essential booking details."}, status=status.HTTP_400_BAD_REQUEST)

        tripid_from_session = trip_details.get('trip_id')
        
        if (tripid_from_url) != (tripid_from_session):
            return Response({"error": "Trip ID mismatch between session and URL."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve room selections and reserved rooms
        room_selections = room_selection_details.get('room_selections', [])
        reserved_rooms = room_selection_details.get('reserved_rooms', [])

        # Number of passengers
        num_passengers = booking_details.get('number_of_passengers', 0)

        if num_passengers == 0:
            return Response({"error": "No passengers added yet."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate the total price
        total_price = self.calculate_total_price(room_selections, reserved_rooms, package_selections, trip_details, num_passengers, passengers)

        # Store the total price in session for use in payment API
        request.session['total_price'] = str(total_price)
        
        # Prepare the booking summary response
        summary = {
            "trip_details": trip_details,
            "passenger_details": passengers,
            "room_selections": room_selections,
            "reserved_rooms": reserved_rooms,
            "package_selections": package_selections,
            "total_price": float(total_price),  # Convert to float for JSON serialization
        }

        return Response(summary, status=status.HTTP_200_OK)

    def calculate_total_price(self, room_selections, reserved_rooms, package_selections, trip_details, num_passengers, passengers):
        """
        Calculate the total price based on room selections, package selections, and trip details.
        """
        total_room_price = Decimal('0.00')
        total_package_price = Decimal('0.00')

        # Current date
        current_date = datetime.now()

        # Calculate chargeable passengers based on age (greater than 5 years)
        def calculate_age(dob):
            dob_date = datetime.strptime(dob, "%Y-%m-%d")
            return current_date.year - dob_date.year - ((current_date.month, current_date.day) < (dob_date.month, dob_date.day))

        #print(passengers)
        # Filter passengers older than 5 years
        chargeable_passengers = [
            p for p in passengers if calculate_age(p["date_of_birth"]) > 5
        ]
        num_chargeable_passengers = len(chargeable_passengers)

        # Get cost per person from trip details
        cost_per_person = Decimal(trip_details.get("trip_cost_per_person", 0))

        # Calculate total room price
        for room in room_selections:
            room_type = room.get('room_type')
            num_rooms = room.get('number_of_rooms', 1)
            matching_room = next((r for r in reserved_rooms if r['room_type'] == room_type), None)
            if matching_room:
                room_price = Decimal(matching_room.get('dynamic_price', 0))
                total_room_price += room_price * num_rooms

        # Reduce room price proportionally for passengers aged 5 and below
        total_passengers = len(passengers)
        if total_passengers > 0:
            total_room_price *= Decimal(num_chargeable_passengers) / Decimal(total_passengers)

        # Calculate total package price
        available_packages = trip_details.get('available_packages', [])
        for package in package_selections:
            package_name = package.get('package_name')
            quantity = package.get('quantity', 1)
            package_details = next((pkg for pkg in available_packages if pkg['name'] == package_name), None)
            if package_details:
                package_price = Decimal(package_details['price'])
                total_package_price += package_price * quantity

        # Total cost: room price + package price + per person cost for chargeable passengers
        total_price = total_room_price + total_package_price + (cost_per_person * num_chargeable_passengers)

        return total_price

class MmsPaymentDetailView(APIView):
    """
    Retrieve payment details (such as amount) for a user from session data.
    """
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request, *args, **kwargs):
        """
        Get the payment information (retrieved from session storage).
        """
        # Retrieve payment details from session storage
        payment_details = request.session.get('total_price', None)

        if not payment_details:
            return Response({'error': 'Payment details not found in session'}, status=400)

        return Response(payment_details)  # Return the payment data stored in session
    
class MmsPaymentStatusView(APIView):
    """
    Simulate and return payment status dynamically with basic validation for payment details.
    """

    def post(self, request, *args, **kwargs):
        """
        Process payment details and validate the input.
        """
        payment_data = request.data

        # Extract payment details from the request
        first_name = payment_data.get('first_name', '').strip()
        last_name = payment_data.get('last_name', '').strip()
        email = payment_data.get('email', '').strip()
        phone = payment_data.get('phone', '').strip()
        card_number = payment_data.get('card_number', '').strip()
        card_cvv = payment_data.get('card_cvv', '').strip()
        card_expiry = payment_data.get('card_expiry', '').strip()
        
        amount = request.session.get('total_price', None)
        # Basic validation
        errors = {}
        if not first_name:
            errors['first_name'] = "First name is required."
        if not last_name:
            errors['last_name'] = "Last name is required."
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors['email'] = "A valid email address is required."
        if not phone or not re.fullmatch(r'\+?[1-9]\d{1,14}', phone):
            errors['phone'] = "A valid phone number with at least 10 digits is required."
        if not card_number or not card_number.isdigit() or len(card_number) not in [13, 16, 19]:
            errors['card_number'] = "A valid card number with 13, 16, or 19 digits is required."
        if not card_cvv or not card_cvv.isdigit() or len(card_cvv) not in [3, 4]:
            errors['card_cvv'] = "A valid CVV with 3 or 4 digits is required."
        if not card_expiry or not re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", card_expiry):
            errors['card_expiry'] = "A valid card expiry date in MM/YY format is required."

        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        card_number = '*' * (len(card_number) - 4) + card_number[-4:]
        # Simulate payment success/failure logic
        is_success = random.choice([True])  # Simulates payment success/failure
        if is_success:
            request.session['payment_details'] = {
                "transaction_id": f"{uuid.uuid4()}",
                "payment_time": int(now().timestamp()),
                "payment_amount": amount,  # Use the amount sent from frontend
                "payment_method": card_number,  # Example payment method,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone   
            }
            payment_details = { 
                "status": "succeeded"  
            }
            return Response(payment_details, status=status.HTTP_200_OK)
        else:
            return Response(
                {"status": "failed", "reason": "Payment processing failed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
class MmsPaymentSucceededView(APIView):
    """
    View to handle booking creation after a successful payment.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to create a booking after payment succeeds.
        """
        
        # Extract session data
        session_data = request.session
        
        # Extract necessary session details
        trip_id = session_data.get('trip_details', {}).get('trip_id')
        package_selection = session_data.get('packages', [])
        reserved_rooms = session_data.get('room_selection_details', {}).get('reserved_rooms', [])
        passengers_data = session_data.get('passengers', [])
        number_of_passengers = session_data.get('booking_details', {}).get('number_of_passengers')
        total_price = session_data.get('total_price')
        payment_details = session_data.get('payment_details', {})
        
        print(trip_id, package_selection, reserved_rooms, passengers_data, number_of_passengers, total_price, payment_details)

        # Check if all required session data is present
        if not all([trip_id, package_selection, reserved_rooms, passengers_data, total_price, payment_details]):
            return Response({"error": "Missing session data for booking."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a dictionary with the extracted session data
        booking_data = {
            'trip_id': trip_id,
            'package_selection': package_selection,
            'reserved_rooms': reserved_rooms,
            'passengers_data': passengers_data,
            'number_of_passengers': number_of_passengers,
            'total_price': total_price,
            'payment_details': payment_details
        }

        # Pass session data as actual input data (not context)
        serializer = serializers.MmsBookingConfirmSerializer(data=booking_data, context={'request': request})

        if serializer.is_valid():
          
            # The serializer handles the creation and transaction inside the create method
            booking = serializer.save()  # This triggers the create() method in the serializer

            request.session.pop('trip_details', None)
            request.session.pop('packages', None)
            request.session.pop('room_selection_details', None)
            request.session.pop('passengers', None)
            request.session.pop('booking_details', None)
            request.session.pop('total_price', None)
            request.session.pop('payment_details', None)
            self.send_confirmation_email(booking, request)

            # Return a successful response with the booking details
            return Response({
                "message": "Booking created successfully",
                "booking_id": booking.bookingid
            }, status=status.HTTP_201_CREATED)
            

        # If validation fails, return an error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_confirmation_email(self, booking, request):
            """
            Send an email with booking and invoice details.
            """
            # Prepare email details
            customer_email =  booking.userid.email  # Assuming the first passenger is the primary contact
            subject = f"Booking Confirmation - {booking.bookingid}"
            
            # Generate the email body from a template
            context = {
                'bookingid': booking.bookingid,
                'tripname': booking.tripid.tripname,
                'tripdestination': booking.tripid.portstops.filter(isendport=True).values_list('portid__portname', flat=True).first(),
                'tripstartdate': booking.tripid.startdate,
                'tripenddate': booking.tripid.enddate,
                'passengers': booking.groupid.mmspassenger_set.all(),
                'rooms': booking.mmstriproom_set.all(),
                'packages': booking.mmsbookingpackage_set.all(),
                'total_price': booking.mmsinvoice_set.first().totalamount,
                'invoiceid': booking.mmsinvoice_set.first().invoiceid,
                'payment_details': booking.mmsinvoice_set.first().mmspaymentdetail_set.all()                                                            # Assuming total price is stored
            }
            
            # Use a template to render the email body
            message = render_to_string('email/booking_confirmation.html', context)

            # Send the email (using SMTP configured in settings)
            send_mail(
                subject,
            '',  # Empty plain text body since we are using HTML
            settings.EMAIL_HOST_USER,  # From email address
            [customer_email],  # Recipient email address
            fail_silently=False,
            html_message=message 
            )
# class MmsUserBookingsListView(generics.ListAPIView):
#     """
#     View to list all bookings for the authenticated user.
#     """

#     permission_classes = [IsAuthenticated]
#     serializer_class = serializers.MmsUserBookingListSerializer

#     def get_queryset(self):
#         """
#         Filter bookings to only include those belonging to the authenticated user.
#         """
#         user = self.request.user
#         bookings = models.MmsBooking.objects.filter(userid=user).select_related('tripid')
#         print(bookings)
#         return bookings
    
class MmsUserBookingsListView(APIView):
    """
    View to list all bookings for the authenticated user, grouped by status.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests and return grouped bookings.
        """
        user = request.user
        bookings = models.MmsBooking.objects.filter(userid=user).select_related('tripid')
        serializer = serializers.MmsUserBookingListSerializer()
        grouped_data = serializer.to_representation(bookings)
        return Response(grouped_data)
    
class MmsUserBookingDetailView(generics.RetrieveAPIView):
    """
    View to retrieve detailed information for a specific booking.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.MmsBookingDetailSerializer
    lookup_field = 'bookingid'

    def get_queryset(self):
        """
        Ensure only bookings belonging to the authenticated user and matching the bookingid are returned.
        """
        user = self.request.user
        bookingid = self.kwargs['bookingid']  # Get the bookingid from the URL
        return models.MmsBooking.objects.filter(userid=user, bookingid=bookingid)
    