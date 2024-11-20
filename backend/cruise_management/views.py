from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

class UserRegistrationView(generics.CreateAPIView):
    """
    User Registration View that handles the creation of a new user.
    - Validates input using UserRegistrationSerializer.
    - Creates a new user and returns the user data.
    """
        
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom Token Obtain View to handle login and issue JWT tokens.
    Uses the CustomTokenObtainPairSerializer to validate and generate tokens.
    """
    serializer_class = CustomTokenObtainPairSerializer
    