from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
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
    path('ports/list', views.MmsPortListView.as_view(), name='list-ports'),
    path('ports/add', views.MmsPortCreateUpdateView.as_view(), name='add-port'),
    path('ports/<int:portid>/update', views.MmsPortCreateUpdateView.as_view(), name='update-port'),
    path('ports/<int:portid>/delete', views.MmsPortDeleteView.as_view(), name='del-port'),
    path('restaurants/add', views.MmsRestaurantCreateUpdateView.as_view(), name='add-restuarant'),
    path('restaurants/list', views.MmsRestaurantListView.as_view(), name='list-restuarants'),
    path('restaurants/<int:restaurantid>/update', views.MmsRestaurantCreateUpdateView.as_view(), name='update-restuarant'),
    path('restaurants/<int:restaurantid>/delete', views.MmsRestaurantDeleteView.as_view(), name='delete-restuarant'),
    path('activities/list', views.MmsActivityListView.as_view(), name='list-activity'),
    path('activities/add', views.MmsActivityCreateUpdateView.as_view(), name='add-activity'),
    path('activities/<int:activityid>/update', views.MmsActivityCreateUpdateView.as_view(), name='update-activity'),
    path('activities/<int:activityid>/delete', views.MmsActivityDeleteView.as_view(), name='update-activity'),
    path('locations/list', views.MmsRoomLocListView.as_view(), name='list-loctions'),
    path('locations/add', views.MmsRoomLocCreateUpdateView.as_view(), name='add-locaton'),
    path('locations/<int:locid>/update', views.MmsRoomLocCreateUpdateView.as_view(), name='update-location'),
    path('locations/<int:locid>/delete', views.MmsRoomLocDeleteView.as_view(), name='delete-location'),
    path('room-types/list', views.MmsRoomTypeListView.as_view(), name='list-room-types'),
    path('room-types/add', views.MmsRoomTypeCreateUpdateView.as_view(), name='add-room-type'),
    path('room-types/<int:stateroomtypeid>/update', views.MmsRoomTypeCreateUpdateView.as_view(), name='update-room-type'),
    path('room-types/<int:stateroomtypeid>/delete', views.MmsRoomTypeDeleteView.as_view(), name='delete-room-type'),
    path('rooms/add', views.MmsRoomCreateUpdateView.as_view(), name='room-create'),  # Single room creation
    path('rooms/<int:roomnumber>/update', views.MmsRoomCreateUpdateView.as_view(), name='room-update'),  # Single room update
    path('rooms/bulk-create', views.MmsRoomBulkCSVCreateView.as_view(), name='room-bulk-create'),  # Bulk create from CSV
    path('rooms/bulk-update', views.MmsRoomBulkUpdateView.as_view(), name='room-bulk-update'),  # Bulk update via UI
    path('rooms/list', views.MmsRoomListView.as_view(), name='list-rooms'),  
    path('rooms/<int:roomnumber>/delete', views.MmsRoomDeleteView.as_view(), name='delete-room'), 
    path('trips/add', views.MmsTripCreateUpdateView.as_view(), name='add-trips'),
    path('trips/<int:tripid>/update', views.MmsTripCreateUpdateView.as_view(), name='update-trips'),
    path('trips/list',views.MmsTripListView.as_view(),name = 'trip-list-view'),
    path('trips/list/<int:pk>', views.MmsTripDetailView.as_view(), name='trip-detail'),
    path('port-stops/add', views.MmsPortStopCreateUpdateView.as_view(), name='add-port-stops'),
    path('port-stops/<int:itineraryid>/update', views.MmsPortStopCreateUpdateView.as_view(), name='update-port-stops'),
    path('register', views.UserCreateView.as_view(), name='user-register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout', views.LogoutView.as_view(), name = 'logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('user/<int:id>/update', views.UserUpdateView.as_view(), name='user-update'),
    path('user/delete', views.UserDeleteView.as_view(), name='self-delete-user'),
    
]