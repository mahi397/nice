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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
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
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8mb3;
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
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
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb3;
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
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb3;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
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
  `activitytype` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Type of the activity',
  `activityname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Name of the activity	',
  `activitydescription` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Description of the activity on board the ship.',
  `floor` smallint NOT NULL COMMENT 'Floor at which the activity or entertainment is located',
  `capacity` int NOT NULL COMMENT 'Capacity of the activity/ entertainment',
  PRIMARY KEY (`activityid`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_activity`
--

LOCK TABLES `mms_activity` WRITE;
/*!40000 ALTER TABLE `mms_activity` DISABLE KEYS */;
INSERT INTO `mms_activity` VALUES (1,'Entertainment','Theaters','A spacious theater offering live performances, movies, and entertainment shows.',8,190),(2,'Entertainment','Theaters','An intimate theater experience for small audience screenings and niche performances.',10,56),(3,'Entertainment','Casino','A vibrant casino featuring slot machines, poker tables, and other gaming attractions.',7,176),(4,'Entertainment','Library','A quiet library with a diverse collection of books and comfortable reading spaces.',3,69),(5,'Entertainment','Library','A smaller library with an emphasis on travel guides and leisure reading.',4,77),(6,'Entertainment','Children Play','A fun-filled play area with games, activities, and toys for children.',3,121),(7,'Entertainment','Gym','A fully-equipped gym with cardio machines, weights, and fitness classes.',5,85),(8,'Entertainment','Outdoor Pool','A large outdoor pool with lounge chairs and a poolside bar.',11,197),(9,'Entertainment','Indoor Pool','An indoor pool with a climate-controlled environment and a jacuzzi.',9,178),(10,'Entertainment','Whirlpool','A relaxing whirlpool with hydrotherapy jets for rejuvenation.',11,78),(11,'Entertainment','Whirlpool','A secondary whirlpool offering a serene experience for passengers.',9,180),(12,'Entertainment','Steam Room','A steam room designed for relaxation and skin rejuvenation.',9,149),(13,'Entertainment','Sona Room','A traditional sauna room for detoxification and relaxation.',9,56),(14,'Entertainment','Yoga Room','A peaceful yoga studio offering guided sessions for all skill levels.',5,179),(15,'Entertainment','Night Club','An energetic night club with live DJs, dancing, and cocktails.',8,51),(16,'Entertainment','Night Club','A larger night club featuring themed nights and special events.',11,136),(17,'Entertainment','Tennis Court','An open-air tennis court for recreational and competitive matches.',11,67);
/*!40000 ALTER TABLE `mms_activity` ENABLE KEYS */;
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
  `bookingstatus` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Status of the booking, e.g., "Confirmed," "Pending," "Canceled." Assists with management tracking.',
  `groupid` bigint NOT NULL COMMENT 'Unqiue identifier for every group',
  `tripid` bigint NOT NULL COMMENT 'Primary key for each trip. Unique identifier for each trip entry.',
  `userid` int NOT NULL,
  PRIMARY KEY (`bookingid`),
  KEY `mms_booking_mms_group_fk` (`groupid`),
  KEY `mms_booking_mms_trip_fk` (`tripid`),
  KEY `mms_booking_mms_user_fk_idx` (`userid`),
  CONSTRAINT `mms_booking_mms_group_fk` FOREIGN KEY (`groupid`) REFERENCES `mms_group` (`groupid`),
  CONSTRAINT `mms_booking_mms_trip_fk` FOREIGN KEY (`tripid`) REFERENCES `mms_trip` (`tripid`),
  CONSTRAINT `mms_booking_mms_user_fk` FOREIGN KEY (`userid`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_booking`
--

LOCK TABLES `mms_booking` WRITE;
/*!40000 ALTER TABLE `mms_booking` DISABLE KEYS */;
INSERT INTO `mms_booking` VALUES (1,'2024-01-08 10:00:00','Confirmed',3,1,21),(2,'2024-02-15 14:30:00','Pending',1,2,12),(3,'2024-03-12 09:45:00','Confirmed',4,3,29),(4,'2024-04-25 16:20:00','Canceled',2,4,7),(5,'2024-05-08 11:00:00','Confirmed',8,5,19),(6,'2024-06-14 18:30:00','Confirmed',10,6,9),(7,'2024-07-10 08:45:00','Pending',7,7,23),(8,'2024-08-02 20:15:00','Confirmed',9,8,6),(9,'2024-09-18 15:00:00','Confirmed',5,9,27),(10,'2024-10-05 13:00:00','Pending',6,10,10),(11,'2024-11-30 17:10:00','Confirmed',2,11,15),(12,'2024-12-20 12:00:00','Canceled',1,12,18),(13,'2025-01-11 09:15:00','Confirmed',10,13,26),(14,'2025-02-14 19:45:00','Pending',4,14,2),(15,'2025-03-07 16:00:00','Confirmed',8,15,25),(16,'2025-04-18 10:30:00','Confirmed',3,16,1),(17,'2025-05-25 14:20:00','Confirmed',6,17,28),(18,'2025-06-09 11:45:00','Pending',9,18,13),(19,'2025-07-10 17:30:00','Confirmed',5,19,11),(20,'2025-08-01 13:10:00','Confirmed',7,20,20),(21,'2025-09-14 08:50:00','Pending',10,21,4),(22,'2025-10-27 19:00:00','Confirmed',1,22,16),(23,'2025-11-24 09:00:00','Canceled',8,23,30),(24,'2025-12-14 21:15:00','Confirmed',4,24,8),(25,'2025-12-20 11:25:00','Pending',6,25,3),(26,'2025-12-31 23:59:00','Confirmed',9,26,5),(27,'2025-12-25 19:45:00','Confirmed',3,27,22),(28,'2025-12-29 13:10:00','Pending',5,28,17),(29,'2025-12-30 10:30:00','Confirmed',2,29,24),(30,'2025-12-31 21:15:00','Canceled',7,30,14);
/*!40000 ALTER TABLE `mms_booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_booking_package`
--

DROP TABLE IF EXISTS `mms_booking_package`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_booking_package` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bookingid` bigint NOT NULL,
  `packageid` smallint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `mms_booking_package_booking_fk_idx` (`bookingid`),
  KEY `mms_booking_package_mms_package_fk_idx` (`packageid`),
  CONSTRAINT `mms_booking_package_mms_booking_fk` FOREIGN KEY (`bookingid`) REFERENCES `mms_booking` (`bookingid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `mms_booking_package_mms_package_fk` FOREIGN KEY (`packageid`) REFERENCES `mms_package` (`packageid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_booking_package`
--

LOCK TABLES `mms_booking_package` WRITE;
/*!40000 ALTER TABLE `mms_booking_package` DISABLE KEYS */;
INSERT INTO `mms_booking_package` VALUES (1,1,101),(2,2,2),(3,3,3),(4,4,4),(5,5,5),(6,6,5),(7,7,5),(8,8,3),(9,9,2),(10,10,5),(11,11,4),(12,12,1),(13,13,2),(14,14,4),(15,15,1),(16,16,1),(17,17,3),(18,18,4),(19,19,1),(20,20,4),(21,21,4),(22,22,5),(23,23,1),(24,24,4),(25,25,5),(26,26,2),(27,27,3),(28,28,5),(29,29,5),(30,30,5);
/*!40000 ALTER TABLE `mms_booking_package` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_group`
--

DROP TABLE IF EXISTS `mms_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_group` (
  `groupid` bigint NOT NULL AUTO_INCREMENT COMMENT 'Unqiue identifier for every group',
  `groupname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Name of the group',
  `count` int NOT NULL,
  PRIMARY KEY (`groupid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_group`
--

LOCK TABLES `mms_group` WRITE;
/*!40000 ALTER TABLE `mms_group` DISABLE KEYS */;
INSERT INTO `mms_group` VALUES (1,'Adventure Enthusiasts',120),(2,'Family Travelers',110),(3,'Corporate Retreats',100),(4,'Luxury Seekers',80),(5,'Nature Lovers',100),(6,'Photography Buffs',70),(7,'Wellness Wanderers',50),(8,'Foodie Explorers',70),(9,'History Aficionados',60),(10,'Solo Travelers',50);
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
  `paymentstatus` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Indicates whether the invoice is "Paid," "Unpaid," or "Overdue." Tracks financial status.',
  `duedate` datetime NOT NULL COMMENT 'Date by which the payment should be completed. Ensures timely collection.',
  `bookingid` bigint NOT NULL COMMENT 'Unique identifier for every booking',
  `dueamount` decimal(8,2) NOT NULL,
  PRIMARY KEY (`invoiceid`),
  KEY `mms_invoice_mms_booking_fk` (`bookingid`),
  CONSTRAINT `mms_invoice_mms_booking_fk` FOREIGN KEY (`bookingid`) REFERENCES `mms_booking` (`bookingid`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_invoice`
--

LOCK TABLES `mms_invoice` WRITE;
/*!40000 ALTER TABLE `mms_invoice` DISABLE KEYS */;
INSERT INTO `mms_invoice` VALUES (1,'2024-01-09 12:00:00',232.38,'Paid','2024-02-08 12:00:00',1,232.38),(2,'2024-02-16 10:00:00',708.38,'Unpaid','2024-03-17 10:00:00',2,708.38),(3,'2024-03-13 09:30:00',534.89,'Paid','2024-04-12 09:30:00',3,534.89),(4,'2024-04-26 15:45:00',772.44,'Overdue','2024-05-26 15:45:00',4,772.44),(5,'2024-05-09 11:15:00',298.74,'Paid','2024-06-08 11:15:00',5,298.74),(6,'2024-06-15 13:45:00',918.80,'Unpaid','2024-07-15 13:45:00',6,918.80),(7,'2024-07-11 14:30:00',315.22,'Paid','2024-08-10 14:30:00',7,315.22),(8,'2024-08-03 16:00:00',776.14,'Overdue','2024-09-02 16:00:00',8,776.14),(9,'2024-09-19 10:30:00',354.31,'Paid','2024-10-18 10:30:00',9,354.31),(10,'2024-10-06 12:45:00',399.13,'Unpaid','2024-11-05 12:45:00',10,399.13),(11,'2024-12-01 09:00:00',830.24,'Paid','2024-12-31 09:00:00',11,830.24),(12,'2024-12-21 15:30:00',956.91,'Overdue','2025-01-20 15:30:00',12,956.91),(13,'2025-01-12 11:15:00',642.11,'Paid','2025-02-11 11:15:00',13,642.11),(14,'2025-02-15 10:45:00',206.87,'Unpaid','2025-03-17 10:45:00',14,206.87),(15,'2025-03-08 14:30:00',445.53,'Paid','2025-04-07 14:30:00',15,445.53),(16,'2025-04-19 10:00:00',931.02,'Overdue','2025-05-19 10:00:00',16,931.02),(17,'2025-05-26 11:45:00',558.35,'Paid','2025-06-25 11:45:00',17,558.35),(18,'2025-06-10 13:15:00',441.86,'Unpaid','2025-07-10 13:15:00',18,441.86),(19,'2025-07-11 09:00:00',168.31,'Paid','2025-08-10 09:00:00',19,168.31),(20,'2025-08-02 12:45:00',164.69,'Overdue','2025-09-01 12:45:00',20,164.69),(21,'2025-09-15 13:30:00',858.57,'Paid','2025-10-14 13:30:00',21,858.57),(22,'2025-10-28 10:15:00',642.70,'Unpaid','2025-11-27 10:15:00',22,642.70),(23,'2025-11-25 11:00:00',363.92,'Paid','2025-12-25 11:00:00',23,363.92),(24,'2025-12-15 12:30:00',386.91,'Overdue','2026-01-14 12:30:00',24,386.91),(25,'2025-12-21 09:15:00',298.18,'Paid','2026-01-20 09:15:00',25,298.18),(26,'2025-12-31 23:59:00',892.92,'Paid','2026-01-30 23:59:00',26,892.92),(27,'2025-12-25 19:45:00',755.34,'Paid','2026-01-24 19:45:00',27,755.34),(28,'2025-12-29 13:10:00',387.65,'Overdue','2026-01-28 13:10:00',28,387.65),(29,'2025-12-30 10:30:00',569.33,'Paid','2026-01-29 10:30:00',29,569.33),(30,'2025-12-31 21:15:00',482.10,'Canceled','2026-01-30 21:15:00',30,482.10);
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
  `packagename` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Name of the packages offered on the trip',
  `base_price` decimal(5,2) NOT NULL COMMENT 'Price of the package per person per night',
  `packagedetails` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Details of the package',
  PRIMARY KEY (`packageid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
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
  `firstname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Stores the passenger''s first name',
  `lastname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Stores the passenger''s last name',
  `dateofbirth` datetime NOT NULL COMMENT 'Hold''s the passenger''s birth date',
  `gender` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Captures the gender of the passenger',
  `contactnumber` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'A primary phone number to reach the passenger for notifications, emergencies, or updates related to their trip.',
  `emailaddress` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Stores the passenger├ÄΓÇ£├âΓÇí├âΓÇôs email address for electronic communication, including booking confirmations and promotional materials.',
  `streetaddr` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'The street address of the passenger''s primary residence, used for correspondence and identification purposes.',
  `city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Represents the passenger''s residential address. This could be useful for billing, mailing tickets, or other physical correspondence.',
  `state` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Represents the passenger''s residential address. This could be useful for billing, mailing tickets, or other physical correspondence.',
  `country` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Represents the passenger''s residential address. This could be useful for billing, mailing tickets, or other physical correspondence.',
  `zipcode` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Represents the passenger''s residential address. This could be useful for billing, mailing tickets, or other physical correspondence.',
  `nationality` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Records the passenger''s nationality, which may be relevant for certain legal or travel restrictions.',
  `passportnumber` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Stores the passport number, useful for international cruise trips where passport details are required for customs and immigration checks.',
  `emergencycontactname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'The name of a designated emergency contact who can be notified if needed.',
  `emergencycontactnumber` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'The contact number for the emergency contact, ensuring quick reachability in case of emergencies during the trip.',
  `groupid` bigint NOT NULL COMMENT 'Unqiue identifier for every group',
  PRIMARY KEY (`passengerid`),
  KEY `mms_passenger_mms_group_fk` (`groupid`),
  CONSTRAINT `mms_passenger_mms_group_fk` FOREIGN KEY (`groupid`) REFERENCES `mms_group` (`groupid`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_passenger`
--

LOCK TABLES `mms_passenger` WRITE;
/*!40000 ALTER TABLE `mms_passenger` DISABLE KEYS */;
INSERT INTO `mms_passenger` VALUES (1,'John','Doe','1985-07-12 00:00:00','M','1234567890','john.doe@example.com','123 Elm St','Springfield','IL','USA','62704','American','A12345678','Jane Doe','0987654321',3),(2,'Jane','Smith','1992-03-25 00:00:00','F','2345678901','jane.smith@example.com','456 Oak St','New York','NY','USA','10001','American','B98765432','John Smith','0123456789',7),(3,'Emily','Brown','1978-10-15 00:00:00','F','3456789012','emily.brown@example.com','789 Pine St','Seattle','WA','USA','98101','Canadian','C56789012','William Brown','8765432109',5),(4,'Michael','Johnson','1980-05-20 00:00:00','M','4567890123','michael.johnson@example.com','321 Birch St','Los Angeles','CA','USA','90001','British','D23456789','Sarah Johnson','5432109876',2),(5,'Jessica','Williams','1990-11-30 00:00:00','F','5678901234','jessica.williams@example.com','654 Maple St','Austin','TX','USA','73301','Australian','E34567890','Chris Williams','2109876543',9),(6,'William','Davis','1988-08-12 00:00:00','M','6789012345','william.davis@example.com','987 Cedar St','Denver','CO','USA','80202','American','F45678901','Emily Davis','5432109876',6),(7,'Sophia','Martinez','1995-01-22 00:00:00','F','7890123456','sophia.martinez@example.com','654 Palm St','Miami','FL','USA','33101','Mexican','G56789012','Carlos Martinez','9876543210',8),(8,'James','Harris','1982-02-18 00:00:00','M','8901234567','james.harris@example.com','432 Willow St','Boston','MA','USA','02108','British','H12345678','Lisa Harris','9876543210',4),(9,'Olivia','Clark','1997-04-10 00:00:00','F','9012345678','olivia.clark@example.com','876 Redwood St','Chicago','IL','USA','60601','American','I23456789','Nathan Clark','6543210987',10),(10,'Liam','Lewis','1993-07-05 00:00:00','M','0123456789','liam.lewis@example.com','345 Aspen St','Houston','TX','USA','77002','Canadian','J34567890','Mia Lewis','7654321098',1),(11,'Isabella','Taylor','1986-02-14 00:00:00','F','1112223334','isabella.taylor@example.com','12 Forest Ln','Phoenix','AZ','USA','85001','American','K23456789','Alex Taylor','9988776655',2),(12,'Noah','Anderson','1990-06-20 00:00:00','M','2223334445','noah.anderson@example.com','45 Lake St','Dallas','TX','USA','75201','American','L12345678','Sophia Anderson','8877665544',4),(13,'Mia','Thomas','1992-11-05 00:00:00','F','3334445556','mia.thomas@example.com','78 Sunset Blvd','San Francisco','CA','USA','94101','British','M98765432','Ryan Thomas','7766554433',5),(14,'Lucas','Moore','1983-01-15 00:00:00','M','4445556667','lucas.moore@example.com','32 Hilltop Rd','Seattle','WA','USA','98102','Canadian','N56789012','Emma Moore','6655443322',7),(15,'Emma','White','1989-09-09 00:00:00','F','5556667778','emma.white@example.com','54 Bay St','San Diego','CA','USA','92101','American','O34567890','Daniel White','5544332211',3),(16,'Alexander','King','1987-07-22 00:00:00','M','6667778889','alex.king@example.com','67 Broadway','Austin','TX','USA','73301','Mexican','P45678901','Isabella King','4433221100',9),(17,'Sophia','Scott','1996-12-25 00:00:00','F','7778889990','sophia.scott@example.com','89 Elm Dr','Boston','MA','USA','02108','Canadian','Q12345678','Ethan Scott','3322110099',6),(18,'Benjamin','Harris','1991-10-30 00:00:00','M','8889991112','ben.harris@example.com','21 High St','Orlando','FL','USA','32801','British','R23456789','Lily Harris','2211009988',10),(19,'Evelyn','Walker','1984-04-18 00:00:00','F','9991112223','evelyn.walker@example.com','76 Valley Rd','Chicago','IL','USA','60602','Australian','S56789012','Jack Walker','1100998877',8),(20,'Logan','Young','1982-03-09 00:00:00','M','1112223334','logan.young@example.com','10 Bridge Ln','Denver','CO','USA','80203','American','T12345678','Grace Young','9988776655',1),(21,'Charlotte','Hill','1990-05-06 00:00:00','F','1234506789','charlotte.hill@example.com','34 Oak Dr','San Jose','CA','USA','95101','American','U98765432','Henry Hill','8765432109',2),(22,'Henry','Baker','1984-08-14 00:00:00','M','2345607891','henry.baker@example.com','11 Cedar Ln','Miami','FL','USA','33109','British','V56789012','Emma Baker','7654321098',3),(23,'Amelia','Evans','1993-07-22 00:00:00','F','3456708912','amelia.evans@example.com','56 Birch Rd','Dallas','TX','USA','75206','Canadian','W34567890','Liam Evans','6543210987',6),(24,'Oliver','Carter','1988-01-19 00:00:00','M','4567809123','oliver.carter@example.com','89 Walnut St','Phoenix','AZ','USA','85004','Australian','X45678901','Sophia Carter','5432109876',7),(25,'Ava','Murphy','1997-10-05 00:00:00','F','5678901234','ava.murphy@example.com','12 Maple Ave','Orlando','FL','USA','32803','American','Y12345678','Ethan Murphy','4321098765',4),(26,'Elijah','Turner','1985-03-12 00:00:00','M','6789012345','elijah.turner@example.com','45 Pine Blvd','Boston','MA','USA','02115','Mexican','Z23456789','Isabella Turner','3210987654',9),(27,'Harper','Morgan','1989-06-16 00:00:00','F','7890123456','harper.morgan@example.com','78 Valley Dr','Seattle','WA','USA','98103','Canadian','A23456789','Daniel Morgan','2109876543',8),(28,'Lucas','Reed','1994-12-11 00:00:00','M','8901234567','lucas.reed@example.com','34 Elm Ln','Austin','TX','USA','73301','British','B34567890','Mia Reed','1098765432',5),(29,'Ella','Howard','1991-02-20 00:00:00','F','9012345678','ella.howard@example.com','67 Broadway St','Houston','TX','USA','77004','Australian','C45678901','Noah Howard','0987654321',10),(30,'Mason','Coleman','1982-04-09 00:00:00','M','0123456789','mason.coleman@example.com','98 Redwood Rd','Denver','CO','USA','80204','American','D56789012','Grace Coleman','9876543210',1);
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
  `paymentmethod` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Method of payment (e.g., "Credit Card," "Bank Transfer," "Cash"). Provides context for processing.',
  `transactionid` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Unique ID from the payment provider for reference. Useful for audits and confirmations.',
  `invoiceid` bigint NOT NULL COMMENT 'Primary key for the invoice.',
  PRIMARY KEY (`paymentid`),
  KEY `mms_payment_mms_invoice_fk` (`invoiceid`),
  CONSTRAINT `mms_payment_mms_invoice_fk` FOREIGN KEY (`invoiceid`) REFERENCES `mms_invoice` (`invoiceid`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_payment_detail`
--

LOCK TABLES `mms_payment_detail` WRITE;
/*!40000 ALTER TABLE `mms_payment_detail` DISABLE KEYS */;
INSERT INTO `mms_payment_detail` VALUES (1,'2024-01-15 10:30:00',232.38,'Credit Card','TXN12345601',1),(2,'2024-02-20 14:00:00',708.38,'Bank Transfer','TXN12345602',2),(3,'2024-03-18 09:45:00',534.89,'Cash','TXN12345603',3),(4,'2024-05-03 13:30:00',772.44,'Mobile Payment','TXN12345604',4),(5,'2024-05-15 11:00:00',298.74,'Credit Card','TXN12345605',5),(6,'2024-06-25 15:00:00',918.80,'Bank Transfer','TXN12345606',6),(7,'2024-07-18 16:45:00',315.22,'Cash','TXN12345607',7),(8,'2024-08-08 10:15:00',776.14,'Credit Card','TXN12345608',8),(9,'2024-09-24 09:30:00',354.31,'Bank Transfer','TXN12345609',9),(10,'2024-10-12 14:00:00',399.13,'Mobile Payment','TXN12345610',10),(11,'2024-12-05 11:45:00',830.24,'Credit Card','TXN12345611',11),(12,'2024-12-26 15:20:00',956.91,'Bank Transfer','TXN12345612',12),(13,'2024-12-29 13:10:00',642.11,'Cash','TXN12345613',13),(14,'2024-12-30 14:50:00',206.87,'Credit Card','TXN12345614',14),(15,'2024-12-31 16:00:00',445.53,'Bank Transfer','TXN12345615',15),(16,'2024-12-30 12:45:00',931.02,'Mobile Payment','TXN12345616',16),(17,'2024-12-29 14:30:00',558.35,'Cash','TXN12345617',17),(18,'2024-12-29 10:00:00',441.86,'Credit Card','TXN12345618',18),(19,'2024-12-28 13:45:00',168.31,'Bank Transfer','TXN12345619',19),(20,'2024-12-28 09:30:00',164.69,'Mobile Payment','TXN12345620',20),(21,'2024-12-27 14:30:00',858.57,'Credit Card','TXN12345621',21),(22,'2024-12-27 15:45:00',642.70,'Bank Transfer','TXN12345622',22),(23,'2024-12-26 16:20:00',363.92,'Mobile Payment','TXN12345623',23),(24,'2024-12-26 12:30:00',386.91,'Cash','TXN12345624',24),(25,'2024-12-25 11:15:00',298.18,'Credit Card','TXN12345625',25),(26,'2024-12-24 10:00:00',892.92,'Bank Transfer','TXN12345626',26),(27,'2024-12-24 09:45:00',755.37,'Mobile Payment','TXN12345627',27),(28,'2024-12-23 14:10:00',789.47,'Cash','TXN12345628',28),(29,'2024-12-22 12:45:00',52.72,'Credit Card','TXN12345629',29),(30,'2024-12-22 10:30:00',874.13,'Bank Transfer','TXN12345630',30);
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
  `portname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'The name of the port where the cruise either stops during the itinerary or starts/ends the trip. This attribute identifies specific locations included in the trip.',
  `address` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Street address where the port is located. ',
  `portcity` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Name of the country where the port is located. Useful for regional sorting and queries.',
  `portstate` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Name of the state (if applicable) where the port is located. Adds further location specificity.',
  `portcountry` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Name of the city where the port is located. Useful for detailed geographical reference.',
  `nearestairport` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Name of the nearest airport to the port',
  `parkingspots` int NOT NULL COMMENT 'Number of parking spots available at the port',
  PRIMARY KEY (`portid`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_port`
--

LOCK TABLES `mms_port` WRITE;
/*!40000 ALTER TABLE `mms_port` DISABLE KEYS */;
INSERT INTO `mms_port` VALUES (1,'Port 1','1015 N America Way','Miami','FL','USA','Miami International Airport',200),(2,'Port 2','1001 Harbor Blvd','Los Angeles','CA','USA','Los Angeles International Airport',250),(3,'Port 3','Pier 88','New York','NY','USA','John F. Kennedy International Airport',300),(4,'Port 4','Waalhaven Zuid 250','Rotterdam','South Holland','Netherlands','Rotterdam The Hague Airport',100),(5,'Port 5','Marina South Pier','Singapore','Central','Singapore','Singapore Changi Airport',350),(6,'Port 6','Tokyo Bay Area','Tokyo','Kanto','Japan','Narita International Airport',200),(7,'Port 7','Kowloon Bay','Hong Kong','','China','Hong Kong International Airport',400),(8,'Port 8','Moll de Barcelona','Barcelona','Catalonia','Spain','Barcelona-El Prat Airport',150),(9,'Port 9','Port Rashid','Dubai','','UAE','Dubai International Airport',500),(10,'Port 10','Barangaroo','Sydney','NSW','Australia','Sydney Kingsford Smith Airport',600),(11,'Port 11','Dock Road','Cape Town','Western Cape','South Africa','Cape Town International Airport',100),(12,'Port 12','Huangpu River','Shanghai','Shanghai','China','Shanghai Pudong International Airport',450),(13,'Port 13','Avenida de los Corsarios','Buenos Aires','Buenos Aires','Argentina','Ministro Pistarini International Airport',120),(14,'Port 14','Veddeler Bogen','Hamburg','Hamburg','Germany','Hamburg Airport',250),(15,'Port 15','Ballard Estate','Mumbai','Maharashtra','India','Chhatrapati Shivaji International Airport',150),(16,'Port 16','Via Milano','Genoa','Liguria','Italy','Genoa Cristoforo Colombo Airport',130),(17,'Port 17','Quai des Belges','Marseille','Provence-Alpes-Côte d\'Azur','France','Marseille Provence Airport',100),(18,'Port 18','Kattendijkdok-Oostkaai','Antwerp','Flanders','Belgium','Antwerp International Airport',80),(19,'Port 19','Av. Siqueira Campos','Santos','São Paulo','Brazil','Santos Dumont Airport',250),(20,'Port 20','Busan Port','Busan','South Gyeongsang','South Korea','Gimhae International Airport',300),(21,'Port 21','Muelle de la Aduana','Valencia','Valencia','Spain','Valencia Airport',200),(22,'Port 22','Veddeler Bogen','Hamburg','Hamburg','Germany','Hamburg Airport',220),(23,'Port 23','Huangpu River','Shanghai','Shanghai','China','Shanghai Pudong International Airport',500),(24,'Port 24','Port of Colombo','Colombo','Western','Sri Lanka','Bandaranaike International Airport',350),(25,'Port 25','Calle Real','Algeciras','Andalusia','Spain','La Linea de la Concepcion Airport',90),(26,'Port 26','Minato Mirai','Yokohama','Kanagawa','Japan','Haneda Airport',180),(27,'Port 27','Via Cristoforo Colombo','Rome','Lazio','Italy','Leonardo da Vinci International Airport',180),(28,'Port 28','Port de Barceloneta','Barcelona','Catalonia','Spain','Barcelona-El Prat Airport',400),(29,'Port 29','Piazzale di Porta Romana','Milan','Lombardy','Italy','Milan Malpensa Airport',250),(30,'Port 30','Pier 40','San Francisco','CA','USA','San Francisco International Airport',550),(31,'Port 31','Delfshaven','Rotterdam','South Holland','Netherlands','Rotterdam The Hague Airport',200),(32,'Port 32','Port of Long Beach','Long Beach','CA','USA','Long Beach Airport',400),(33,'Port 33','Port of Antwerp','Antwerp','Flanders','Belgium','Antwerp International Airport',180),(34,'Port 34','Pier 39','San Francisco','CA','USA','San Francisco International Airport',300),(35,'Port 35','Glenelg','Adelaide','South Australia','Australia','Adelaide International Airport',150);
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
  `orderofstop` int NOT NULL COMMENT 'The order in which the ship stops at each port',
  `isstartport` tinyint NOT NULL COMMENT 'Indicates if the port is starting point of the trip',
  `isendport` tinyint NOT NULL COMMENT 'Indicates if the port is ending point of the trip',
  `description` varchar(500) NOT NULL,
  PRIMARY KEY (`itineraryid`),
  KEY `mms_port_stop_mms_port_fk` (`portid`),
  KEY `mms_port_stop_mms_trip_fk` (`tripid`),
  CONSTRAINT `mms_port_stop_mms_port_fk` FOREIGN KEY (`portid`) REFERENCES `mms_port` (`portid`),
  CONSTRAINT `mms_port_stop_mms_trip_fk` FOREIGN KEY (`tripid`) REFERENCES `mms_trip` (`tripid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_port_stop`
--

LOCK TABLES `mms_port_stop` WRITE;
/*!40000 ALTER TABLE `mms_port_stop` DISABLE KEYS */;
INSERT INTO `mms_port_stop` VALUES (1,20,1,'2024-08-14 00:00:00','2024-08-14 06:00:00',1,1,0,'Departure at Port 20.'),(2,28,1,'2024-08-16 00:00:00','2024-08-16 11:00:00',2,0,1,'Stop at Port 28.'),(3,8,2,'2024-04-11 00:00:00','2024-04-11 12:00:00',1,1,0,'Departure at Port 8.'),(4,15,2,'2024-04-13 00:00:00','2024-04-13 12:00:00',2,0,0,'Stop at Port 15.'),(5,9,2,'2024-04-15 00:00:00','2024-04-15 07:00:00',3,0,1,'Stop at Port 9.'),(6,4,3,'2024-09-28 00:00:00','2024-09-28 12:00:00',1,1,0,'Departure at Port 4.'),(7,3,3,'2024-09-30 00:00:00','2024-09-30 12:00:00',2,0,0,'Stop at Port 3.'),(8,25,3,'2024-10-02 00:00:00','2024-10-02 07:00:00',3,0,0,'Stop at Port 25.'),(9,14,3,'2024-10-04 00:00:00','2024-10-04 12:00:00',4,0,0,'Stop at Port 14.'),(10,19,3,'2024-10-06 00:00:00','2024-10-06 11:00:00',5,0,1,'Stop at Port 19.'),(11,1,4,'2024-09-16 00:00:00','2024-09-16 09:00:00',1,1,0,'Departure at Port 1.'),(12,2,4,'2024-09-17 00:00:00','2024-09-17 08:00:00',2,0,0,'Stop at Port 2.'),(13,30,4,'2024-09-18 00:00:00','2024-09-18 09:00:00',3,0,0,'Stop at Port 30.'),(14,17,4,'2024-09-19 00:00:00','2024-09-19 06:00:00',4,0,1,'Stop at Port 17.'),(15,9,5,'2024-11-10 00:00:00','2024-11-10 12:00:00',1,1,0,'Departure at Port 9.'),(16,30,5,'2024-11-12 00:00:00','2024-11-12 09:00:00',2,0,0,'Stop at Port 30.'),(17,6,5,'2024-11-14 00:00:00','2024-11-14 10:00:00',3,0,1,'Stop at Port 6.'),(18,27,6,'2024-02-05 00:00:00','2024-02-05 12:00:00',1,1,0,'Departure at Port 27.'),(19,14,6,'2024-02-07 00:00:00','2024-02-07 08:00:00',2,0,0,'Stop at Port 14.'),(20,23,6,'2024-02-09 00:00:00','2024-02-09 12:00:00',3,0,0,'Stop at Port 23.'),(21,29,6,'2024-02-11 00:00:00','2024-02-11 09:00:00',4,0,1,'Stop at Port 29.'),(22,20,1,'2024-08-14 00:00:00','2024-08-14 06:00:00',1,1,0,'Departure at Port 20.'),(23,28,1,'2024-08-16 00:00:00','2024-08-16 11:00:00',2,0,1,'Stop at Port 28.'),(24,8,2,'2024-04-11 00:00:00','2024-04-11 12:00:00',1,1,0,'Departure at Port 8.'),(25,15,2,'2024-04-13 00:00:00','2024-04-13 12:00:00',2,0,0,'Stop at Port 15.'),(26,9,2,'2024-04-15 00:00:00','2024-04-15 07:00:00',3,0,1,'Stop at Port 9.'),(27,4,3,'2024-09-28 00:00:00','2024-09-28 12:00:00',1,1,0,'Departure at Port 4.'),(28,3,3,'2024-09-30 00:00:00','2024-09-30 12:00:00',2,0,0,'Stop at Port 3.'),(29,25,3,'2024-10-02 00:00:00','2024-10-02 07:00:00',3,0,0,'Stop at Port 25.'),(30,14,3,'2024-10-04 00:00:00','2024-10-04 12:00:00',4,0,0,'Stop at Port 14.'),(31,19,3,'2024-10-06 00:00:00','2024-10-06 11:00:00',5,0,1,'Stop at Port 19.'),(32,1,4,'2024-09-16 00:00:00','2024-09-16 09:00:00',1,1,0,'Departure at Port 1.'),(33,2,4,'2024-09-17 00:00:00','2024-09-17 08:00:00',2,0,0,'Stop at Port 2.'),(34,30,4,'2024-09-18 00:00:00','2024-09-18 09:00:00',3,0,0,'Stop at Port 30.'),(35,17,4,'2024-09-19 00:00:00','2024-09-19 06:00:00',4,0,1,'Stop at Port 17.'),(36,9,5,'2024-11-10 00:00:00','2024-11-10 12:00:00',1,1,0,'Departure at Port 9.'),(37,30,5,'2024-11-12 00:00:00','2024-11-12 09:00:00',2,0,0,'Stop at Port 30.'),(38,6,5,'2024-11-14 00:00:00','2024-11-14 10:00:00',3,0,1,'Stop at Port 6.'),(39,27,6,'2024-02-05 00:00:00','2024-02-05 12:00:00',1,1,0,'Departure at Port 27.'),(40,14,6,'2024-02-07 00:00:00','2024-02-07 08:00:00',2,0,0,'Stop at Port 14.'),(41,23,6,'2024-02-09 00:00:00','2024-02-09 12:00:00',3,0,0,'Stop at Port 23.'),(42,29,6,'2024-02-11 00:00:00','2024-02-11 09:00:00',4,0,1,'Stop at Port 29.'),(43,25,7,'2024-01-15 00:00:00','2024-01-15 11:00:00',1,1,0,'Departure at Port 25.'),(44,10,7,'2024-01-18 00:00:00','2024-01-18 11:00:00',2,0,0,'Stop at Port 10.'),(45,5,27,'2024-08-15 00:00:00','2024-08-15 08:00:00',2,0,0,'Stop at Port 5.'),(46,11,27,'2024-08-16 00:00:00','2024-08-16 08:00:00',3,0,0,'Stop at Port 11.'),(47,14,27,'2024-08-17 00:00:00','2024-08-17 12:00:00',4,0,0,'Stop at Port 14.'),(48,4,27,'2024-08-18 00:00:00','2024-08-18 07:00:00',5,0,1,'Stop at Port 4.'),(49,30,28,'2024-09-07 00:00:00','2024-09-07 07:00:00',1,1,0,'Departure at Port 30.'),(50,7,28,'2024-09-09 00:00:00','2024-09-09 06:00:00',2,0,0,'Stop at Port 7.'),(51,17,28,'2024-09-11 00:00:00','2024-09-11 11:00:00',3,0,0,'Stop at Port 17.'),(52,28,28,'2024-09-13 00:00:00','2024-09-13 10:00:00',4,0,0,'Stop at Port 28.'),(53,11,28,'2024-09-15 00:00:00','2024-09-15 11:00:00',5,0,1,'Stop at Port 11.'),(54,1,29,'2024-09-26 00:00:00','2024-09-26 11:00:00',1,1,0,'Departure at Port 1.');
/*!40000 ALTER TABLE `mms_port_stop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_restaurant`
--

DROP TABLE IF EXISTS `mms_restaurant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_restaurant` (
  `restaurantid` smallint NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for each restaurant',
  `restaurantname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Name of the resturant',
  `floornumber` smallint NOT NULL COMMENT 'Floor where the restaurant is located in the ship',
  `openingtime` time DEFAULT NULL COMMENT 'Time at which the restaurant opens',
  `closingtime` time DEFAULT NULL COMMENT 'Time at which the restaurant closes',
  `servesbreakfast` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Value to specify if the restaurant serves breakfast or not. For e.g., ''Y'' for yes and ''N'' for no',
  `serveslunch` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Value to specify if the restaurant serves lunch or not. For e.g., ''Y'' for yes and ''N'' for no',
  `servesdinner` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Value to specify if the restaurant serves dinner or not. For e.g., ''Y'' for yes and ''N'' for no',
  `servesalcohol` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Value to specify if the restaurant serves alcohol or not. For e.g., ''Y'' for yes and ''N'' for no',
  `restaurant_description` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Description of the cuisine served with the restaurant.',
  PRIMARY KEY (`restaurantid`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_restaurant`
--

LOCK TABLES `mms_restaurant` WRITE;
/*!40000 ALTER TABLE `mms_restaurant` DISABLE KEYS */;
INSERT INTO `mms_restaurant` VALUES (1,'Common Buffett',6,'07:00:00','21:00:00','Y','Y','Y','N','Serves Breakfast, Lunch, and Dinner.'),(2,'Italian Specialty',8,'18:00:00','22:00:00','N','N','Y','N','Serves Dinner only.'),(3,'Mexican Specialty',7,'18:00:00','22:00:00','N','N','Y','N','Serves Dinner only.'),(4,'La-carte continental',6,'12:00:00','20:00:00','N','Y','Y','N','Serves Lunch and Dinner.'),(5,'Tokyo Ramen Japanese',5,'12:00:00','20:00:00','N','Y','Y','N','Serves Lunch and Dinner.'),(6,'Ming Wok Chinese',5,'12:00:00','20:00:00','N','Y','Y','N','Serves Lunch and Dinner.'),(7,'Round Clock Café',10,'00:00:00','23:59:59','Y','Y','Y','N','24-hour café with beverages and light food.'),(8,'Pool Bar',10,'10:00:00','22:00:00','N','N','N','Y','Serves alcoholic beverages.'),(9,'Stout Bar',7,'10:00:00','22:00:00','N','N','N','Y','Serves alcoholic beverages.');
/*!40000 ALTER TABLE `mms_restaurant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_room`
--

DROP TABLE IF EXISTS `mms_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_room` (
  `roomnumber` int NOT NULL,
  `roomfloor` smallint NOT NULL COMMENT 'Floor number of the room',
  `stateroomtypeid` smallint NOT NULL COMMENT 'Unique identifier of room type',
  `locid` smallint NOT NULL,
  PRIMARY KEY (`roomnumber`),
  KEY `mms_room_mms_room_type_fk` (`stateroomtypeid`),
  KEY `mms_room_mms_room_loc_fk` (`locid`),
  CONSTRAINT `mms_room_mms_room_loc_fk` FOREIGN KEY (`locid`) REFERENCES `mms_room_loc` (`locid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `mms_room_mms_room_type_fk` FOREIGN KEY (`stateroomtypeid`) REFERENCES `mms_room_type` (`stateroomtypeid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_room`
--

LOCK TABLES `mms_room` WRITE;
/*!40000 ALTER TABLE `mms_room` DISABLE KEYS */;
INSERT INTO `mms_room` VALUES (101,1,1,1),(102,1,2,1),(103,1,3,2),(104,1,4,2),(105,1,5,3),(106,1,6,3),(107,2,7,4),(108,2,1,4),(109,2,2,5),(110,2,3,5),(201,3,4,6),(202,3,5,6),(203,3,6,7),(204,3,7,7),(205,4,1,8),(206,4,2,8),(207,4,3,9),(208,4,4,9),(209,4,5,10),(210,4,6,10),(301,5,7,11),(302,5,1,11),(303,5,2,12),(304,5,3,12);
/*!40000 ALTER TABLE `mms_room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_room_loc`
--

DROP TABLE IF EXISTS `mms_room_loc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_room_loc` (
  `locid` smallint NOT NULL AUTO_INCREMENT COMMENT 'Unique ID of the location in the ship',
  `location` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Name of the location in the ship',
  PRIMARY KEY (`locid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
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
  `stateroomtype` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Name of the stateroom type',
  `roomsize` bigint NOT NULL COMMENT 'Size of the stateroom in SQFT',
  `numberofbeds` smallint NOT NULL COMMENT 'Number of beds in the room',
  `numberofbaths` decimal(2,1) NOT NULL COMMENT 'Number of the bathrooms in the stateroom',
  `numberofbalconies` smallint NOT NULL COMMENT 'Number of balconies in the stateroom',
  `roomtypedescription` varchar(500) NOT NULL,
  `baseprice` decimal(6,2) NOT NULL,
  PRIMARY KEY (`stateroomtypeid`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_room_type`
--

LOCK TABLES `mms_room_type` WRITE;
/*!40000 ALTER TABLE `mms_room_type` DISABLE KEYS */;
INSERT INTO `mms_room_type` VALUES (1,'The Haven Suite',1000,6,3.0,2,'Luxurious suite with panoramic views and multiple amenities',1000.00),(2,'Club Balcony Suite',800,4,2.0,2,'Spacious suite with a private balcony and club lounge access',800.00),(3,'Family Large Balcony',600,4,2.0,1,'Perfect for families with a large private balcony',600.00),(4,'Family Balcony',400,4,1.0,1,'Cozy family room with a private balcony',400.00),(5,'Oceanview Window',300,2,1.0,0,'Comfortable room with a view of the ocean',300.00),(6,'Inside Stateroom',200,2,1.0,0,'Compact room without windows',200.00),(7,'Studio Stateroom',150,1,1.0,0,'Economical room ideal for solo travelers',150.00);
/*!40000 ALTER TABLE `mms_room_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_ship`
--

DROP TABLE IF EXISTS `mms_ship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_ship` (
  `shipid` int NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for every ship',
  `shipname` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `capacity` int NOT NULL,
  PRIMARY KEY (`shipid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_ship`
--

LOCK TABLES `mms_ship` WRITE;
/*!40000 ALTER TABLE `mms_ship` DISABLE KEYS */;
INSERT INTO `mms_ship` VALUES (1,'Caribbean Explorer','A luxury cruise with great views and top amenities.',700),(2,'Ocean Voyager','Explore vast oceans with premium services and restaurants.',800),(3,'Island Breeze','Relax on this beautiful cruise ship with plenty of activities.',650),(4,'Sunset Princess','A blend of luxury and adventure with stunning views.',750),(5,'Blue Horizon','Elegant rooms, fine dining, and unforgettable experiences.',900),(6,'Grand Majesty','A majestic ship with a variety of activities and lounges.',850),(7,'Sea Breeze','A modern ship with relaxing amenities for a perfect vacation.',800),(8,'Dreamliner','Spacious rooms and dining with stunning ocean views.',950),(9,'Crystal Waters','Embark on an adventure with comfort and luxury at sea.',600),(10,'Oceanic Journey','An unforgettable journey with excellent facilities and entertainment.',950);
/*!40000 ALTER TABLE `mms_ship` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_ship_activity`
--

DROP TABLE IF EXISTS `mms_ship_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_ship_activity` (
  `id` int NOT NULL AUTO_INCREMENT,
  `shipid` int NOT NULL,
  `activityid` smallint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `shipid_idx` (`shipid`),
  KEY `mms_activity_fk_idx` (`activityid`),
  CONSTRAINT `mms_activity_fk` FOREIGN KEY (`activityid`) REFERENCES `mms_activity` (`activityid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `mms_ship_fk` FOREIGN KEY (`shipid`) REFERENCES `mms_ship` (`shipid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=124 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_ship_activity`
--

LOCK TABLES `mms_ship_activity` WRITE;
/*!40000 ALTER TABLE `mms_ship_activity` DISABLE KEYS */;
INSERT INTO `mms_ship_activity` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,1,5),(6,1,6),(7,1,7),(8,1,8),(9,1,9),(10,1,10),(11,1,11),(12,1,12),(13,1,13),(14,1,14),(15,1,15),(16,2,1),(17,2,2),(18,2,3),(19,2,4),(20,2,5),(21,2,6),(22,2,7),(23,2,8),(24,2,9),(25,2,10),(26,2,11),(27,2,12),(28,2,13),(29,2,14),(30,2,15),(31,3,1),(32,3,2),(33,3,3),(34,3,4),(35,3,5),(36,3,6),(37,3,7),(38,3,8),(39,3,9),(40,3,10),(41,3,11),(42,3,12),(43,3,13),(44,3,14),(45,3,15),(46,4,1),(47,4,2),(48,4,3),(49,4,4),(50,4,5),(51,4,6),(52,4,7),(53,4,8),(54,4,9),(55,4,10),(56,4,11),(57,4,12),(58,4,13),(59,4,14),(60,4,15),(61,5,1),(62,5,2),(63,5,3),(64,5,4),(65,5,5),(66,5,6),(67,5,8),(68,5,10),(69,5,11),(70,5,12),(71,5,13),(72,5,14),(73,6,1),(74,6,2),(75,6,4),(76,6,5),(77,6,7),(78,6,8),(79,6,10),(80,6,12),(81,6,13),(82,6,14),(83,6,15),(84,7,1),(85,7,2),(86,7,4),(87,7,5),(88,7,6),(89,7,8),(90,7,10),(91,7,12),(92,7,13),(93,7,14),(94,8,1),(95,8,2),(96,8,4),(97,8,5),(98,8,8),(99,8,10),(100,8,11),(101,8,12),(102,8,13),(103,8,14),(104,9,1),(105,9,2),(106,9,4),(107,9,5),(108,9,6),(109,9,10),(110,9,11),(111,9,12),(112,9,13),(113,9,14),(114,10,1),(115,10,2),(116,10,4),(117,10,5),(118,10,6),(119,10,8),(120,10,10),(121,10,11),(122,10,12),(123,10,13);
/*!40000 ALTER TABLE `mms_ship_activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_ship_restaurant`
--

DROP TABLE IF EXISTS `mms_ship_restaurant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_ship_restaurant` (
  `id` int NOT NULL AUTO_INCREMENT,
  `shipid` int NOT NULL,
  `restaurantid` smallint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `mms_ship_fk_idx` (`shipid`),
  KEY `mms_restaurant_fk_idx` (`restaurantid`),
  CONSTRAINT `mms_restaurant_ship_fk` FOREIGN KEY (`restaurantid`) REFERENCES `mms_restaurant` (`restaurantid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `mms_ship_restaurant_fk` FOREIGN KEY (`shipid`) REFERENCES `mms_ship` (`shipid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_ship_restaurant`
--

LOCK TABLES `mms_ship_restaurant` WRITE;
/*!40000 ALTER TABLE `mms_ship_restaurant` DISABLE KEYS */;
INSERT INTO `mms_ship_restaurant` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,1,5),(6,1,6),(7,1,7),(8,1,8),(9,1,9),(10,2,1),(11,2,2),(12,2,3),(13,2,4),(14,2,5),(15,2,6),(16,2,7),(17,2,8),(18,2,9),(19,3,1),(20,3,2),(21,3,3),(22,3,4),(23,3,5),(24,3,6),(25,3,7),(26,3,8),(27,3,9),(28,4,1),(29,4,2),(30,4,5),(31,4,8),(32,5,1),(33,5,4),(34,5,7),(35,6,1),(36,6,3),(37,6,6),(38,7,1),(39,7,2),(40,7,4),(41,8,1),(42,8,3),(43,8,6),(44,9,1),(45,9,5),(46,9,9),(47,10,1),(48,10,2),(49,10,7);
/*!40000 ALTER TABLE `mms_ship_restaurant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_ship_room`
--

DROP TABLE IF EXISTS `mms_ship_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_ship_room` (
  `shiproomid` int NOT NULL AUTO_INCREMENT,
  `shipid` int NOT NULL,
  `roomnumber` int NOT NULL,
  PRIMARY KEY (`shiproomid`),
  KEY `mms_ship_fk_idx` (`shipid`),
  KEY `mms_ship_room_mms_room_fk_idx` (`roomnumber`),
  CONSTRAINT `mms_ship_mms_room_fk` FOREIGN KEY (`shipid`) REFERENCES `mms_ship` (`shipid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `mms_ship_room_mms_room_fk` FOREIGN KEY (`roomnumber`) REFERENCES `mms_room` (`roomnumber`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_ship_room`
--

LOCK TABLES `mms_ship_room` WRITE;
/*!40000 ALTER TABLE `mms_ship_room` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_ship_room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_trip`
--

DROP TABLE IF EXISTS `mms_trip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_trip` (
  `tripid` bigint NOT NULL AUTO_INCREMENT COMMENT 'Primary key for each trip. Unique identifier for each trip entry.',
  `tripname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Descriptive name of the trip.',
  `startdate` date NOT NULL COMMENT 'The date when the trip begins. Ensures accurate tracking of trip schedules.',
  `enddate` date NOT NULL COMMENT 'The date when the trip ends. Helps define the trip duration.',
  `tripcostperperson` decimal(8,2) NOT NULL COMMENT 'Cost per person for the trip, including taxes. Supports budgeting and billing.',
  `tripstatus` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Status of the trip (e.g., upcoming, ongoing, completed).',
  `cancellationpolicy` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Trip cancellation status ‘canceled’.',
  `tripcapacity` int NOT NULL COMMENT 'Total passenger capacity for the cruise liner.',
  `tripdescription` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Description of the trip booked.',
  `finalbookingdate` date NOT NULL,
  `tripcapacityremaining` int NOT NULL,
  `tempcapacityreserved` tinyint NOT NULL DEFAULT '0',
  `tempreservationtimestamp` timestamp(1) NULL DEFAULT NULL,
  `tempcapacitynumber` int NOT NULL DEFAULT '0',
  `shipid` int NOT NULL,
  PRIMARY KEY (`tripid`),
  KEY `mms_ship_mms_trip_fk` (`shipid`),
  CONSTRAINT `mms_ship_mms_trip_fk` FOREIGN KEY (`shipid`) REFERENCES `mms_ship` (`shipid`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_trip`
--

LOCK TABLES `mms_trip` WRITE;
/*!40000 ALTER TABLE `mms_trip` DISABLE KEYS */;
INSERT INTO `mms_trip` VALUES (1,'Caribbean Adventure','2024-07-09','2024-07-16',1536.82,'Confirmed','Flexible cancellation policy',489,'Explore the best of tropical beaches and sunny islands.','2024-07-08',489,0,'2024-12-08 14:01:59.7',0,2),(2,'Tropical Escape','2024-05-17','2024-05-25',128.72,'Upcoming','Flexible cancellation policy',252,'Embark on a luxurious cruise across the Caribbean waters.','2024-05-16',252,0,'2024-12-08 14:01:59.7',0,3),(3,'Island Getaway','2024-07-14','2024-07-24',1811.38,'Upcoming','Flexible cancellation policy',290,'Dive into adventure with endless islands and clear blue skies.','2024-07-13',290,0,'2024-12-08 14:01:59.7',0,5),(4,'Jungle Safari','2024-12-04','2024-12-12',683.24,'Confirmed','Flexible cancellation policy',444,'Join us for an unforgettable beach getaway.','2024-12-02',444,0,'2024-12-08 14:01:59.7',0,2),(5,'Ocean Breeze','2024-01-11','2024-01-19',1312.29,'Confirmed','Flexible cancellation policy',340,'Experience the wonders of the Caribbean with pristine beaches and clear waters.','2024-01-10',340,0,'2024-12-08 14:01:59.7',0,1),(6,'Sunshine Voyage','2024-09-07','2024-09-15',1870.55,'Upcoming','Flexible cancellation policy',363,'Discover hidden gems and explore the uncharted islands.','2024-09-05',363,0,'2024-12-08 14:01:59.7',0,9),(7,'Paradise Cruise','2024-02-11','2024-02-21',1336.74,'Confirmed','Flexible cancellation policy',404,'Bask in the sun with this perfect beach vacation.','2024-02-09',404,0,'2024-12-08 14:01:59.7',0,8),(8,'Mystic Shores','2024-05-27','2024-06-05',1377.64,'Confirmed','Flexible cancellation policy',281,'A relaxing retreat to the most tranquil islands.','2024-05-26',281,0,'2024-12-08 14:01:59.8',0,6),(9,'Sunset Retreat','2024-05-18','2024-05-23',574.94,'Upcoming','canceled',65,'Enjoy nature\'s beauty and serene tropical surroundings.','2024-05-17',65,0,'2024-12-08 14:01:59.8',0,7),(10,'Blue Lagoon Tour','2024-03-27','2024-04-03',1569.83,'Confirmed','Flexible cancellation policy',318,'A journey of a lifetime awaits with ocean views and fine dining.','2024-03-26',318,0,'2024-12-08 14:01:59.8',0,8),(11,'Tropical Haven','2024-11-27','2024-12-01',551.11,'Confirmed','Flexible cancellation policy',436,'A fantastic adventure with island hopping and sun-kissed beaches.','2024-11-26',436,0,'2024-12-08 14:01:59.8',0,3),(12,'Coral Reef Expedition','2024-11-19','2024-11-24',748.78,'Upcoming','canceled',64,'Get away to crystal-clear waters and white sandy beaches.','2024-11-17',64,0,'2024-12-08 14:01:59.8',0,6),(13,'Golden Sands Trip','2024-05-29','2024-06-02',1092.75,'Confirmed','canceled',267,'Revel in adventure and relaxation with scenic views and unforgettable experiences.','2024-05-26',267,0,'2024-12-08 14:01:59.8',0,9),(14,'Seashell Island','2024-03-08','2024-03-18',796.81,'Confirmed','canceled',316,'Experience luxury at sea with tropical destinations and deluxe accommodations.','2024-03-07',316,0,'2024-12-08 14:01:59.8',0,3),(15,'Palm Paradise','2024-11-17','2024-11-27',514.47,'Confirmed','Flexible cancellation policy',355,'A complete paradise getaway with everything you need for the perfect trip.','2024-11-15',355,0,'2024-12-08 14:01:59.8',0,4),(16,'Sapphire Escape','2024-01-27','2024-02-02',264.15,'Confirmed','canceled',271,'Travel to the most beautiful beaches the Caribbean has to offer.','2024-01-26',271,0,'2024-12-08 14:01:59.8',0,7),(17,'Oceanic Horizon','2024-10-20','2024-10-28',715.55,'Confirmed','Flexible cancellation policy',309,'An unforgettable tour of the best islands and the most breathtaking views.','2024-10-19',309,0,'2024-12-08 14:01:59.8',0,5),(18,'Sunset Journey','2024-05-26','2024-05-30',1935.84,'Upcoming','Flexible cancellation policy',396,'Come join us for a serene trip to the islands with rich history.','2024-05-23',396,0,'2024-12-08 14:01:59.8',0,9),(19,'Wild Safari Expedition','2024-06-30','2024-07-09',1843.37,'Upcoming','canceled',210,'Luxury, adventure, and relaxation come together on this unforgettable journey.','2024-06-27',210,0,'2024-12-08 14:01:59.8',0,2),(20,'Lagoon Voyage','2024-09-08','2024-09-15',1713.86,'Confirmed','Flexible cancellation policy',240,'A tropical dream adventure with endless white sands and blue waters.','2024-09-05',240,0,'2024-12-08 14:01:59.8',0,4),(21,'Dream Island Adventure','2024-02-13','2024-02-20',1650.86,'Upcoming','canceled',224,'Embark on a journey to the most beautiful shores and crystal clear waters.','2024-02-12',224,0,'2024-12-08 14:01:59.8',0,5),(22,'Deep Sea Dive','2024-05-07','2024-05-16',1538.34,'Confirmed','canceled',132,'Explore secluded beaches and tropical islands in this exciting escape.','2024-05-05',132,0,'2024-12-08 14:01:59.8',0,6),(23,'Caribbean Winds Tour','2024-04-10','2024-04-19',464.77,'Confirmed','canceled',376,'A family-friendly vacation for fun and sun in the Caribbean.','2024-04-07',376,0,'2024-12-08 14:01:59.8',0,9),(24,'Treasure Island Journey','2024-06-15','2024-06-22',1054.22,'Upcoming','canceled',461,'Discover the beauty of the Caribbean with an all-inclusive experience.','2024-06-14',461,0,'2024-12-08 14:01:59.8',0,1),(25,'Island Breeze','2024-08-14','2024-08-19',517.62,'Confirmed','Flexible cancellation policy',75,'Join us on a scenic voyage with coastal views and vibrant tropical colors.','2024-08-12',75,0,'2024-12-08 14:01:59.8',0,1),(26,'Coastal Discovery','2024-04-22','2024-04-30',1238.42,'Confirmed','Flexible cancellation policy',319,'Embark on a tranquil adventure with secluded beaches and exclusive resorts.','2024-04-21',319,0,'2024-12-08 14:01:59.8',0,6),(27,'Grand Cruise Adventure','2024-10-31','2024-11-07',370.50,'Confirmed','Flexible cancellation policy',86,'A relaxing trip across warm waters with all the luxury of tropical escape.','2024-10-29',86,0,'2024-12-08 14:01:59.8',0,7),(28,'Island Serenity','2024-03-28','2024-04-07',613.86,'Confirmed','',197,'Experience a new world of adventure and relaxation along pristine shores.','2024-03-25',197,0,'2024-12-08 14:01:59.8',0,9),(29,'Seaside Getaway','2024-05-10','2024-05-19',1993.42,'Upcoming','canceled',142,'Explore the best of tropical beaches and sunny islands.','2024-05-08',142,0,'2024-12-08 14:01:59.8',0,8),(30,'Caribbean Adventure','2024-08-26','2024-09-01',953.18,'Confirmed','canceled',91,'Embark on a luxurious cruise across the Caribbean waters.','2024-08-23',91,0,'2024-12-08 14:01:59.8',0,10),(31,'Caribbean Explorer','2024-11-03','2024-11-10',1500.00,'Confirmed','Flexible cancellation policy',320,'An amazing tour across tropical islands and crystal-clear waters.','2024-11-01',320,0,'2024-12-08 14:01:59.8',0,11),(32,'Southern Sun Cruise','2024-12-01','2024-12-10',1270.12,'Upcoming','canceled',250,'A luxury cruise featuring southern islands with breathtaking sunsets.','2024-11-29',250,0,'2024-12-08 14:01:59.8',0,12),(33,'Northern Lights Cruise','2025-01-05','2025-01-12',2050.32,'Confirmed','Flexible cancellation policy',180,'Discover the breathtaking beauty of the Northern Lights on this exclusive cruise.','2025-01-04',180,0,'2024-12-08 14:01:59.8',0,13),(34,'Exotic Far East','2025-02-10','2025-02-20',1723.58,'Upcoming','canceled',200,'Explore the ancient lands of Asia and the exotic beaches of the East.','2025-02-09',200,0,'2024-12-08 14:01:59.8',0,14),(35,'Mediterranean Odyssey','2025-03-01','2025-03-10',1345.64,'Confirmed','Flexible cancellation policy',350,'A wonderful Mediterranean journey with stops at historical landmarks and beautiful beaches.','2025-02-28',350,0,'2024-12-08 14:01:59.8',0,15),(36,'Arctic Adventure','2025-04-10','2025-04-17',2100.45,'Confirmed','Flexible cancellation policy',120,'Venture into the Arctic for a once-in-a-lifetime polar exploration experience.','2025-04-09',120,0,'2024-12-08 14:01:59.8',0,16),(37,'Amazon River Expedition','2025-05-05','2025-05-12',1895.87,'Upcoming','canceled',180,'Embark on an unforgettable adventure along the Amazon River.','2025-05-04',180,0,'2024-12-08 14:01:59.8',0,17),(38,'Pacific Horizons','2025-06-10','2025-06-17',1580.23,'Confirmed','Flexible cancellation policy',200,'Explore the stunning Pacific Islands on a luxurious cruise.','2025-06-09',200,0,'2024-12-08 14:01:59.8',0,18),(39,'Alaskan Wilderness','2025-07-01','2025-07-08',2450.12,'Confirmed','Flexible cancellation policy',250,'Witness the breathtaking wilderness of Alaska and its spectacular glaciers.','2025-06-30',250,0,'2024-12-08 14:01:59.8',0,19),(40,'South Pacific Dreams','2025-08-01','2025-08-08',1995.33,'Upcoming','canceled',350,'A luxurious escape to the serene beaches and crystal-clear waters of the South Pacific.','2025-07-31',350,0,'2024-12-08 14:01:59.8',0,20);
/*!40000 ALTER TABLE `mms_trip` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_trip_package`
--

DROP TABLE IF EXISTS `mms_trip_package`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_trip_package` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tripid` bigint NOT NULL,
  `packageid` smallint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `mms_trip_package_trip_fk` (`tripid`),
  KEY `mms_trip_package_package_fk` (`packageid`),
  CONSTRAINT `mms_trip_package_package_fk` FOREIGN KEY (`packageid`) REFERENCES `mms_package` (`packageid`),
  CONSTRAINT `mms_trip_package_trip_fk` FOREIGN KEY (`tripid`) REFERENCES `mms_trip` (`tripid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_trip_package`
--

LOCK TABLES `mms_trip_package` WRITE;
/*!40000 ALTER TABLE `mms_trip_package` DISABLE KEYS */;
INSERT INTO `mms_trip_package` VALUES (3,1,1),(4,1,2),(5,2,3),(6,2,4),(7,3,5),(8,3,6),(9,4,7),(10,4,8),(11,5,9),(12,5,10),(13,6,11),(14,6,12),(15,7,13),(16,7,14),(17,8,15),(18,8,16),(19,9,17),(20,9,18),(21,10,19),(22,10,20),(23,11,21),(24,11,22),(25,12,23),(26,12,24),(27,13,25),(28,13,26),(29,14,27),(30,14,28),(31,15,29),(32,15,30);
/*!40000 ALTER TABLE `mms_trip_package` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_trip_room`
--

DROP TABLE IF EXISTS `mms_trip_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_trip_room` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dynamicprice` decimal(6,2) NOT NULL,
  `baseprice` decimal(6,2) NOT NULL,
  `isbooked` tinyint NOT NULL DEFAULT '0',
  `roomtype` varchar(20) NOT NULL,
  `location` varchar(50) NOT NULL,
  `roomnumber` int NOT NULL,
  `tripid` bigint NOT NULL,
  `tempreserved` tinyint DEFAULT '0',
  `tempreservationtimestamp` timestamp(1) NULL DEFAULT NULL,
  `tempreservationuser` int DEFAULT NULL,
  `bookingid` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `mms_trip_room_mms_trip_fk_idx` (`tripid`),
  KEY `mms_trip_room_mms_room_fk_idx` (`roomnumber`),
  KEY `mms_trip_room_mms_booking_fk_idx` (`bookingid`),
  CONSTRAINT `mms_trip_room_mms_booking_fk` FOREIGN KEY (`bookingid`) REFERENCES `mms_booking` (`bookingid`),
  CONSTRAINT `mms_trip_room_mms_room_fk` FOREIGN KEY (`roomnumber`) REFERENCES `mms_room` (`roomnumber`),
  CONSTRAINT `mms_trip_room_mms_trip_fk` FOREIGN KEY (`tripid`) REFERENCES `mms_trip` (`tripid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_trip_room`
--

LOCK TABLES `mms_trip_room` WRITE;
/*!40000 ALTER TABLE `mms_trip_room` DISABLE KEYS */;
INSERT INTO `mms_trip_room` VALUES (1,500.00,450.00,0,'The Haven Suite','Deck 1',1,1,1,'2024-01-07 19:30:00.0',NULL,15),(2,550.00,500.00,0,'Club Balcony Suite','Deck 2',2,1,0,NULL,NULL,3),(3,450.00,400.00,0,'Family Large Balcony','Deck 3',3,2,1,'2024-02-10 21:00:00.0',NULL,27),(4,600.00,550.00,0,'Family Balcony','Deck 4',4,2,0,NULL,NULL,11),(5,400.00,350.00,0,'Oceanview Window','Deck 5',5,3,1,'2024-03-01 15:15:00.0',NULL,19),(6,450.00,400.00,0,'Inside Stateroom','Deck 6',6,3,0,NULL,NULL,25),(7,650.00,600.00,0,'Studio Stateroom','Deck 7',7,4,1,'2024-04-10 13:00:00.0',NULL,18),(8,700.00,650.00,0,'The Haven Suite','Deck 8',8,4,0,NULL,NULL,1),(9,550.00,500.00,0,'Club Balcony Suite','Deck 9',9,5,0,NULL,NULL,22),(10,600.00,550.00,0,'Family Large Balcony','Deck 10',10,5,1,'2024-05-05 16:30:00.0',NULL,8),(11,750.00,700.00,0,'The Haven Suite','Deck 11',11,6,1,'2024-06-20 21:00:00.0',NULL,6),(12,800.00,750.00,0,'Studio Stateroom','Deck 12',12,6,0,NULL,NULL,14),(13,450.00,400.00,0,'Family Balcony','Deck 13',13,7,0,NULL,NULL,4),(14,500.00,450.00,0,'Inside Stateroom','Deck 14',14,7,1,'2024-07-01 15:00:00.0',NULL,10),(15,550.00,500.00,0,'Club Balcony Suite','Deck 15',15,8,1,'2024-07-07 12:30:00.0',NULL,20),(16,600.00,550.00,0,'The Haven Suite','Deck 16',16,8,0,NULL,NULL,2),(17,500.00,450.00,0,'Family Large Balcony','Deck 17',17,9,1,'2024-08-01 17:45:00.0',NULL,23),(18,550.00,500.00,0,'Studio Stateroom','Deck 18',18,9,0,NULL,NULL,9),(19,600.00,550.00,0,'Oceanview Window','Deck 19',19,10,1,'2024-09-03 18:30:00.0',NULL,7),(20,650.00,600.00,0,'Inside Stateroom','Deck 20',20,10,0,NULL,NULL,12),(21,450.00,400.00,0,'Family Balcony','Deck 21',21,11,1,'2024-10-09 15:15:00.0',NULL,24),(22,500.00,450.00,0,'Studio Stateroom','Deck 22',22,11,0,NULL,NULL,5),(23,650.00,600.00,0,'The Haven Suite','Deck 23',23,12,0,NULL,NULL,13),(24,700.00,650.00,0,'Club Balcony Suite','Deck 24',24,12,1,'2024-12-04 14:30:00.0',NULL,21);
/*!40000 ALTER TABLE `mms_trip_room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mms_user_profile`
--

DROP TABLE IF EXISTS `mms_user_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mms_user_profile` (
  `profileid` int NOT NULL AUTO_INCREMENT,
  `phonenumber` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `dateofbirth` date DEFAULT NULL,
  `userid` int NOT NULL,
  PRIMARY KEY (`profileid`),
  KEY `fk_mms_user_profile_auth_user` (`userid`),
  CONSTRAINT `mms_user_profile_userid_fk` FOREIGN KEY (`userid`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mms_user_profile`
--

LOCK TABLES `mms_user_profile` WRITE;
/*!40000 ALTER TABLE `mms_user_profile` DISABLE KEYS */;
/*!40000 ALTER TABLE `mms_user_profile` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb3;
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
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb3;
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

-- Dump completed on 2024-12-08  9:27:24
