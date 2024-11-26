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
    path('port/add', views.MmsPortCreateUpdateView.as_view(), name='add-port'),
    path('port/<int:pk>/update/', views.MmsPortCreateUpdateView.as_view(), name='update-port'),
    path('restaurant/add/', views.MmsRestaurantCreateUpdateView.as_view(), name='add-restuarant'),
    path('restaurant/<int:pk>/update/', views.MmsRestaurantCreateUpdateView.as_view(), name='update-restuarant'),
    path('activity/add/', views.MmsActivityCreateUpdateView.as_view(), name='add-activity'),
    path('activity/<int:pk>/update/', views.MmsActivityCreateUpdateView.as_view(), name='update-activity'),
    path('trip/add/', views.MmsTripAddUpdateView.as_view(), name='add-trips'),
    path('trip/<int:tripid>/update/', views.MmsTripAddUpdateView.as_view(), name='update-trips'),
]
