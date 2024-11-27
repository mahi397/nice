from . import models
from django.db import transaction
from . import filters, serializers
from django.core.mail import send_mail
from . permissions import IsAdminOrStaff
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import mixins, generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated

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

class MmsTripListView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = models.MmsTrip.objects.prefetch_related('portstops')
    serializer_class = serializers.MmsTripListSerializer
    permission_classes = [AllowAny]
    filter_class = filters.CruiseFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return models.MmsTrip.objects.all()
        return models.MmsTrip.objects.filter(tripstatus__iexact='upcoming')

    def get(self, request, *args, **kwargs):
        # Apply filters dynamically
        filtered_queryset = self.filter_queryset(self.get_queryset())
        # Serialize data
        return self.list(request, *args, **kwargs)
    
class MmsTripDetailView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    queryset = models.MmsTrip.objects.all()
    serializer_class = serializers.MmsTripDetailSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class MmsPortCreateUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = models.MmsPort.objects.all()
    serializer_class = serializers.MmsPortCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'portid'  # Use URL to identify the resource
    
    def update(self, request, *args, **kwargs):
        # Extract `portid` from URL
        portid = kwargs.get('portid')

        # Validate the `portid` in the request body (if provided)
        if 'portid' in request.data and str(request.data['portid']) != str(portid):
            return Response(
                {"detail": "Port ID in the request body does not match the URL."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Call the parent class update method
        return super().update(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request=request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request=request, *args, **kwargs)
    
class MmsRestaurantCreateUpdateView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = models.MmsRestaurant.objects.all()
    serializer_class = serializers.MmsRestaurantCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'restaurantid'  # Use URL to identify the resource
    
    def update(self, request, *args, **kwargs):
        # Extract `portid` from URL
        restaurantid = kwargs.get('restaurantid')

        # Validate the `portid` in the request body (if provided)
        if 'restaurantid' in request.data and str(request.data['restaurantid']) != str(restaurantid):
            return Response(
                {"detail": "Restaurant ID in the request body does not match the URL."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Call the parent class update method
        return super().update(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request=request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request=request, *args, **kwargs)
    
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
    
    def put(self, request, *args, **kwargs):
        return self.update(request=request, *args, **kwargs)
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