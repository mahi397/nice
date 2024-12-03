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
  `floor` smallint NOT NULL COMMENT 'Floor at which the activity or entertainment is located',
  `capacity` int NOT NULL COMMENT 'Capacity of the activity/ entertainment',
  `activity_description` varchar(45) NOT NULL COMMENT 'Description of the activity on board the ship.',
  PRIMARY KEY (`activityid`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_activity`
--

LOCK TABLES `mms_activity` WRITE;
/*!40000 ALTER TABLE `mms_activity` DISABLE KEYS */;
INSERT INTO `mms_activity` VALUES (1,'Entertainment','Theaters',8,190,'Unit 1 on Floor 8'),(2,'Entertainment','Theaters',10,56,'Unit 2 on Floor 10'),(3,'Entertainment','Casino',7,176,'Unit 1 on Floor 7'),(4,'Entertainment','Library',3,69,'Unit 1 on Floor 3'),(5,'Entertainment','Library',4,77,'Unit 2 on Floor 4'),(6,'Entertainment','Children Play',3,121,'Unit 1 on Floor 3'),(7,'Entertainment','Gym',5,85,'Unit 1 on Floor 5'),(8,'Entertainment','Outdoor Pool',11,197,'Unit 1 on Floor 11'),(9,'Entertainment','Indoor Pool',9,178,'Unit 1 on Floor 9'),(10,'Entertainment','Whirlpool',11,78,'Unit 1 on Floor 11'),(11,'Entertainment','Whirlpool',9,180,'Unit 2 on Floor 9'),(12,'Entertainment','Steam Room',9,149,'Unit 1 on Floor 9'),(13,'Entertainment','Sona Room',9,56,'Unit 1 on Floor 9'),(14,'Entertainment','Yoga Room',5,179,'Unit 1 on Floor 5'),(15,'Entertainment','Night Club',8,51,'Unit 1 on Floor 8'),(16,'Entertainment','Night Club',11,136,'Unit 2 on Floor 11'),(17,'Entertainment','Tennis Court',11,67,'Unit 1 on Floor 11');
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
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_activity_psngr`
--

LOCK TABLES `mms_activity_psngr` WRITE;
/*!40000 ALTER TABLE `mms_activity_psngr` DISABLE KEYS */;
INSERT INTO `mms_activity_psngr` VALUES (1,12,24),(2,14,17),(3,7,8),(4,2,24),(5,12,27),(6,8,15),(7,3,7),(8,13,3),(9,4,21),(10,14,1),(11,12,9),(12,7,2),(13,2,7),(14,16,28),(15,14,7),(16,13,29),(17,10,29),(18,2,21),(19,1,6),(20,14,11),(21,8,3),(22,3,19),(23,9,17),(24,7,8),(25,2,24),(26,11,26),(27,5,24),(28,2,4),(29,6,8),(30,5,17);
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
  UNIQUE KEY `bookingid_UNIQUE` (`bookingid`),
  KEY `mms_booking_mms_group_fk` (`groupid`),
  KEY `mms_booking_mms_trip_fk` (`tripid`),
  KEY `fk_auth_user_booking` (`userid`),
  CONSTRAINT `fk_auth_user_booking` FOREIGN KEY (`userid`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `mms_booking_mms_group_fk` FOREIGN KEY (`groupid`) REFERENCES `mms_group` (`groupid`),
  CONSTRAINT `mms_booking_mms_trip_fk` FOREIGN KEY (`tripid`) REFERENCES `mms_trip` (`tripid`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_booking`
--

LOCK TABLES `mms_booking` WRITE;
/*!40000 ALTER TABLE `mms_booking` DISABLE KEYS */;
INSERT INTO `mms_booking` VALUES (1,'2024-09-15 00:00:00','BOOKED',232.38,3,24,218),(2,'2025-01-20 00:00:00','UNAVAILABLE',708.38,7,25,576),(3,'2024-12-15 00:00:00','AVAILABLE',534.89,8,13,50),(4,'2024-07-05 00:00:00','UNAVAILABLE',772.44,1,1,73),(5,'2024-07-05 00:00:00','BOOKED',298.74,5,1,158),(6,'2024-07-05 00:00:00','UNAVAILABLE',918.80,6,1,913),(7,'2024-11-15 00:00:00','UNAVAILABLE',315.22,1,17,866),(8,'2024-07-05 00:00:00','AVAILABLE',776.14,5,1,48),(9,'2024-07-05 00:00:00','AVAILABLE',354.31,7,1,358),(10,'2025-04-01 00:00:00','BOOKED',399.13,9,16,298),(11,'2025-04-01 00:00:00','BOOKED',830.24,2,6,540),(12,'2024-07-05 00:00:00','UNAVAILABLE',956.91,2,1,648),(13,'2024-07-05 00:00:00','AVAILABLE',642.11,8,1,260),(14,'2024-07-05 00:00:00','UNAVAILABLE',206.87,7,1,759),(15,'2024-07-05 00:00:00','BOOKED',445.53,4,1,859),(16,'2025-04-10 00:00:00','AVAILABLE',931.02,3,26,526),(17,'2024-07-05 00:00:00','AVAILABLE',558.35,8,1,55),(18,'2024-07-05 00:00:00','AVAILABLE',441.86,6,1,977),(19,'2025-01-01 00:00:00','BOOKED',168.31,3,14,530),(20,'2025-06-05 00:00:00','AVAILABLE',164.69,1,10,607),(21,'2024-07-05 00:00:00','AVAILABLE',858.57,2,1,779),(22,'2024-07-05 00:00:00','BOOKED',642.70,3,1,334),(23,'2024-12-15 00:00:00','AVAILABLE',363.92,4,13,918),(24,'2024-12-15 00:00:00','AVAILABLE',386.91,10,13,785),(25,'2025-03-05 00:00:00','UNAVAILABLE',298.18,8,5,580),(26,'2025-02-10 00:00:00','AVAILABLE',892.92,1,9,294),(27,'2025-06-01 00:00:00','AVAILABLE',755.37,9,22,688),(28,'2024-07-05 00:00:00','UNAVAILABLE',789.47,9,1,754),(29,'2024-12-15 00:00:00','BOOKED',52.72,7,13,410),(30,'2024-07-05 00:00:00','AVAILABLE',874.13,5,1,51);
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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_group`
--

LOCK TABLES `mms_group` WRITE;
/*!40000 ALTER TABLE `mms_group` DISABLE KEYS */;
INSERT INTO `mms_group` VALUES (1,'Adventure Seekers'),(2,'Family Travelers'),(3,'Corporate Retreat'),(4,'Friends Getaway'),(5,'Romantic Escapades'),(6,'Solo Explorers'),(7,'Weekend Wanderers'),(8,'Nature Enthusiasts'),(9,'Cultural Tourists'),(10,'Luxury Cruisers');
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
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_invoice`
--

LOCK TABLES `mms_invoice` WRITE;
/*!40000 ALTER TABLE `mms_invoice` DISABLE KEYS */;
INSERT INTO `mms_invoice` VALUES (1,'2010-02-03 00:00:00',339.00,'unpaid','2023-09-18 00:00:00',5),(2,'2006-09-22 00:00:00',885.52,'paid','2003-01-09 00:00:00',12),(3,'2007-09-24 00:00:00',983.31,'unpaid','2024-02-22 00:00:00',19),(4,'2001-03-15 00:00:00',283.89,'unpaid','2021-06-08 00:00:00',1),(5,'2020-05-07 00:00:00',664.89,'paid','2012-11-14 00:00:00',22),(6,'2003-02-21 00:00:00',93.92,'paid','2021-05-15 00:00:00',8),(7,'2018-12-01 00:00:00',628.63,'unpaid','2002-02-15 00:00:00',17),(8,'2008-08-22 00:00:00',176.35,'unpaid','2001-04-10 00:00:00',30),(9,'2019-06-06 00:00:00',678.30,'paid','2008-03-01 00:00:00',14),(10,'2005-09-07 00:00:00',73.75,'unpaid','2020-11-17 00:00:00',9),(11,'2024-01-21 00:00:00',792.01,'paid','2022-03-29 00:00:00',25),(12,'2014-09-06 00:00:00',263.00,'unpaid','2012-09-13 00:00:00',2),(13,'2000-12-07 00:00:00',905.99,'unpaid','2001-08-06 00:00:00',28),(14,'2015-10-08 00:00:00',550.10,'paid','2020-09-11 00:00:00',7),(15,'2016-04-05 00:00:00',987.05,'unpaid','2019-10-09 00:00:00',18),(16,'2018-04-05 00:00:00',801.72,'paid','2002-11-28 00:00:00',11),(17,'2010-12-11 00:00:00',329.75,'unpaid','2018-11-30 00:00:00',20),(18,'2009-08-31 00:00:00',954.94,'paid','2023-09-09 00:00:00',3),(19,'2014-07-21 00:00:00',517.56,'unpaid','2001-01-11 00:00:00',16),(20,'2019-12-21 00:00:00',154.80,'paid','2019-03-21 00:00:00',27),(21,'2024-03-15 00:00:00',450.00,'paid','2024-04-14 00:00:00',6),(22,'2024-06-10 00:00:00',275.00,'unpaid','2024-07-10 00:00:00',24),(23,'2024-09-01 00:00:00',390.00,'paid','2024-10-01 00:00:00',13),(24,'2024-05-20 00:00:00',480.00,'unpaid','2024-06-19 00:00:00',10),(25,'2024-07-11 00:00:00',320.00,'paid','2024-08-10 00:00:00',29),(26,'2024-04-05 00:00:00',350.00,'unpaid','2024-05-05 00:00:00',4),(27,'2024-08-23 00:00:00',299.00,'paid','2024-09-22 00:00:00',15),(28,'2024-11-17 00:00:00',425.00,'unpaid','2024-12-16 00:00:00',21),(29,'2024-01-30 00:00:00',310.00,'paid','2024-02-29 00:00:00',23),(30,'2024-02-28 00:00:00',360.00,'unpaid','2024-03-29 00:00:00',26);
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_package`
--

LOCK TABLES `mms_package` WRITE;
/*!40000 ALTER TABLE `mms_package` DISABLE KEYS */;
INSERT INTO `mms_package` VALUES (1,'Water and Non-Alcoholic',40.00,'$40/person/night'),(2,'Unlimited Bar',80.00,'$80/person/night (for adults age over 21)'),(3,'Internet 200 minutes, 100 GB',150.00,'$150/person for entire trip'),(4,'Unlimited Internet',250.00,'$250/person for entire trip'),(5,'Specialty Dining',60.00,'$60/person/night (Italian, La-carte, Mexican, Japanese, Chinese)');
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
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_passenger`
--

LOCK TABLES `mms_passenger` WRITE;
/*!40000 ALTER TABLE `mms_passenger` DISABLE KEYS */;
INSERT INTO `mms_passenger` VALUES (1,'Sophia','Garcia','1985-03-15 00:00:00','F','1111111111','sophia.garcia@example.com','321 Harbor Ave','Miami','Florida','USA','33101','American','P9876543','Jane Garcia','2222222222',8),(2,'Emma','Johnson','1987-07-20 00:00:00','F','3333333333','emma.johnson@example.com','654 Ocean Dr','Los Angeles','California','USA','90001','American','P8765432','Mark Johnson','4444444444',10),(3,'Liam','Brown','1990-01-12 00:00:00','M','5555555555','liam.brown@example.com','789 Port Blvd','New York','New York','USA','10001','American','P7654321','Anna Brown','6666666666',6),(4,'Mia','Anderson','1992-05-09 00:00:00','F','7777777777','mia.anderson@example.com','456 Cruise Rd','Houston','Texas','USA','77001','American','P6543210','Emma Anderson','8888888888',7),(5,'Noah','Martinez','1995-11-23 00:00:00','M','9999999999','noah.martinez@example.com','123 Bay St','Chicago','Illinois','USA','60601','American','P5432109','Sophia Martinez','0000000000',7),(6,'Olivia','Taylor','1988-02-28 00:00:00','F','1010101010','olivia.taylor@example.com','567 Dock Ln','Miami','Florida','USA','33101','American','P4321098','James Taylor','1212121212',1),(7,'James','Smith','1993-06-15 00:00:00','M','1313131313','james.smith@example.com','890 Harbor Dr','Seattle','Washington','USA','98101','American','P3210987','Mia Smith','1414141414',10),(8,'Emma','Clark','1991-08-22 00:00:00','F','1515151515','emma.clark@example.com','112 Ocean Ave','Boston','Massachusetts','USA','02101','American','P2109876','Olivia Clark','1616161616',10),(9,'Benjamin','Garcia','1989-12-11 00:00:00','M','1717171717','benjamin.garcia@example.com','345 Coastal Rd','San Diego','California','USA','92101','American','P1098765','Sophia Garcia','1818181818',5),(10,'Amelia','Lee','1986-09-14 00:00:00','F','1919191919','amelia.lee@example.com','678 Shoreline Rd','Orlando','Florida','USA','32801','American','P0987654','Liam Lee','2020202020',9),(11,'Liam','Davis','1992-03-17 00:00:00','M','2121212121','liam.davis@example.com','987 Bay Rd','Austin','Texas','USA','73301','American','P8765431','Emma Davis','2323232323',6),(12,'Sophia','Anderson','1994-10-05 00:00:00','F','2424242424','sophia.anderson@example.com','223 Dockside Blvd','San Francisco','California','USA','94101','American','P7654320','Noah Anderson','2525252525',7),(13,'Olivia','Martinez','1997-12-29 00:00:00','F','2626262626','olivia.martinez@example.com','111 Seaside Dr','Las Vegas','Nevada','USA','89101','American','P6543219','Mia Martinez','2727272727',1),(14,'Noah','Garcia','1988-11-18 00:00:00','M','2828282828','noah.garcia@example.com','444 Harbor Way','Atlanta','Georgia','USA','30301','American','P5432108','Sophia Garcia','2929292929',7),(15,'James','Taylor','1990-06-25 00:00:00','M','3030303030','james.taylor@example.com','678 Pier Ave','Charlotte','North Carolina','USA','28201','American','P4321097','Olivia Taylor','3131313131',10),(16,'Emma','Smith','1993-08-16 00:00:00','F','3232323232','emma.smith@example.com','890 Beach Blvd','Phoenix','Arizona','USA','85001','American','P3210986','Benjamin Smith','3333333333',10),(17,'Mia','Clark','1995-01-12 00:00:00','F','3434343434','mia.clark@example.com','345 Oceanview Ln','Denver','Colorado','USA','80201','American','P2109875','Liam Clark','3535353535',4),(18,'Amelia','Davis','1991-05-30 00:00:00','F','3636363636','amelia.davis@example.com','111 Cruise Way','Dallas','Texas','USA','75201','American','P1098764','James Davis','3737373737',9),(19,'Benjamin','Lee','1989-04-22 00:00:00','M','3838383838','benjamin.lee@example.com','456 Harbor View','Seattle','Washington','USA','98101','American','P0987653','Amelia Lee','3939393939',5),(20,'Sophia','Brown','1992-07-14 00:00:00','F','4040404040','sophia.brown@example.com','789 Bayside Dr','Miami','Florida','USA','33101','American','P9876542','Liam Brown','4141414141',8),(21,'Liam','Johnson','1991-09-10 00:00:00','M','4242424242','liam.johnson@example.com','222 Dock Lane','Boston','Massachusetts','USA','02101','American','P8765432','Emma Johnson','4343434343',6),(22,'Olivia','Taylor','1987-03-15 00:00:00','F','4444444444','olivia.taylor@example.com','333 Sunset Blvd','Chicago','Illinois','USA','60601','American','P7654321','Sophia Taylor','4545454545',1),(23,'Benjamin','Martinez','1994-06-20 00:00:00','M','4646464646','benjamin.martinez@example.com','456 Horizon Rd','San Diego','California','USA','92101','American','P6543210','John Martinez','4747474747',5),(24,'Emma','Davis','1996-11-11 00:00:00','F','4848484848','emma.davis@example.com','789 Ocean Drive','Houston','Texas','USA','77001','American','P5432109','James Davis','4949494949',9),(25,'Mia','Brown','1990-12-25 00:00:00','F','5050505050','mia.brown@example.com','890 Pier Place','Orlando','Florida','USA','32801','American','P4321098','Benjamin Brown','5151515151',4),(26,'Sophia','Clark','1988-08-30 00:00:00','F','5252525252','sophia.clark@example.com','345 Seaside Ave','New Orleans','Louisiana','USA','70101','American','P3210987','Mia Clark','5353535353',8),(27,'Noah','Lee','1989-04-05 00:00:00','M','5454545454','noah.lee@example.com','123 Cruise Blvd','San Jose','California','USA','95101','American','P2109876','Emma Lee','5555555555',7),(28,'James','Garcia','1992-02-14 00:00:00','M','5656565656','james.garcia@example.com','678 Bayfront Dr','Portland','Oregon','USA','97201','American','P1098765','Olivia Garcia','5757575757',2),(29,'Amelia','Martinez','1993-05-01 00:00:00','F','5858585858','amelia.martinez@example.com','222 Horizon Way','Las Vegas','Nevada','USA','89101','American','P9876543','James Martinez','5959595959',9),(30,'Emma','Johnson','1989-07-24 00:00:00','F','6060606060','emma.johnson@example.com','555 Coastal Rd','Phoenix','Arizona','USA','85001','American','P8765434','Noah Johnson','6161616161',10);
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
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_payment_detail`
--

LOCK TABLES `mms_payment_detail` WRITE;
/*!40000 ALTER TABLE `mms_payment_detail` DISABLE KEYS */;
INSERT INTO `mms_payment_detail` VALUES (1,'2025-06-20 00:00:00',70.66,'visa','NICE847362901',12),(2,'2024-12-05 00:00:00',32.26,'mastercard','NICE935271468',5),(3,'2025-05-15 00:00:00',232.79,'Amex','NICE248736509',18),(4,'2025-05-15 00:00:00',383.26,'visa','NICE492813765',25),(5,'2024-12-05 00:00:00',193.54,'mastercard','NICE716493582',9),(6,'2024-12-05 00:00:00',456.66,'Amex','NICE365927418',27),(7,'2025-06-01 00:00:00',88.82,'mastercard','NICE504726193',3),(8,'2024-12-05 00:00:00',295.20,'Amex','NICE138594762',15),(9,'2024-12-05 00:00:00',251.21,'visa','NICE672819543',21),(10,'2024-12-05 00:00:00',71.13,'mastercard','NICE985137246',8),(11,'2025-07-10 00:00:00',759.48,'Amex','NICE234819765',30),(12,'2024-12-05 00:00:00',630.26,'visa','NICE478926153',6),(13,'2025-05-15 00:00:00',286.65,'mastercard','NICE593182467',22),(14,'2025-02-15 00:00:00',467.16,'Amex','NICE746592831',4),(15,'2025-09-10 00:00:00',479.13,'visa','NICE829435176',19),(16,'2025-08-05 00:00:00',367.01,'mastercard','NICE317659842',11),(17,'2025-09-01 00:00:00',99.45,'Amex','NICE914583726',24),(18,'2025-11-05 00:00:00',289.42,'visa','NICE682391457',17),(19,'2024-12-05 00:00:00',50.10,'mastercard','NICE456729813',1),(20,'2025-04-15 00:00:00',929.69,'Amex','NICE795634281',14),(21,'2025-05-15 00:00:00',404.86,'visa','NICE367248915',29),(22,'2024-12-05 00:00:00',846.68,'mastercard','NICE924816537',2),(23,'2024-12-05 00:00:00',321.96,'Amex','NICE581364792',23),(24,'2024-12-05 00:00:00',988.15,'visa','NICE193578426',7),(25,'2024-12-05 00:00:00',96.70,'mastercard','NICE826394517',28),(26,'2024-12-05 00:00:00',81.61,'Amex','NICE492176835',13),(27,'2024-12-05 00:00:00',676.73,'visa','NICE157863429',26),(28,'2024-12-05 00:00:00',382.72,'mastercard','NICE319524768',10),(29,'2025-11-01 00:00:00',579.24,'Amex','NICE873195246',20),(30,'2025-09-01 00:00:00',500.75,'Visa','NICE621487935',16);
/*!40000 ALTER TABLE `mms_payment_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_port`
--

DROP TABLE IF EXISTS `mms_port`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_port` (
  `portid` int NOT NULL AUTO_INCREMENT COMMENT 'Primary key for the port entity. Unique identifier for each port.',
  `portname` varchar(100) NOT NULL COMMENT 'The name of the port where the cruise either stops during the itinerary or starts/ends the trip. This attribute identifies specific locations included in the trip.',
  `address` varchar(50) NOT NULL COMMENT 'Street address where the port is located. ',
  `portcity` varchar(50) NOT NULL COMMENT 'Name of the country where the port is located. Useful for regional sorting and queries.',
  `portstate` varchar(50) NOT NULL COMMENT 'Name of the state (if applicable) where the port is located. Adds further location specificity.',
  `portcountry` varchar(50) NOT NULL COMMENT 'Name of the city where the port is located. Useful for detailed geographical reference.',
  `nearestairport` varchar(100) NOT NULL COMMENT 'Name of the nearest airport to the port',
  `parkingspots` int NOT NULL COMMENT 'Number of parking spots available at the port',
  PRIMARY KEY (`portid`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_port`
--

LOCK TABLES `mms_port` WRITE;
/*!40000 ALTER TABLE `mms_port` DISABLE KEYS */;
INSERT INTO `mms_port` VALUES (1,'Port of Miami','123 Port Address','Miami','Florida','USA','MIA',480),(2,'Port of Los Angeles','123 Port Address','Los Angeles','California','USA','LAX',465),(3,'Port of Rotterdam','123 Port Address','Rotterdam','South Holland','Netherlands','RTM',364),(4,'Port of Singapore','123 Port Address','Singapore','Central Region','Singapore','SIN',452),(5,'Port of Dubai','123 Port Address','Dubai','Dubai','UAE','DXB',193),(6,'Port of Sydney','456 Port Address','Sydney','New South Wales','Australia','SYD',320),(7,'Port of Tokyo','789 Port Address','Tokyo','Tokyo Prefecture','Japan','HND',275),(8,'Port of Cape Town','101 Port Address','Cape Town','Western Cape','South Africa','CPT',215),(9,'Port of Vancouver','202 Port Address','Vancouver','British Columbia','Canada','YVR',400),(10,'Port of Rio de Janeiro','303 Port Address','Rio de Janeiro','Rio de Janeiro','Brazil','GIG',290),(11,'Port of Hamburg','404 Port Address','Hamburg','Hamburg','Germany','HAM',310),(12,'Port of Shanghai','505 Port Address','Shanghai','Shanghai','China','PVG',500),(13,'Port of New York','606 Port Address','New York','New York','USA','JFK',380),(14,'Port of Athens','707 Port Address','Athens','Attica','Greece','ATH',250);
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
  `departuretime` datetime DEFAULT NULL COMMENT 'Time of departure from the port',
  `arrivaltime` datetime DEFAULT NULL COMMENT 'Time at which the ship arrives at the port',
  `orderofstop` smallint NOT NULL COMMENT 'The order in which the ship stops at each port',
  `isstartport` char(1) NOT NULL COMMENT 'Indicates if the port is starting point of the trip',
  `isendport` char(1) NOT NULL COMMENT 'Indicates if the port is ending point of the trip',
  PRIMARY KEY (`itineraryid`),
  KEY `mms_port_stop_mms_port_fk` (`portid`),
  KEY `mms_port_stop_mms_trip_fk` (`tripid`),
  CONSTRAINT `mms_port_stop_mms_port_fk` FOREIGN KEY (`portid`) REFERENCES `mms_port` (`portid`),
  CONSTRAINT `mms_port_stop_mms_trip_fk` FOREIGN KEY (`tripid`) REFERENCES `mms_trip` (`tripid`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_port_stop`
--

LOCK TABLES `mms_port_stop` WRITE;
/*!40000 ALTER TABLE `mms_port_stop` DISABLE KEYS */;
INSERT INTO `mms_port_stop` VALUES (1,3,17,'2025-12-10 00:00:00','2025-12-07 00:00:00',2,'N','N'),(2,6,29,'2025-01-12 00:00:00','2025-01-12 00:00:00',5,'N','N'),(3,8,5,'2025-03-30 00:00:00','2025-03-21 00:00:00',3,'N','N'),(4,2,12,'2025-11-18 00:00:00','2025-11-12 00:00:00',8,'N','N'),(5,5,21,'2025-06-12 00:00:00','2025-06-09 00:00:00',1,'N','N'),(6,7,8,'2025-07-21 00:00:00','2025-07-16 00:00:00',9,'N','N'),(7,4,19,'2025-05-03 00:00:00','2025-04-25 00:00:00',4,'N','N'),(8,9,4,'2025-02-03 00:00:00','2025-02-03 00:00:00',7,'N','N'),(9,1,14,'2025-12-14 00:00:00','2025-12-09 00:00:00',6,'N','N'),(10,10,25,'2026-01-01 00:00:00','2025-12-30 00:00:00',10,'N','N'),(11,3,11,'2025-07-01 00:00:00','2025-06-26 00:00:00',4,'N','N'),(12,8,30,'2025-04-06 00:00:00','2025-03-31 00:00:00',7,'N','N'),(13,6,13,'2025-05-04 00:00:00','2025-04-27 00:00:00',2,'N','N'),(14,2,24,'2025-11-11 00:00:00','2025-11-02 00:00:00',6,'N','N'),(15,7,7,'2025-01-11 00:00:00','2025-01-08 00:00:00',3,'N','N'),(16,4,15,'2025-11-11 00:00:00','2025-11-10 00:00:00',8,'N','N'),(17,1,28,'2025-03-03 00:00:00','2025-02-28 00:00:00',5,'N','N'),(18,5,20,'2025-04-26 00:00:00','2025-04-22 00:00:00',9,'N','N'),(19,9,2,'2025-05-25 00:00:00','2025-05-20 00:00:00',10,'N','N'),(20,10,9,'2025-07-07 00:00:00','2025-06-29 00:00:00',1,'N','N'),(21,6,18,'2025-12-07 00:00:00','2025-11-28 00:00:00',7,'N','N'),(22,2,3,'2025-10-31 00:00:00','2025-10-28 00:00:00',4,'N','N'),(23,7,16,'2025-06-19 00:00:00','2025-06-18 00:00:00',8,'N','N'),(24,9,23,'2025-05-18 00:00:00','2025-05-15 00:00:00',3,'N','N'),(25,3,6,'2025-11-01 00:00:00','2025-11-01 00:00:00',5,'N','N'),(26,5,13,'2025-07-27 00:00:00','2025-07-20 00:00:00',2,'N','N'),(27,10,26,'2025-12-02 00:00:00','2025-11-28 00:00:00',6,'N','N'),(28,8,14,'2025-05-05 00:00:00','2025-05-01 00:00:00',1,'N','N'),(29,4,29,'2025-02-09 00:00:00','2025-02-07 00:00:00',9,'N','N'),(30,1,10,'2025-12-24 00:00:00','2025-12-23 00:00:00',8,'N','N'),(31,2,28,'2025-08-27 00:00:00','2025-08-19 00:00:00',3,'N','N'),(32,8,20,'2025-03-13 00:00:00','2025-03-09 00:00:00',7,'N','N'),(33,6,19,'2025-11-16 00:00:00','2025-11-08 00:00:00',5,'N','N'),(34,3,27,'2025-07-30 00:00:00','2025-07-27 00:00:00',4,'N','N'),(35,4,9,'2025-02-15 00:00:00','2025-02-11 00:00:00',2,'N','N');
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
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_psngr_package`
--

LOCK TABLES `mms_psngr_package` WRITE;
/*!40000 ALTER TABLE `mms_psngr_package` DISABLE KEYS */;
INSERT INTO `mms_psngr_package` VALUES (1,1,25,428.97),(2,4,15,783.42),(3,2,5,372.39),(4,3,19,52.38),(5,1,23,634.92),(6,5,18,129.87),(7,3,12,738.54),(8,4,11,428.69),(9,2,28,847.23),(10,5,29,368.47),(11,1,14,802.56),(12,4,6,470.13),(13,2,30,928.89),(14,3,3,300.99),(15,1,24,621.49),(16,5,16,782.46),(17,2,2,534.92),(18,3,10,932.34),(19,1,20,529.65),(20,4,22,782.31),(21,5,17,829.12),(22,2,21,872.56),(23,3,9,348.29),(24,4,7,672.38),(25,5,1,583.19),(26,1,8,700.59),(27,2,4,834.11),(28,3,13,920.42),(29,4,27,456.38),(30,5,26,830.59);
/*!40000 ALTER TABLE `mms_psngr_package` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_restaurant`
--

DROP TABLE IF EXISTS `mms_restaurant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_restaurant` (
  `restaurantid` smallint NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for each restaurant',
  `restaurantname` varchar(50) NOT NULL COMMENT 'Name of the resturant',
  `floornumber` smallint NOT NULL COMMENT 'Floor where the restaurant is located in the ship',
  `openingtime` time DEFAULT NULL COMMENT 'Time at which the restaurant opens',
  `closingtime` time DEFAULT NULL COMMENT 'Time at which the restaurant closes',
  `servesbreakfast` char(1) NOT NULL COMMENT 'Value to specify if the restaurant serves breakfast or not. For e.g., ''Y'' for yes and ''N'' for no',
  `serveslunch` char(1) NOT NULL COMMENT 'Value to specify if the restaurant serves lunch or not. For e.g., ''Y'' for yes and ''N'' for no',
  `servesdinner` char(1) NOT NULL COMMENT 'Value to specify if the restaurant serves dinner or not. For e.g., ''Y'' for yes and ''N'' for no',
  `servesalcohol` char(1) NOT NULL COMMENT 'Value to specify if the restaurant serves alcohol or not. For e.g., ''Y'' for yes and ''N'' for no',
  `resturant_description` mediumtext NOT NULL COMMENT 'Description of the cuisine served with the restaurant.',
  PRIMARY KEY (`restaurantid`),
  UNIQUE KEY `restaurantid_UNIQUE` (`restaurantid`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_restaurant`
--

LOCK TABLES `mms_restaurant` WRITE;
/*!40000 ALTER TABLE `mms_restaurant` DISABLE KEYS */;
INSERT INTO `mms_restaurant` VALUES (1,'Common Buffett',6,'07:00:00','21:00:00','Y','Y','Y','N','Serves Breakfast, Lunch, and Dinner.'),(2,'Italian Specialty',8,'18:00:00','22:00:00','N','N','Y','N','Serves Dinner only.'),(3,'Mexican Specialty',7,'18:00:00','22:00:00','N','N','Y','N','Serves Dinner only.'),(4,'La-carte continental',6,'12:00:00','20:00:00','N','Y','Y','N','Serves Lunch and Dinner.'),(5,'Tokyo Ramen Japanese',5,'12:00:00','20:00:00','N','Y','Y','N','Serves Lunch and Dinner.'),(6,'Ming Wok Chinese',5,'12:00:00','20:00:00','N','Y','Y','N','Serves Lunch and Dinner.'),(7,'Round Clock Café',10,'00:00:00','23:59:59','Y','Y','Y','N','Serves beverages and light food, open 24 hours.'),(8,'Pool Bar',10,'10:00:00','22:00:00','N','N','N','Y','Serves alcoholic beverages.'),(9,'Stout Bar',7,'10:00:00','22:00:00','N','N','N','Y','Serves alcoholic beverages.');
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
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_restaurant_psngr`
--

LOCK TABLES `mms_restaurant_psngr` WRITE;
/*!40000 ALTER TABLE `mms_restaurant_psngr` DISABLE KEYS */;
INSERT INTO `mms_restaurant_psngr` VALUES (1,2,15),(2,4,7),(3,7,22),(4,9,18),(5,3,27),(6,8,3),(7,6,12),(8,5,25),(9,1,30),(10,2,9),(11,4,21),(12,9,17),(13,8,14),(14,3,5),(15,6,19),(16,7,1),(17,5,8),(18,2,13),(19,4,20),(20,9,29),(21,8,10),(22,3,6),(23,6,24),(24,7,4),(25,5,23),(26,2,11),(27,4,28),(28,9,16),(29,8,26),(30,3,2);
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
INSERT INTO `mms_room` VALUES (1,3,425.38,1,1),(2,3,816.29,2,1),(3,3,891.41,3,1),(4,3,490.04,4,1),(5,3,677.33,5,1),(6,3,765.57,6,2),(7,3,763.32,7,2),(8,3,320.94,1,2),(9,3,883.40,2,2),(10,3,876.85,3,2),(11,4,564.62,4,3),(12,4,940.77,5,3),(13,4,23.12,6,3),(14,4,699.49,7,3),(15,4,520.09,1,3),(16,4,948.08,2,4),(17,4,358.41,3,4),(18,4,363.81,4,4),(19,4,47.28,5,4),(20,5,579.44,6,4),(21,5,601.55,7,1),(22,5,679.66,4,1),(23,5,887.47,4,2),(24,5,324.99,5,2),(25,6,886.30,5,3),(26,6,334.15,6,3),(27,6,141.90,6,3),(28,6,991.34,7,4),(29,6,808.92,7,4),(30,6,799.44,7,4);
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
INSERT INTO `mms_room_loc` VALUES (1,'Bow (Forward)'),(2,'Stern (Aft)'),(3,'Port Side (Left)'),(4,'Starboard Side (Right)');
/*!40000 ALTER TABLE `mms_room_loc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_room_type`
--

DROP TABLE IF EXISTS `mms_room_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_room_type` (
  `stateroomtypeid` smallint NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier of room type',
  `stateroomtype` varchar(20) NOT NULL COMMENT 'Name of the stateroom type',
  `roomsize` bigint NOT NULL COMMENT 'Size of the stateroom in SQFT',
  `numberofbeds` smallint NOT NULL COMMENT 'Number of beds in the room',
  `numberofbaths` decimal(2,1) NOT NULL COMMENT 'Number of the bathrooms in the stateroom',
  `numberofbalconies` smallint NOT NULL COMMENT 'Number of balconies in the stateroom',
  PRIMARY KEY (`stateroomtypeid`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_room_type`
--

LOCK TABLES `mms_room_type` WRITE;
/*!40000 ALTER TABLE `mms_room_type` DISABLE KEYS */;
INSERT INTO `mms_room_type` VALUES (1,'The Haven Suite',1000,6,3.0,2),(2,'Club Balcony Suite',800,4,2.0,2),(3,'Family Large Balcony',600,4,2.0,1),(4,'Family Balcony',400,4,1.5,1),(5,'Oceanview Window',300,2,1.0,0),(6,'Inside Stateroom',200,2,1.0,0),(7,'Studio Stateroom',150,1,1.0,0);
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
  `trip_cancellation` varchar(255) DEFAULT NULL,
  `trip_capacity` int NOT NULL COMMENT 'Total passenger capacity for the cruise liner.',
  `trip_description` text NOT NULL COMMENT 'Description of the trip booked.',
  `final_booking` date NOT NULL,
  PRIMARY KEY (`tripid`)
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_trip`
--

LOCK TABLES `mms_trip` WRITE;
/*!40000 ALTER TABLE `mms_trip` DISABLE KEYS */;
INSERT INTO `mms_trip` VALUES (1,'Caribbean Adventure Cruise','2025-01-05 00:00:00','2025-01-12 00:00:00',1200.00,'ON-TIME',NULL,655,'A 7-day cruise exploring the beautiful Caribbean islands.','2024-12-29'),(2,'Mediterranean Escape','2025-03-10 00:00:00','2025-03-17 00:00:00',1800.00,'PENDING','N/A',734,'A luxurious 10-day journey through the Mediterranean Sea.','2025-03-03'),(3,'Alaskan Glacier Voyage','2025-06-15 00:00:00','2025-06-19 00:00:00',1400.00,'PENDING','N/A',703,'Experience the stunning glaciers of Alaska on this 7-day voyage.','2025-06-08'),(4,'Asian Treasures Cruise','2025-07-01 00:00:00','2025-07-10 00:00:00',2000.00,'ON-TIME',NULL,817,'Explore the cultural and natural treasures of Asia on this 10-day cruise.','2025-06-24'),(5,'European River Journey','2025-09-05 00:00:00','2025-09-13 00:00:00',1600.00,'ON-TIME',NULL,973,'Sail through the heart of Europe on this scenic 10-day river cruise.','2025-08-29'),(6,'South Pacific Explorer','2025-10-01 00:00:00','2025-10-10 00:00:00',2200.00,'CANCELLED','Cancelled due to unforeseen circumstances',918,'Discover the beauty of the South Pacific on this 10-day adventure.','2025-09-24'),(7,'Baltic Capitals Cruise','2025-05-15 00:00:00','2025-05-21 00:00:00',1900.00,'PENDING','N/A',670,'Visit the vibrant capitals of the Baltic region on this 10-day cruise.','2025-05-08'),(8,'Panama Canal Voyage','2025-11-20 00:00:00','2025-11-24 00:00:00',2100.00,'CANCELLED','Cancelled due to unforeseen circumstances',599,'Transit the iconic Panama Canal on this 10-day voyage.','2025-11-13'),(9,'Hawaiian Island Hopper','2025-08-10 00:00:00','2025-08-14 00:00:00',2500.00,'CANCELLED',NULL,982,'Hop between the beautiful islands of Hawaii on this 10-day journey.','2025-08-03'),(10,'Galapagos Expedition','2025-12-05 00:00:00','2025-12-12 00:00:00',3000.00,'ON-TIME',NULL,616,'Experience the unique wildlife of the Galapagos Islands on this 10-day expedition.','2025-11-28'),(11,'Caribbean Adventure Cruise','2025-01-05 00:00:00','2025-01-10 00:00:00',1200.00,'ON-TIME',NULL,632,'A 7-day cruise exploring the beautiful Caribbean islands.','2024-12-29'),(12,'Mediterranean Escape','2025-03-10 00:00:00','2025-03-16 00:00:00',1800.00,'CANCELLED','Cancelled due to unforeseen circumstances',811,'A luxurious 10-day journey through the Mediterranean Sea.','2025-03-03'),(13,'Alaskan Glacier Voyage','2025-06-15 00:00:00','2025-06-19 00:00:00',1400.00,'ON-TIME','N/A',663,'Experience the stunning glaciers of Alaska on this 7-day voyage.','2025-06-08'),(14,'Asian Treasures Cruise','2025-07-01 00:00:00','2025-07-08 00:00:00',2000.00,'ON-TIME',NULL,883,'Explore the cultural and natural treasures of Asia on this 10-day cruise.','2025-06-24'),(15,'European River Journey','2025-09-05 00:00:00','2025-09-10 00:00:00',1600.00,'ON-TIME','N/A',927,'Sail through the heart of Europe on this scenic 10-day river cruise.','2025-08-29'),(16,'South Pacific Explorer','2025-10-01 00:00:00','2025-10-09 00:00:00',2200.00,'ON-TIME','Cancelled due to unforeseen circumstances',986,'Discover the beauty of the South Pacific on this 10-day adventure.','2025-09-24'),(17,'Baltic Capitals Cruise','2025-05-15 00:00:00','2025-05-22 00:00:00',1900.00,'CANCELLED','Cancelled due to unforeseen circumstances',649,'Visit the vibrant capitals of the Baltic region on this 10-day cruise.','2025-05-08'),(18,'Panama Canal Voyage','2025-11-20 00:00:00','2025-11-26 00:00:00',2100.00,'CANCELLED','Cancelled due to unforeseen circumstances',787,'Transit the iconic Panama Canal on this 10-day voyage.','2025-11-13'),(19,'Hawaiian Island Hopper','2025-08-10 00:00:00','2025-08-15 00:00:00',2500.00,'PENDING','N/A',989,'Hop between the beautiful islands of Hawaii on this 10-day journey.','2025-08-03'),(20,'Galapagos Expedition','2025-12-05 00:00:00','2025-12-11 00:00:00',3000.00,'ON-TIME',NULL,583,'Experience the unique wildlife of the Galapagos Islands on this 10-day expedition.','2025-11-28'),(21,'Amazon River Adventure','2025-09-15 00:00:00','2025-09-20 00:00:00',2800.00,'ON-TIME',NULL,949,'Cruise through the heart of the Amazon rainforest on this 10-day adventure.','2025-09-08'),(22,'Antarctic Expedition','2025-12-01 00:00:00','2025-12-05 00:00:00',5000.00,'ON-TIME',NULL,999,'Explore the pristine landscapes of Antarctica on this exclusive 15-day expedition.','2025-11-24'),(23,'Norwegian Fjords Cruise','2025-06-01 00:00:00','2025-06-07 00:00:00',2600.00,'PENDING','N/A',645,'Experience the dramatic beauty of Norway’s fjords on this 10-day cruise.','2025-05-25'),(24,'Great Barrier Reef Adventure','2025-03-15 00:00:00','2025-03-24 00:00:00',2400.00,'ON-TIME',NULL,730,'Explore the wonders of the Great Barrier Reef on this 10-day journey.','2025-03-08'),(25,'Eastern Mediterranean Odyssey','2025-07-20 00:00:00','2025-07-29 00:00:00',2000.00,'PENDING','N/A',717,'Sail the historic waters of the Eastern Mediterranean on this 10-day cruise.','2025-07-13'),(26,'Canadian Maritimes Cruise','2025-10-10 00:00:00','2025-10-19 00:00:00',1800.00,'PENDING','N/A',895,'Explore the picturesque Canadian Maritimes on this 10-day cruise.','2025-10-03'),(27,'Japanese Cherry Blossom Cruise','2025-04-01 00:00:00','2025-04-06 00:00:00',3000.00,'CANCELLED','N/A',824,'Witness the beauty of Japan’s cherry blossoms on this 10-day cruise.','2025-03-25'),(28,'South Africa Coastal Cruise','2025-02-01 00:00:00','2025-02-06 00:00:00',2600.00,'PENDING','N/A',935,'Discover the stunning coastlines of South Africa on this 10-day cruise.','2025-01-25'),(29,'Transatlantic Crossing','2025-11-01 00:00:00','2025-11-05 00:00:00',1700.00,'CANCELLED','Cancelled due to unforeseen circumstances',704,'Sail across the Atlantic on this classic 15-day voyage.','2025-10-25'),(30,'Greek Island Hopper','2025-05-05 00:00:00','2025-05-12 00:00:00',2200.00,'ON-TIME',NULL,715,'Visit the beautiful Greek islands on this 10-day cruise.','2025-04-28');
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
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_trip_activity`
--

LOCK TABLES `mms_trip_activity` WRITE;
/*!40000 ALTER TABLE `mms_trip_activity` DISABLE KEYS */;
INSERT INTO `mms_trip_activity` VALUES (1,20,17),(2,11,15),(3,12,10),(4,11,3),(5,30,17),(6,29,10),(7,22,3),(8,10,8),(9,1,7),(10,2,8),(11,3,9),(12,4,17),(13,7,11),(14,4,10),(15,9,7),(16,8,3),(17,23,1),(18,28,1),(19,7,3),(20,26,4),(21,10,7),(22,17,9),(23,15,10),(24,16,4),(25,22,17),(26,27,13),(27,29,12),(28,30,13),(29,11,10),(30,9,8);
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
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_trip_restaurant`
--

LOCK TABLES `mms_trip_restaurant` WRITE;
/*!40000 ALTER TABLE `mms_trip_restaurant` DISABLE KEYS */;
INSERT INTO `mms_trip_restaurant` VALUES (1,5,3),(2,19,7),(3,8,2),(4,12,5),(5,23,1),(6,15,6),(7,27,4),(8,9,9),(9,30,8),(10,14,3),(11,22,7),(12,3,2),(13,11,1),(14,6,5),(15,28,6),(16,17,9),(17,2,4),(18,25,8),(19,1,3),(20,18,7),(21,4,5),(22,13,2),(23,24,1),(24,10,6),(25,21,9),(26,26,8),(27,7,4),(28,16,3),(29,20,7);
/*!40000 ALTER TABLE `mms_trip_restaurant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_trip_room`
--

DROP TABLE IF EXISTS `mms_trip_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_trip_room` (
  `triproomid` int NOT NULL AUTO_INCREMENT COMMENT 'A unique identifier for the association between a trip and a specific room allocation. This ID links a particular room to a specific trip, allowing the tracking of room assignments for each trip. It is used to map rooms to the trips they are associated with, facilitating room reservations and occupancy management for each trip.',
  `roomnumber` int NOT NULL,
  `tripid` bigint NOT NULL,
  `roomsaleprice` decimal(8,2) NOT NULL COMMENT 'Room sale price for that particular trip',
  PRIMARY KEY (`triproomid`),
  UNIQUE KEY `triproomid_UNIQUE` (`triproomid`),
  KEY `mms_trip_room_mms_room_fk` (`roomnumber`),
  KEY `mms_trip_room_mms_trip_fk` (`tripid`),
  CONSTRAINT `mms_trip_room_mms_room_fk` FOREIGN KEY (`roomnumber`) REFERENCES `mms_room` (`roomnumber`),
  CONSTRAINT `mms_trip_room_mms_trip_fk` FOREIGN KEY (`tripid`) REFERENCES `mms_trip` (`tripid`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_trip_room`
--

LOCK TABLES `mms_trip_room` WRITE;
/*!40000 ALTER TABLE `mms_trip_room` DISABLE KEYS */;
INSERT INTO `mms_trip_room` VALUES (1,23,7,806.68),(2,9,28,526.55),(3,11,5,761.48),(4,19,18,968.12),(5,1,14,462.70),(6,27,2,892.76),(7,16,22,701.84),(8,15,8,252.65),(9,3,30,595.61),(10,28,4,552.62),(11,10,6,224.08),(12,20,13,979.16),(13,30,24,248.57),(14,12,9,113.18),(15,5,16,918.44),(16,7,1,716.83),(17,25,27,926.12),(18,14,23,334.52),(19,4,17,520.40),(20,29,25,618.52),(21,6,3,326.02),(22,8,19,423.38),(23,13,10,648.91),(24,18,26,14.34),(25,26,12,764.54),(26,2,20,10.26),(27,22,11,806.49),(28,21,21,452.36),(29,17,15,519.51),(30,24,29,303.73);
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

-- Dump completed on 2024-12-03 18:05:38
