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
    path('register/', views.UserCreateView.as_view(), name='user-register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', views.LogoutView.as_view(), name = 'logout'),
    path('user/<int:id>/update/', views.UserUpdateView.as_view(), name='user-update'),
    path('user/delete/', views.UserDeleteView.as_view(), name='self-delete-user'),
    path('trips/',views.MmsTripListView.as_view(),name = 'trip-list-view'),
    path('trips/<int:pk>/', views.MmsTripDetailView.as_view(), name='trip-detail'),
    path('port/add/', views.MmsPortCreateUpdateView.as_view(), name='add-port'),
    path('port/<int:portid>/update/', views.MmsPortCreateUpdateView.as_view(), name='update-port'),
    path('restaurant/add/', views.MmsRestaurantCreateUpdateView.as_view(), name='add-restuarant'),
    path('restaurant/<int:restaurantid>/update/', views.MmsRestaurantCreateUpdateView.as_view(), name='update-restuarant'),
    path('activity/add/', views.MmsActivityCreateUpdateView.as_view(), name='add-activity'),
    path('activity/<int:activityid>/update/', views.MmsActivityCreateUpdateView.as_view(), name='update-activity'),
    path('trip/add/', views.MmsTripCreateUpdateView.as_view(), name='add-trips'),
    path('trip/<int:tripid>/update/', views.MmsTripCreateUpdateView.as_view(), name='update-trips'),
    path('port-stop/add/', views.MmsPortStopCreateUpdateView.as_view(), name='add-port-stops'),
    path('port-stop/<int:itineraryid>/update/', views.MmsPortStopCreateUpdateView.as_view(), name='update-port-stops'),
    
]
