from . import views
from django.urls import path
from rest_framework_simplejwt.views import  TokenRefreshView

"""
    **Endpoint:**
    - `POST /register/`

    **Description:**
    Handles user registration. Accepts user details and creates a new user in the system.

    **Request Body:**
    - `username`, `email`, `password`, `confirm_password`, `first_name`, `last_name`.

    **Response:**
    - `201 Created`: User registered successfully.
    - `400 Bad Request`: Validation errors (e.g., username already exists).
    
    **Endpoint:**
    - `POST /login/`

    **Description:**
    Authenticates a user and issues JWT tokens (access and refresh).

    **Request Body:**
    - `username` (str): The username of the user.
    - `password` (str): The password of the user.

    **Response:**
    - `200 OK`: Returns access/refresh tokens and user details.
    - `401 Unauthorized`: Invalid username or password.
    
    **Endpoint:**
    - `POST /refresh/`

    **Description:**
    Refreshes the access token using the provided refresh token.

    **Request Body:**
    - `refresh` (str): The refresh token.

    **Response:**
    - `200 OK`: Returns a new access token.
    - `401 Unauthorized`: Invalid or expired refresh token.
    """

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user_register'),
    path('login/', views.LoginView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name = 'token_blacklist'),
    path('trips/',views.MmsTripListView.as_view(),name = 'trip_list_view'),
    path('trips/<int:pk>/', views.MmsTripDetailView.as_view(), name='trip-detail'),
    path('add-port/', views.MmsPortCreateUpdateView.as_view(), name='add-port'),
    path('add-port/<int:pk>/', views.MmsPortCreateUpdateView.as_view(), name='add-port'),
    path('add-restaurant/', views.MmsRestaurantCreateUpdateView.as_view(), name='add-restuarant'),
    path('add-restaurant/<int:pk>/', views.MmsRestaurantCreateUpdateView.as_view(), name='update-restuarant'),
    path('add-activity/', views.MmsActivityCreateUpdateView.as_view(), name='add-activity'),
    path('add-activity/<int:pk>/', views.MmsActivityCreateUpdateView.as_view(), name='update-activity'),
]
