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
    path('admin/login', views.AdminLoginView.as_view(), name='staff-login'),
    path('admin/logout', views.AdminLogoutView.as_view(), name='staff-logout'),
    path('admin/ports/list', views.MmsPortListView.as_view(), name='list-ports'),
    path('admin/ports/add', views.MmsPortCreateUpdateView.as_view(), name='add-port'),
    path('admin/ports/<int:portid>/update', views.MmsPortCreateUpdateView.as_view(), name='update-port'),
    path('admin/ports/<int:portid>/delete', views.MmsPortDeleteView.as_view(), name='del-port'),
    path('admin/restaurants/add', views.MmsRestaurantCreateUpdateView.as_view(), name='add-restuarant'),
    path('admin/restaurants/list', views.MmsRestaurantListView.as_view(), name='list-restuarants'),
    path('admin/restaurants/<int:restaurantid>/update', views.MmsRestaurantCreateUpdateView.as_view(), name='update-restuarant'),
    path('admin/restaurants/<int:restaurantid>/delete', views.MmsRestaurantDeleteView.as_view(), name='delete-restuarant'),
    path('admin/activities/list', views.MmsActivityListView.as_view(), name='list-activity'),
    path('admin/activities/add', views.MmsActivityCreateUpdateView.as_view(), name='add-activity'),
    path('admin/activities/<int:activityid>/update', views.MmsActivityCreateUpdateView.as_view(), name='update-activity'),
    path('admin/activities/<int:activityid>/delete', views.MmsActivityDeleteView.as_view(), name='update-activity'),
    path('admin/locations/list', views.MmsRoomLocListView.as_view(), name='list-loctions'),
    path('admin/locations/add', views.MmsRoomLocCreateUpdateView.as_view(), name='add-locaton'),
    path('admin/locations/<int:locid>/update', views.MmsRoomLocCreateUpdateView.as_view(), name='update-location'),
    path('admin/locations/<int:locid>/delete', views.MmsRoomLocDeleteView.as_view(), name='delete-location'),
    path('admin/room-types/list', views.MmsRoomTypeListView.as_view(), name='list-room-types'),
    path('admin/room-types/add', views.MmsRoomTypeCreateUpdateView.as_view(), name='add-room-type'),
    path('admin/room-types/<int:stateroomtypeid>/update', views.MmsRoomTypeCreateUpdateView.as_view(), name='update-room-type'),
    path('admin/room-types/<int:stateroomtypeid>/delete', views.MmsRoomTypeDeleteView.as_view(), name='delete-room-type'),
    path('admin/rooms/add', views.MmsRoomCreateView.as_view(), name='add-rooms'),
    path('admin/rooms/list', views.MmsRoomListView.as_view(), name='list-rooms'),  
    path('admin/rooms/<int:roomnumber>/delete', views.MmsRoomDeleteView.as_view(), name='delete-room'), 
    path('admin/ships/list', views.MmsShipListView.as_view(), name='list-ships'),
    path('admin/ships/add', views.MmsShipCreateView.as_view(), name='add-ship'),
    path('admin/ships/<int:shipid>/delete', views.MmsShipDeleteView.as_view(), name='delete-ship'),
    path('admin/packages/list', views.MmsPackageListView.as_view(), name='list-packages'),
    path('admin/packages/add', views.MmsPackageCreateUpdateView.as_view(), name='add-package'),
    path('admin/packages/<int:packageid>/update', views.MmsPackageCreateUpdateView.as_view(), name='update-package'),
    path('admin/packages/<int:packageid>/delete', views.MmsPackageDeleteView.as_view(), name='delete-package'),
    path('admin/trips/add', views.MmsTripAddView.as_view(), name='add-trips'),
    path('admin/trips/<int:tripid>/update', views.MmsTripAddView.as_view(), name='update-trips'),
    path('admin/trips/list',views.MmsTripListView.as_view(),name = 'trip-list-view'),
    path('admin/trips/list/<int:pk>', views.MmsTripDetailView.as_view(), name='trip-detail'),
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
