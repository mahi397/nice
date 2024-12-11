# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class MmsActivity(models.Model):
    activityid = models.SmallAutoField(primary_key=True, db_comment='Unique identifier for every entertainment and activity')
    activitytype = models.CharField(max_length=30, db_collation='utf8mb4_unicode_ci', db_comment='Type of the activity')
    activityname = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', db_comment='Name of the activity\t')
    activitydescription = models.CharField(max_length=300, db_collation='utf8mb4_unicode_ci', db_comment='Description of the activity on board the ship.')
    floor = models.SmallIntegerField(db_comment='Floor at which the activity or entertainment is located')
    capacity = models.IntegerField(db_comment='Capacity of the activity/ entertainment')

    class Meta:
        managed = False
        db_table = 'mms_activity'


class MmsBooking(models.Model):
    bookingid = models.BigAutoField(primary_key=True, db_comment='Unique identifier for every booking')
    bookingdate = models.DateTimeField(db_comment='Date when the booking was made. Important for scheduling and availability tracking.')
    bookingstatus = models.CharField(max_length=20, db_collation='utf8mb4_unicode_ci', db_comment='Status of the booking, e.g., "Confirmed," "Pending," "Canceled." Assists with management tracking.')
    groupid = models.ForeignKey('MmsGroup', models.DO_NOTHING, db_column='groupid', db_comment='Unqiue identifier for every group')
    tripid = models.ForeignKey('MmsTrip', models.DO_NOTHING, db_column='tripid', db_comment='Primary key for each trip. Unique identifier for each trip entry.')
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userid')
    cancellationdate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mms_booking'


class MmsBookingPackage(models.Model):
    bookingid = models.ForeignKey(MmsBooking, models.DO_NOTHING, db_column='bookingid')
    packageid = models.ForeignKey('MmsPackage', models.DO_NOTHING, db_column='packageid')
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'mms_booking_package'


class MmsGroup(models.Model):
    groupid = models.BigAutoField(primary_key=True, db_comment='Unqiue identifier for every group')
    groupname = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', db_comment='Name of the group')
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'mms_group'


class MmsInvoice(models.Model):
    invoiceid = models.BigAutoField(primary_key=True, db_comment='Primary key for the invoice.')
    invoicedate = models.DateTimeField(db_comment='Date when the invoice was generated. Important for tracking billing and payment cycles.')
    totalamount = models.DecimalField(max_digits=8, decimal_places=2, db_comment='Total amount billed on the invoice ')
    paymentstatus = models.CharField(max_length=20, db_collation='utf8mb4_unicode_ci', db_comment='Indicates whether the invoice is "Paid," "Unpaid," or "Overdue." Tracks financial status.')
    bookingid = models.ForeignKey(MmsBooking, models.DO_NOTHING, db_column='bookingid', db_comment='Unique identifier for every booking')
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=15)
    email = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'mms_invoice'


class MmsPackage(models.Model):
    packageid = models.SmallAutoField(primary_key=True, db_comment='Unique identifier for every package')
    packagename = models.CharField(max_length=30, db_collation='utf8mb4_unicode_ci', db_comment='Name of the packages offered on the trip')
    base_price = models.DecimalField(max_digits=5, decimal_places=2, db_comment='Price of the package per person per night')
    packagedetails = models.CharField(max_length=255, db_collation='utf8mb4_unicode_ci', db_comment='Details of the package')

    class Meta:
        managed = False
        db_table = 'mms_package'


class MmsPassenger(models.Model):
    passengerid = models.BigAutoField(primary_key=True, db_comment='Unique identifier for each passenger')
    firstname = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', db_comment="Stores the passenger's first name")
    lastname = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', db_comment="Stores the passenger's last name")
    dateofbirth = models.DateTimeField(db_comment="Hold's the passenger's birth date")
    gender = models.CharField(max_length=1, db_collation='utf8mb4_unicode_ci', db_comment='Captures the gender of the passenger')
    contactnumber = models.CharField(max_length=15, db_collation='utf8mb4_unicode_ci', db_comment='A primary phone number to reach the passenger for notifications, emergencies, or updates related to their trip.')
    emailaddress = models.CharField(max_length=100, db_collation='utf8mb4_unicode_ci', db_comment='Stores the passengerΓö£├ä╬ô├ç┬úΓö£├ó╬ô├ç├¡Γö£├ó╬ô├ç├┤s email address for electronic communication, including booking confirmations and promotional materials.')
    streetaddr = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', db_comment="The street address of the passenger's primary residence, used for correspondence and identification purposes.")
    city = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', db_comment="Represents the passenger's residential address. This could be useful for billing, mailing tickets, or other physical correspondence.")
    state = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', db_comment="Represents the passenger's residential address. This could be useful for billing, mailing tickets, or other physical correspondence.")
    country = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', db_comment="Represents the passenger's residential address. This could be useful for billing, mailing tickets, or other physical correspondence.")
    zipcode = models.CharField(max_length=5, db_collation='utf8mb4_unicode_ci', db_comment="Represents the passenger's residential address. This could be useful for billing, mailing tickets, or other physical correspondence.")
    nationality = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', db_comment="Records the passenger's nationality, which may be relevant for certain legal or travel restrictions.")
    passportnumber = models.CharField(max_length=20, db_collation='utf8mb4_unicode_ci', db_comment='Stores the passport number, useful for international cruise trips where passport details are required for customs and immigration checks.')
    emergencycontactname = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', db_comment='The name of a designated emergency contact who can be notified if needed.')
    emergencycontactnumber = models.CharField(max_length=15, db_collation='utf8mb4_unicode_ci', db_comment='The contact number for the emergency contact, ensuring quick reachability in case of emergencies during the trip.')
    groupid = models.ForeignKey(MmsGroup, models.DO_NOTHING, db_column='groupid', db_comment='Unqiue identifier for every group')

    class Meta:
        managed = False
        db_table = 'mms_passenger'


class MmsPaymentDetail(models.Model):
    paymentid = models.BigAutoField(primary_key=True, db_comment='Primary key for each payment record.')
    paymentdate = models.DateTimeField(db_comment='Date when the payment was made. Important for financial records.')
    paymentamount = models.DecimalField(max_digits=6, decimal_places=2, db_comment='Amount paid during the transaction. Helps track partial or full payments.')
    paymentmethod = models.CharField(max_length=20, db_collation='utf8mb4_unicode_ci', db_comment='Method of payment (e.g., "Credit Card," "Bank Transfer," "Cash"). Provides context for processing.')
    transactionid = models.CharField(max_length=100, db_collation='utf8mb4_unicode_ci', db_comment='Unique ID from the payment provider for reference. Useful for audits and confirmations.')
    invoiceid = models.ForeignKey(MmsInvoice, models.DO_NOTHING, db_column='invoiceid', db_comment='Primary key for the invoice.')

    class Meta:
        managed = False
        db_table = 'mms_payment_detail'


class MmsPort(models.Model):
    portid = models.AutoField(primary_key=True, db_comment='Primary key for the port entity. Unique identifier for each port.')
    portname = models.CharField(max_length=100, db_collation='utf8mb4_unicode_ci', db_comment='The name of the port where the cruise either stops during the itinerary or starts/ends the trip. This attribute identifies specific locations included in the trip.')
    address = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', db_comment='Street address where the port is located. ')
    portcity = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', db_comment='Name of the country where the port is located. Useful for regional sorting and queries.')
    portstate = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', db_comment='Name of the state (if applicable) where the port is located. Adds further location specificity.')
    portcountry = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', db_comment='Name of the city where the port is located. Useful for detailed geographical reference.')
    nearestairport = models.CharField(max_length=100, db_collation='utf8mb4_unicode_ci', db_comment='Name of the nearest airport to the port')
    parkingspots = models.IntegerField(db_comment='Number of parking spots available at the port')

    class Meta:
        managed = False
        db_table = 'mms_port'


class MmsPortStop(models.Model):
    itineraryid = models.BigAutoField(primary_key=True, db_comment='Unique identifier for every port stop of a trip')
    portid = models.ForeignKey(MmsPort, models.DO_NOTHING, db_column='portid', db_comment='Primary key for the port entity. Unique identifier for each port.', related_name='portstops')
    tripid = models.ForeignKey('MmsTrip', models.DO_NOTHING, db_column='tripid', db_comment='Primary key for each trip. Unique identifier for each trip entry.', related_name='portstops')
    arrivaltime = models.DateTimeField(blank=True, null=True, db_comment='Time at which the ship arrives at the port')
    departuretime = models.DateTimeField(blank=True, null=True, db_comment='Time of departure from the port')
    orderofstop = models.IntegerField(db_comment='The order in which the ship stops at each port')
    isstartport = models.IntegerField(db_comment='Indicates if the port is starting point of the trip')
    isendport = models.IntegerField(db_comment='Indicates if the port is ending point of the trip')
    description = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'mms_port_stop'


class MmsRestaurant(models.Model):
    restaurantid = models.SmallAutoField(primary_key=True, db_comment='Unique identifier for each restaurant')
    restaurantname = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', db_comment='Name of the resturant')
    floornumber = models.SmallIntegerField(db_comment='Floor where the restaurant is located in the ship')
    openingtime = models.TimeField(blank=True, null=True, db_comment='Time at which the restaurant opens')
    closingtime = models.TimeField(blank=True, null=True, db_comment='Time at which the restaurant closes')
    servesbreakfast = models.CharField(max_length=1, db_collation='utf8mb4_unicode_ci', db_comment="Value to specify if the restaurant serves breakfast or not. For e.g., 'Y' for yes and 'N' for no")
    serveslunch = models.CharField(max_length=1, db_collation='utf8mb4_unicode_ci', db_comment="Value to specify if the restaurant serves lunch or not. For e.g., 'Y' for yes and 'N' for no")
    servesdinner = models.CharField(max_length=1, db_collation='utf8mb4_unicode_ci', db_comment="Value to specify if the restaurant serves dinner or not. For e.g., 'Y' for yes and 'N' for no")
    servesalcohol = models.CharField(max_length=1, db_collation='utf8mb4_unicode_ci', db_comment="Value to specify if the restaurant serves alcohol or not. For e.g., 'Y' for yes and 'N' for no")
    restaurant_description = models.CharField(max_length=45, db_collation='utf8mb4_unicode_ci', db_comment='Description of the cuisine served with the restaurant.')

    class Meta:
        managed = False
        db_table = 'mms_restaurant'


class MmsRoom(models.Model):
    roomnumber = models.IntegerField(primary_key=True)
    roomfloor = models.SmallIntegerField(db_comment='Floor number of the room')
    stateroomtypeid = models.ForeignKey('MmsRoomType', models.DO_NOTHING, db_column='stateroomtypeid', db_comment='Unique identifier of room type')
    locid = models.ForeignKey('MmsRoomLoc', models.DO_NOTHING, db_column='locid')

    class Meta:
        managed = False
        db_table = 'mms_room'


class MmsRoomLoc(models.Model):
    locid = models.SmallAutoField(primary_key=True, db_comment='Unique ID of the location in the ship')
    location = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', db_comment='Name of the location in the ship')

    class Meta:
        managed = False
        db_table = 'mms_room_loc'


class MmsRoomType(models.Model):
    stateroomtypeid = models.SmallAutoField(primary_key=True, db_comment='Unique identifier of room type')
    stateroomtype = models.CharField(max_length=20, db_collation='utf8mb4_unicode_ci', db_comment='Name of the stateroom type')
    roomsize = models.BigIntegerField(db_comment='Size of the stateroom in SQFT')
    numberofbeds = models.SmallIntegerField(db_comment='Number of beds in the room')
    numberofbaths = models.DecimalField(max_digits=2, decimal_places=1, db_comment='Number of the bathrooms in the stateroom')
    numberofbalconies = models.SmallIntegerField(db_comment='Number of balconies in the stateroom')
    roomtypedescription = models.CharField(max_length=500)
    baseprice = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'mms_room_type'


class MmsShip(models.Model):
    shipid = models.AutoField(primary_key=True, db_comment='Unique identifier for every ship')
    shipname = models.CharField(max_length=45, db_collation='utf8mb4_0900_ai_ci')
    description = models.CharField(max_length=150, db_collation='utf8mb4_0900_ai_ci')
    capacity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'mms_ship'


class MmsShipActivity(models.Model):
    shipid = models.ForeignKey(MmsShip, models.DO_NOTHING, db_column='shipid')
    activityid = models.ForeignKey(MmsActivity, models.DO_NOTHING, db_column='activityid')

    class Meta:
        managed = False
        db_table = 'mms_ship_activity'


class MmsShipRestaurant(models.Model):
    shipid = models.ForeignKey(MmsShip, models.DO_NOTHING, db_column='shipid')
    restaurantid = models.ForeignKey(MmsRestaurant, models.DO_NOTHING, db_column='restaurantid')

    class Meta:
        managed = False
        db_table = 'mms_ship_restaurant'


class MmsShipRoom(models.Model):
    shiproomid = models.AutoField(primary_key=True)
    shipid = models.ForeignKey(MmsShip, models.DO_NOTHING, db_column='shipid')
    roomnumber = models.ForeignKey(MmsRoom, models.DO_NOTHING, db_column='roomnumber')

    class Meta:
        managed = False
        db_table = 'mms_ship_room'


class MmsTrip(models.Model):
    tripid = models.BigAutoField(primary_key=True, db_comment='Primary key for each trip. Unique identifier for each trip entry.')
    tripname = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', db_comment='Descriptive name of the trip.')
    startdate = models.DateField(db_comment='The date when the trip begins. Ensures accurate tracking of trip schedules.')
    enddate = models.DateField(db_comment='The date when the trip ends. Helps define the trip duration.')
    tripcostperperson = models.DecimalField(max_digits=8, decimal_places=2, db_comment='Cost per person for the trip, including taxes. Supports budgeting and billing.')
    tripstatus = models.CharField(max_length=20, db_collation='utf8mb4_unicode_ci', db_comment='Status of the trip (e.g., upcoming, ongoing, completed).')
    cancellationpolicy = models.CharField(max_length=300, db_collation='utf8mb4_unicode_ci', db_comment='Trip cancellation status ΓÇÿcanceledΓÇÖ.')
    tripcapacity = models.IntegerField(db_comment='Total passenger capacity for the cruise liner.')
    tripdescription = models.CharField(max_length=300, db_collation='utf8mb4_unicode_ci', db_comment='Description of the trip booked.')
    finalbookingdate = models.DateField()
    tripcapacityremaining = models.IntegerField()
    tempcapacityreserved = models.IntegerField()
    tempreservationtimestamp = models.DateTimeField(blank=True, null=True)
    tempcapacitynumber = models.IntegerField(blank=True, null=True)
    shipid = models.ForeignKey(MmsShip, models.DO_NOTHING, db_column='shipid')

    class Meta:
        managed = False
        db_table = 'mms_trip'


class MmsTripPackage(models.Model):
    tripid = models.ForeignKey(MmsTrip, models.DO_NOTHING, db_column='tripid')
    packageid = models.ForeignKey(MmsPackage, models.DO_NOTHING, db_column='packageid')

    class Meta:
        managed = False
        db_table = 'mms_trip_package'


class MmsTripRoom(models.Model):
    dynamicprice = models.DecimalField(max_digits=6, decimal_places=2)
    baseprice = models.DecimalField(max_digits=6, decimal_places=2)
    isbooked = models.IntegerField()
    roomtype = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    roomnumber = models.ForeignKey(MmsRoom, models.DO_NOTHING, db_column='roomnumber')
    tripid = models.ForeignKey(MmsTrip, models.DO_NOTHING, db_column='tripid')
    tempreserved = models.IntegerField(blank=True, null=True)
    tempreservationtimestamp = models.DateTimeField(blank=True, null=True)
    tempreservationuser = models.IntegerField(blank=True, null=True)
    bookingid = models.ForeignKey(MmsBooking, models.DO_NOTHING, db_column='bookingid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mms_trip_room'


class MmsUserProfile(models.Model):
    profileid = models.AutoField(primary_key=True)
    phonenumber = models.CharField(max_length=15, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)
    dateofbirth = models.DateField(blank=True, null=True)
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userid')

    class Meta:
        managed = False
        db_table = 'mms_user_profile'


class TokenBlacklistBlacklistedtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    blacklisted_at = models.DateTimeField()
    token = models.OneToOneField('TokenBlacklistOutstandingtoken', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'token_blacklist_blacklistedtoken'


class TokenBlacklistOutstandingtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    jti = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'token_blacklist_outstandingtoken'
