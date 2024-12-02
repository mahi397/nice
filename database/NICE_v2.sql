-- MySQL dump 10.13  Distrib 8.0.40, for macos14 (arm64)
--
-- Host: 127.0.0.1    Database: nice
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_activity`
--

DROP TABLE IF EXISTS `mms_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_activity` (
  `activityid` smallint NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for every entertainment and activity',
  `activitytype` varchar(30) NOT NULL COMMENT 'Type of the activity',
  `activityname` varchar(50) NOT NULL COMMENT 'Name of the activity	',
  `activity_description` varchar(45) NOT NULL COMMENT 'Description of the activity on board the ship.',
  `floor` smallint NOT NULL COMMENT 'Floor at which the activity or entertainment is located',
  `capacity` int NOT NULL COMMENT 'Capacity of the activity/ entertainment',
  PRIMARY KEY (`activityid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_activity`
--

LOCK TABLES `mms_activity` WRITE;
/*!40000 ALTER TABLE `mms_activity` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_activity_psngr`
--

DROP TABLE IF EXISTS `mms_activity_psngr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_activity_psngr` (
  `actreservationid` bigint NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for each entertainment and activity reservation',
  `activityid` smallint NOT NULL COMMENT 'Unique identifier for every entertainment and activity',
  `passengerid` bigint DEFAULT NULL COMMENT 'Unique identifier for each passenger',
  PRIMARY KEY (`actreservationid`),
  KEY `mms_psngr_mms_activity_fk` (`activityid`),
  KEY `mms_activity_mms_psngr_fk` (`passengerid`),
  CONSTRAINT `mms_activity_mms_psngr_fk` FOREIGN KEY (`passengerid`) REFERENCES `mms_passenger` (`passengerid`),
  CONSTRAINT `mms_psngr_mms_activity_fk` FOREIGN KEY (`activityid`) REFERENCES `mms_activity` (`activityid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_activity_psngr`
--

LOCK TABLES `mms_activity_psngr` WRITE;
/*!40000 ALTER TABLE `mms_activity_psngr` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_activity_psngr` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_booking`
--

DROP TABLE IF EXISTS `mms_booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_booking` (
  `bookingid` bigint NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for every booking',
  `bookingdate` datetime NOT NULL COMMENT 'Date when the booking was made. Important for scheduling and availability tracking.',
  `bookingstatus` varchar(20) NOT NULL COMMENT 'Status of the booking, e.g., "Confirmed," "Pending," "Canceled." Assists with management tracking.',
  `estimatedcost` decimal(8,2) NOT NULL COMMENT 'Estimated cost for the trip including base cost, room price and package price exclusing tax and other add ons',
  `groupid` bigint NOT NULL COMMENT 'Unqiue identifier for every group',
  `tripid` bigint NOT NULL COMMENT 'Primary key for each trip. Unique identifier for each trip entry.',
  `userid` int NOT NULL,
  PRIMARY KEY (`bookingid`),
  KEY `mms_booking_mms_group_fk` (`groupid`),
  KEY `mms_booking_mms_trip_fk` (`tripid`),
  KEY `fk_auth_user_booking` (`userid`),
  CONSTRAINT `fk_auth_user_booking` FOREIGN KEY (`userid`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `mms_booking_mms_group_fk` FOREIGN KEY (`groupid`) REFERENCES `mms_group` (`groupid`),
  CONSTRAINT `mms_booking_mms_trip_fk` FOREIGN KEY (`tripid`) REFERENCES `mms_trip` (`tripid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_booking`
--

LOCK TABLES `mms_booking` WRITE;
/*!40000 ALTER TABLE `mms_booking` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_group`
--

DROP TABLE IF EXISTS `mms_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_group` (
  `groupid` bigint NOT NULL AUTO_INCREMENT COMMENT 'Unqiue identifier for every group',
  `groupname` varchar(50) NOT NULL COMMENT 'Name of the group',
  PRIMARY KEY (`groupid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_group`
--

LOCK TABLES `mms_group` WRITE;
/*!40000 ALTER TABLE `mms_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_invoice`
--

DROP TABLE IF EXISTS `mms_invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_invoice` (
  `invoiceid` bigint NOT NULL AUTO_INCREMENT COMMENT 'Primary key for the invoice.',
  `invoicedate` datetime NOT NULL COMMENT 'Date when the invoice was generated. Important for tracking billing and payment cycles.',
  `totalamount` decimal(8,2) NOT NULL COMMENT 'Total amount billed on the invoice ',
  `paymentstatus` varchar(20) NOT NULL COMMENT 'Indicates whether the invoice is "Paid," "Unpaid," or "Overdue." Tracks financial status.',
  `duedate` datetime NOT NULL COMMENT 'Date by which the payment should be completed. Ensures timely collection.',
  `bookingid` bigint NOT NULL COMMENT 'Unique identifier for every booking',
  PRIMARY KEY (`invoiceid`),
  KEY `mms_invoice_mms_booking_fk` (`bookingid`),
  CONSTRAINT `mms_invoice_mms_booking_fk` FOREIGN KEY (`bookingid`) REFERENCES `mms_booking` (`bookingid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_invoice`
--

LOCK TABLES `mms_invoice` WRITE;
/*!40000 ALTER TABLE `mms_invoice` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_package`
--

DROP TABLE IF EXISTS `mms_package`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_package` (
  `packageid` smallint NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for every package',
  `packagename` varchar(30) NOT NULL COMMENT 'Name of the packages offered on the trip',
  `base_price` decimal(5,2) NOT NULL COMMENT 'Price of the package per person per night',
  `packagedetails` varchar(255) NOT NULL COMMENT 'Details of the package',
  PRIMARY KEY (`packageid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_package`
--

LOCK TABLES `mms_package` WRITE;
/*!40000 ALTER TABLE `mms_package` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_package` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_passenger`
--

DROP TABLE IF EXISTS `mms_passenger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_passenger` (
  `passengerid` bigint NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for each passenger',
  `firstname` varchar(50) NOT NULL COMMENT 'Stores the passenger''s first name',
  `lastname` varchar(50) NOT NULL COMMENT 'Stores the passenger''s last name',
  `dateofbirth` datetime NOT NULL COMMENT 'Hold''s the passenger''s birth date',
  `gender` char(1) NOT NULL COMMENT 'Captures the gender of the passenger',
  `contactnumber` varchar(10) NOT NULL COMMENT 'A primary phone number to reach the passenger for notifications, emergencies, or updates related to their trip.',
  `emailaddress` varchar(100) NOT NULL COMMENT 'Stores the passenger├ÄΓÇ£├âΓÇí├âΓÇôs email address for electronic communication, including booking confirmations and promotional materials.',
  `streetaddr` varchar(50) NOT NULL COMMENT 'The street address of the passenger''s primary residence, used for correspondence and identification purposes.',
  `city` varchar(50) NOT NULL COMMENT 'Represents the passenger''s residential address. This could be useful for billing, mailing tickets, or other physical correspondence.',
  `state` varchar(50) NOT NULL COMMENT 'Represents the passenger''s residential address. This could be useful for billing, mailing tickets, or other physical correspondence.',
  `country` varchar(50) NOT NULL COMMENT 'Represents the passenger''s residential address. This could be useful for billing, mailing tickets, or other physical correspondence.',
  `zipcode` varchar(5) NOT NULL COMMENT 'Represents the passenger''s residential address. This could be useful for billing, mailing tickets, or other physical correspondence.',
  `nationality` varchar(50) NOT NULL COMMENT 'Records the passenger''s nationality, which may be relevant for certain legal or travel restrictions.',
  `passportnumber` varchar(20) NOT NULL COMMENT 'Stores the passport number, useful for international cruise trips where passport details are required for customs and immigration checks.',
  `emergencycontactname` varchar(50) NOT NULL COMMENT 'The name of a designated emergency contact who can be notified if needed.',
  `emergencycontactnumber` varchar(10) NOT NULL COMMENT 'The contact number for the emergency contact, ensuring quick reachability in case of emergencies during the trip.',
  `groupid` bigint NOT NULL COMMENT 'Unqiue identifier for every group',
  PRIMARY KEY (`passengerid`),
  KEY `mms_passenger_mms_group_fk` (`groupid`),
  CONSTRAINT `mms_passenger_mms_group_fk` FOREIGN KEY (`groupid`) REFERENCES `mms_group` (`groupid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_passenger`
--

LOCK TABLES `mms_passenger` WRITE;
/*!40000 ALTER TABLE `mms_passenger` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_passenger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_payment_detail`
--

DROP TABLE IF EXISTS `mms_payment_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_payment_detail` (
  `paymentid` bigint NOT NULL AUTO_INCREMENT COMMENT 'Primary key for each payment record.',
  `paymentdate` datetime NOT NULL COMMENT 'Date when the payment was made. Important for financial records.',
  `paymentamount` decimal(6,2) NOT NULL COMMENT 'Amount paid during the transaction. Helps track partial or full payments.',
  `paymentmethod` varchar(20) NOT NULL COMMENT 'Method of payment (e.g., "Credit Card," "Bank Transfer," "Cash"). Provides context for processing.',
  `transactionid` varchar(100) NOT NULL COMMENT 'Unique ID from the payment provider for reference. Useful for audits and confirmations.',
  `invoiceid` bigint NOT NULL COMMENT 'Primary key for the invoice.',
  PRIMARY KEY (`paymentid`,`invoiceid`),
  KEY `mms_payment_mms_invoice_fk` (`invoiceid`),
  CONSTRAINT `mms_payment_mms_invoice_fk` FOREIGN KEY (`invoiceid`) REFERENCES `mms_invoice` (`invoiceid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_payment_detail`
--

LOCK TABLES `mms_payment_detail` WRITE;
/*!40000 ALTER TABLE `mms_payment_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_payment_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_port`
--

DROP TABLE IF EXISTS `mms_port`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_port` (
  `portid` int NOT NULL COMMENT 'Primary key for the port entity. Unique identifier for each port.',
  `portname` varchar(100) NOT NULL COMMENT 'The name of the port where the cruise either stops during the itinerary or starts/ends the trip. This attribute identifies specific locations included in the trip.',
  `address` varchar(50) NOT NULL COMMENT 'Street address where the port is located. ',
  `portcity` varchar(50) NOT NULL COMMENT 'Name of the country where the port is located. Useful for regional sorting and queries.',
  `portstate` varchar(50) NOT NULL COMMENT 'Name of the state (if applicable) where the port is located. Adds further location specificity.',
  `portcountry` varchar(50) NOT NULL COMMENT 'Name of the city where the port is located. Useful for detailed geographical reference.',
  `nearestairport` varchar(100) NOT NULL COMMENT 'Name of the nearest airport to the port',
  `parkingspots` int NOT NULL COMMENT 'Number of parking spots available at the port',
  PRIMARY KEY (`portid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_port`
--

LOCK TABLES `mms_port` WRITE;
/*!40000 ALTER TABLE `mms_port` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_port` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_port_stop`
--

DROP TABLE IF EXISTS `mms_port_stop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_port_stop` (
  `itineraryid` bigint NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for every port stop of a trip',
  `portid` int NOT NULL COMMENT 'Primary key for the port entity. Unique identifier for each port.',
  `tripid` bigint NOT NULL COMMENT 'Primary key for each trip. Unique identifier for each trip entry.',
  `arrivaltime` datetime DEFAULT NULL COMMENT 'Time at which the ship arrives at the port',
  `departuretime` datetime DEFAULT NULL COMMENT 'Time of departure from the port',
  `orderofstop` smallint NOT NULL COMMENT 'The order in which the ship stops at each port',
  `isstartport` char(1) NOT NULL COMMENT 'Indicates if the port is starting point of the trip',
  `isendport` char(1) NOT NULL COMMENT 'Indicates if the port is ending point of the trip',
  PRIMARY KEY (`itineraryid`),
  KEY `mms_port_stop_mms_port_fk` (`portid`),
  KEY `mms_port_stop_mms_trip_fk` (`tripid`),
  CONSTRAINT `mms_port_stop_mms_port_fk` FOREIGN KEY (`portid`) REFERENCES `mms_port` (`portid`),
  CONSTRAINT `mms_port_stop_mms_trip_fk` FOREIGN KEY (`tripid`) REFERENCES `mms_trip` (`tripid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_port_stop`
--

LOCK TABLES `mms_port_stop` WRITE;
/*!40000 ALTER TABLE `mms_port_stop` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_port_stop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_psngr_package`
--

DROP TABLE IF EXISTS `mms_psngr_package`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_psngr_package` (
  `purchaseid` bigint NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for every package purchased by the passenger',
  `packageid` smallint NOT NULL COMMENT 'Unique identifier for every package',
  `passengerid` bigint DEFAULT NULL COMMENT 'Unique identifier for each passenger',
  `sale_price` decimal(6,2) NOT NULL COMMENT 'The actual price paid by the passenger for the package at the time of booking. \nThis price may differ from the base price in the mms_package table due to discounts, promotions, or special offers applied at the time of purchase.\n ',
  PRIMARY KEY (`purchaseid`),
  KEY `mms_package_mms_psngr_fk` (`passengerid`),
  KEY `mms_psngr_mms_package_fk` (`packageid`),
  CONSTRAINT `mms_package_mms_psngr_fk` FOREIGN KEY (`passengerid`) REFERENCES `mms_passenger` (`passengerid`),
  CONSTRAINT `mms_psngr_mms_package_fk` FOREIGN KEY (`packageid`) REFERENCES `mms_package` (`packageid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_psngr_package`
--

LOCK TABLES `mms_psngr_package` WRITE;
/*!40000 ALTER TABLE `mms_psngr_package` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_psngr_package` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_restaurant`
--

DROP TABLE IF EXISTS `mms_restaurant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_restaurant` (
  `restaurantid` smallint NOT NULL COMMENT 'Unique identifier for each restaurant',
  `restaurantname` varchar(50) NOT NULL COMMENT 'Name of the resturant',
  `floornumber` smallint NOT NULL COMMENT 'Floor where the restaurant is located in the ship',
  `openingtime` time DEFAULT NULL COMMENT 'Time at which the restaurant opens',
  `closingtime` time DEFAULT NULL COMMENT 'Time at which the restaurant closes',
  `servesbreakfast` char(1) NOT NULL COMMENT 'Value to specify if the restaurant serves breakfast or not. For e.g., ''Y'' for yes and ''N'' for no',
  `serveslunch` char(1) NOT NULL COMMENT 'Value to specify if the restaurant serves lunch or not. For e.g., ''Y'' for yes and ''N'' for no',
  `servesdinner` char(1) NOT NULL COMMENT 'Value to specify if the restaurant serves dinner or not. For e.g., ''Y'' for yes and ''N'' for no',
  `servesalcohol` char(1) NOT NULL COMMENT 'Value to specify if the restaurant serves alcohol or not. For e.g., ''Y'' for yes and ''N'' for no',
  `resturant_description` varchar(45) NOT NULL COMMENT 'Description of the cuisine served with the restaurant.',
  PRIMARY KEY (`restaurantid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_restaurant`
--

LOCK TABLES `mms_restaurant` WRITE;
/*!40000 ALTER TABLE `mms_restaurant` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_restaurant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_restaurant_psngr`
--

DROP TABLE IF EXISTS `mms_restaurant_psngr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_restaurant_psngr` (
  `restreservationid` bigint NOT NULL AUTO_INCREMENT COMMENT 'Unique ID for every restaurant reservation',
  `restaurantid` smallint NOT NULL COMMENT 'Unique identifier for each restaurant',
  `passengerid` bigint DEFAULT NULL COMMENT 'Unique identifier for each passenger',
  PRIMARY KEY (`restreservationid`),
  KEY `mms_psngr_mms_restaurant_fk` (`restaurantid`),
  KEY `mms_restaurant_mms_psngr_fk` (`passengerid`),
  CONSTRAINT `mms_psngr_mms_restaurant_fk` FOREIGN KEY (`restaurantid`) REFERENCES `mms_restaurant` (`restaurantid`),
  CONSTRAINT `mms_restaurant_mms_psngr_fk` FOREIGN KEY (`passengerid`) REFERENCES `mms_passenger` (`passengerid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_restaurant_psngr`
--

LOCK TABLES `mms_restaurant_psngr` WRITE;
/*!40000 ALTER TABLE `mms_restaurant_psngr` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_restaurant_psngr` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_room`
--

DROP TABLE IF EXISTS `mms_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_room` (
  `roomnumber` int NOT NULL COMMENT 'Unique identifier for every room',
  `roomfloor` smallint NOT NULL COMMENT 'Floor number of the room',
  `roombaseprice` decimal(8,2) NOT NULL COMMENT 'Price of the room per night',
  `stateroomtypeid` smallint NOT NULL COMMENT 'Unique identifier of room type',
  `locid` smallint NOT NULL,
  PRIMARY KEY (`roomnumber`),
  KEY `mms_room_mms_room_loc_fk` (`locid`),
  KEY `mms_room_mms_room_type_fk` (`stateroomtypeid`),
  CONSTRAINT `mms_room_mms_room_loc_fk` FOREIGN KEY (`locid`) REFERENCES `mms_room_loc` (`locid`),
  CONSTRAINT `mms_room_mms_room_type_fk` FOREIGN KEY (`stateroomtypeid`) REFERENCES `mms_room_type` (`stateroomtypeid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_room`
--

LOCK TABLES `mms_room` WRITE;
/*!40000 ALTER TABLE `mms_room` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_room_loc`
--

DROP TABLE IF EXISTS `mms_room_loc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_room_loc` (
  `locid` smallint NOT NULL COMMENT 'Unique ID of the location	in the ship',
  `location` varchar(50) NOT NULL COMMENT 'Name of the location in the ship',
  PRIMARY KEY (`locid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_room_loc`
--

LOCK TABLES `mms_room_loc` WRITE;
/*!40000 ALTER TABLE `mms_room_loc` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_room_loc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_room_type`
--

DROP TABLE IF EXISTS `mms_room_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_room_type` (
  `stateroomtypeid` smallint NOT NULL COMMENT 'Unique identifier of room type',
  `stateroomtype` varchar(20) NOT NULL COMMENT 'Name of the stateroom type',
  `roomsize` bigint NOT NULL COMMENT 'Size of the stateroom in SQFT',
  `numberofbeds` smallint NOT NULL COMMENT 'Number of beds in the room',
  `numberofbaths` decimal(2,1) NOT NULL COMMENT 'Number of the bathrooms in the stateroom',
  `numberofbalconies` smallint NOT NULL COMMENT 'Number of balconies in the stateroom',
  PRIMARY KEY (`stateroomtypeid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_room_type`
--

LOCK TABLES `mms_room_type` WRITE;
/*!40000 ALTER TABLE `mms_room_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_room_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_trip`
--

DROP TABLE IF EXISTS `mms_trip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_trip` (
  `tripid` bigint NOT NULL AUTO_INCREMENT COMMENT 'Primary key for each trip. Unique identifier for each trip entry.',
  `tripname` varchar(50) NOT NULL COMMENT 'Descriptive name of the trip.',
  `startdate` datetime NOT NULL COMMENT 'The date when the trip begins. Ensures accurate tracking of trip schedules.',
  `enddate` datetime NOT NULL COMMENT 'The date when the trip ends. Helps define the trip duration.',
  `tripcostperperson` decimal(8,2) NOT NULL COMMENT 'Cost per person for the trip, including taxes. Supports budgeting and billing.',
  `tripstatus` varchar(20) NOT NULL COMMENT 'Status of the trip (e.g., upcoming, ongoing, completed).',
  `trip_cancellation` varchar(10) NOT NULL COMMENT 'Trip cancellation status ‘canceled’.',
  `trip_capacity` int NOT NULL COMMENT 'Total passenger capacity for the cruise liner.',
  `trip_description` text NOT NULL COMMENT 'Description of the trip booked.',
  `final_booking` date NOT NULL,
  PRIMARY KEY (`tripid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_trip`
--

LOCK TABLES `mms_trip` WRITE;
/*!40000 ALTER TABLE `mms_trip` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_trip` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_trip_activity`
--

DROP TABLE IF EXISTS `mms_trip_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_trip_activity` (
  `tripactivityid` int NOT NULL AUTO_INCREMENT COMMENT 'A unique identifier for each record in the trip_activity junction table. This serves as the primary key and distinguishes each trip-activity relationship.',
  `tripid` bigint NOT NULL,
  `activityid` smallint NOT NULL COMMENT 'Unique identifier for every entertainment and activity',
  PRIMARY KEY (`tripactivityid`),
  KEY `mms_activity_mms_trip_fk` (`tripid`),
  KEY `mms_trip_mms_activity_fk` (`activityid`),
  CONSTRAINT `mms_activity_mms_trip_fk` FOREIGN KEY (`tripid`) REFERENCES `mms_trip` (`tripid`),
  CONSTRAINT `mms_trip_mms_activity_fk` FOREIGN KEY (`activityid`) REFERENCES `mms_activity` (`activityid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_trip_activity`
--

LOCK TABLES `mms_trip_activity` WRITE;
/*!40000 ALTER TABLE `mms_trip_activity` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_trip_activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_trip_restaurant`
--

DROP TABLE IF EXISTS `mms_trip_restaurant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_trip_restaurant` (
  `restauranttripid` int NOT NULL AUTO_INCREMENT COMMENT 'A unique identifier for each record in the trip_restaurant junction table. This serves as the primary key and uniquely identifies the relationship between a trip and a restaurant.',
  `tripid` bigint NOT NULL COMMENT 'Primary key for each trip. Unique identifier for each trip entry.',
  `restaurantid` smallint NOT NULL COMMENT 'Unique identifier for each restaurant',
  PRIMARY KEY (`restauranttripid`),
  KEY `mms_restaurant_mms_trip_fk` (`tripid`),
  KEY `mms_trip_mms_restaurant_fk` (`restaurantid`),
  CONSTRAINT `mms_restaurant_mms_trip_fk` FOREIGN KEY (`tripid`) REFERENCES `mms_trip` (`tripid`),
  CONSTRAINT `mms_trip_mms_restaurant_fk` FOREIGN KEY (`restaurantid`) REFERENCES `mms_restaurant` (`restaurantid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_trip_restaurant`
--

LOCK TABLES `mms_trip_restaurant` WRITE;
/*!40000 ALTER TABLE `mms_trip_restaurant` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_trip_restaurant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_trip_room`
--

DROP TABLE IF EXISTS `mms_trip_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_trip_room` (
  `triproomid` int NOT NULL COMMENT 'A unique identifier for the association between a trip and a specific room allocation. This ID links a particular room to a specific trip, allowing the tracking of room assignments for each trip. It is used to map rooms to the trips they are associated with, facilitating room reservations and occupancy management for each trip.',
  `roomnumber` int NOT NULL,
  `tripid` bigint NOT NULL,
  `roomsaleprice` decimal(8,2) NOT NULL COMMENT 'Room sale price for that particular trip',
  PRIMARY KEY (`triproomid`),
  KEY `mms_trip_room_mms_room_fk` (`roomnumber`),
  KEY `mms_trip_room_mms_trip_fk` (`tripid`),
  CONSTRAINT `mms_trip_room_mms_room_fk` FOREIGN KEY (`roomnumber`) REFERENCES `mms_room` (`roomnumber`),
  CONSTRAINT `mms_trip_room_mms_trip_fk` FOREIGN KEY (`tripid`) REFERENCES `mms_trip` (`tripid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_trip_room`
--

LOCK TABLES `mms_trip_room` WRITE;
/*!40000 ALTER TABLE `mms_trip_room` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_trip_room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token_blacklist_blacklistedtoken`
--

DROP TABLE IF EXISTS `token_blacklist_blacklistedtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_blacklistedtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `blacklisted_at` datetime(6) NOT NULL,
  `token_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_id` (`token_id`),
  CONSTRAINT `token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk` FOREIGN KEY (`token_id`) REFERENCES `token_blacklist_outstandingtoken` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_blacklistedtoken`
--

LOCK TABLES `token_blacklist_blacklistedtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token_blacklist_outstandingtoken`
--

DROP TABLE IF EXISTS `token_blacklist_outstandingtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_outstandingtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` int DEFAULT NULL,
  `jti` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq` (`jti`),
  KEY `token_blacklist_outs_user_id_83bc629a_fk_auth_user` (`user_id`),
  CONSTRAINT `token_blacklist_outs_user_id_83bc629a_fk_auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_outstandingtoken`
--

LOCK TABLES `token_blacklist_outstandingtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-25 21:32:30
