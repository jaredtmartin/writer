-- MySQL dump 10.13  Distrib 5.5.24, for osx10.6 (i386)
--
-- Host: localhost    Database: webservices
-- ------------------------------------------------------
-- Server version	5.5.24

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_bda51c3c` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_a7792de1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_e4470c6e` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add log entry',7,'add_logentry'),(20,'Can change log entry',7,'change_logentry'),(21,'Can delete log entry',7,'delete_logentry'),(22,'Can add Category',8,'add_category'),(23,'Can change Category',8,'change_category'),(24,'Can delete Category',8,'delete_category'),(25,'Can add Article',9,'add_article'),(26,'Can change Article',9,'change_article'),(27,'Can delete Article',9,'delete_article'),(28,'Can add Question',10,'add_question'),(29,'Can change Question',10,'change_question'),(30,'Can delete Question',10,'delete_question'),(31,'Can add Response',11,'add_response'),(32,'Can change Response',11,'change_response'),(33,'Can delete Response',11,'delete_response'),(34,'Can add screenshot',12,'add_screenshot'),(35,'Can change screenshot',12,'change_screenshot'),(36,'Can delete screenshot',12,'delete_screenshot'),(37,'Can add form',13,'add_form'),(38,'Can change form',13,'change_form'),(39,'Can delete form',13,'delete_form'),(40,'Can add element',14,'add_element'),(41,'Can change element',14,'change_element'),(42,'Can delete element',14,'delete_element'),(43,'Can add result',15,'add_result'),(44,'Can change result',15,'change_result'),(45,'Can delete result',15,'delete_result'),(46,'Can add value',16,'add_value'),(47,'Can change value',16,'change_value'),(48,'Can delete value',16,'delete_value'),(49,'Can add facebook user',17,'add_facebookuser'),(50,'Can change facebook user',17,'change_facebookuser'),(51,'Can delete facebook user',17,'delete_facebookuser'),(52,'Can add facebook like',18,'add_facebooklike'),(53,'Can change facebook like',18,'change_facebooklike'),(54,'Can delete facebook like',18,'delete_facebooklike'),(55,'Can add facebook profile',19,'add_facebookprofile'),(56,'Can change facebook profile',19,'change_facebookprofile'),(57,'Can delete facebook profile',19,'delete_facebookprofile'),(58,'Can add open graph share',20,'add_opengraphshare'),(59,'Can change open graph share',20,'change_opengraphshare'),(60,'Can delete open graph share',20,'delete_opengraphshare'),(61,'Can add facebook invite',21,'add_facebookinvite'),(62,'Can change facebook invite',21,'change_facebookinvite'),(63,'Can delete facebook invite',21,'delete_facebookinvite'),(64,'Can add theme',22,'add_theme'),(65,'Can change theme',22,'change_theme'),(66,'Can delete theme',22,'delete_theme');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'jared','','','jared@home.com','pbkdf2_sha256$10000$waRyWWRqkZjE$R6VzYLP0tHcrK1eCIRPlRFwCkEYIhramDQEXh2EVaOQ=',1,1,1,'2012-11-19 21:31:11','2012-11-03 18:54:59'),(3,'fred','','','jaredtmartin@gmail.com','pbkdf2_sha256$10000$S6xpGLC0fIMQ$lSv+fV3BWJVQrw53zvKf6BjNdEPN4PN/ENkXChpJJ5g=',0,1,0,'2012-11-17 16:07:34','2012-11-17 16:07:33');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_fbfc09f1` (`user_id`),
  KEY `auth_user_groups_bda51c3c` (`group_id`),
  CONSTRAINT `group_id_refs_id_f0ee9890` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_831107f1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_fbfc09f1` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_f2045483` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_fbfc09f1` (`user_id`),
  KEY `django_admin_log_e4470c6e` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c8665aa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2012-11-10 03:49:31',1,13,'1','Contacts',1,''),(2,'2012-11-10 04:30:21',1,13,'1','Contacts',2,'Added element \"Country\".'),(3,'2012-11-10 04:32:49',1,13,'1','Contacts',2,'Changed klass and order for element \"Country\". Changed order for element \"Email\". Changed order for element \"Website URL\".'),(4,'2012-11-10 04:37:52',1,13,'1','Contacts',2,'Changed klass for element \"Email\".'),(5,'2012-11-10 04:57:39',1,13,'1','Contacts',2,'Changed success_url.'),(6,'2012-11-10 15:29:25',1,13,'1','Contacts',1,''),(7,'2012-11-10 15:29:46',1,13,'1','Contacts',2,'Changed order for element \"Name\".'),(8,'2012-11-10 16:20:59',1,13,'1','Contacts',2,'Added element \"Choice\".'),(9,'2012-11-10 17:15:28',1,13,'1','Contacts',2,'Changed order for element \"Choice\".'),(10,'2012-11-10 17:20:31',1,13,'1','Contacts',2,'Changed order for element \"Choice\". Changed order for element \"Name\".'),(11,'2012-11-10 17:20:53',1,13,'1','Contacts',2,'Changed order for element \"Name\".'),(12,'2012-11-10 17:38:34',1,13,'1','Contacts',2,'Changed order for element \"Choice\". Changed order for element \"Name\".'),(13,'2012-11-10 17:55:05',1,13,'1','Contacts',1,''),(14,'2012-11-10 18:15:08',1,13,'1','Contacts',1,''),(15,'2012-11-17 16:07:14',1,3,'2','fred',3,''),(16,'2012-11-17 21:02:53',1,13,'1','Image Test',2,'Changed image for element \"Image with text\".'),(17,'2012-11-17 21:41:12',1,13,'1','Image Test',2,'Changed image for element \"Image with text\".'),(18,'2012-11-17 21:52:57',1,13,'1','Image Test',2,'Changed image for element \"Thane Enterprises Inc.\".'),(19,'2012-11-17 21:56:36',1,13,'1','Image Test',2,'Changed klass for element \"Thane Enterprises Inc.\".'),(20,'2012-11-17 21:57:26',1,13,'1','Image Test',2,'Changed klass for element \"Thane Enterprises Inc.\".'),(21,'2012-11-17 21:59:23',1,13,'1','Image Test',2,'Changed klass for element \"Thane Enterprises Inc.\".'),(22,'2012-11-17 21:59:34',1,13,'1','Image Test',2,'Changed klass for element \"Thane Enterprises Inc.\".'),(23,'2012-11-17 21:59:50',1,13,'1','Image Test',2,'Changed klass for element \"Thane Enterprises Inc.\".'),(24,'2012-11-18 03:18:53',1,22,'1','Theme object',1,''),(25,'2012-11-18 03:27:24',1,13,'2','Sample Form',2,'Changed image for element \"Logo\".'),(26,'2012-11-18 03:30:53',1,13,'1','Sample Form',3,''),(27,'2012-11-18 03:31:12',1,22,'1','Original',2,'No fields changed.'),(28,'2012-11-18 03:31:30',1,22,'2','New',1,''),(29,'2012-11-18 03:31:47',1,13,'2','Sample Form',2,'Changed theme.'),(30,'2012-11-18 03:49:02',1,22,'2','New',2,'Changed code.'),(31,'2012-11-18 03:49:12',1,22,'3','Red',1,''),(32,'2012-11-18 03:49:19',1,22,'2','White',2,'Changed name.'),(33,'2012-11-18 03:51:08',1,22,'4','Flat',1,''),(34,'2012-11-18 03:52:40',1,22,'4','Flat',2,'Changed code.'),(35,'2012-11-18 03:55:05',1,22,'4','Flat with comic fonts',2,'Changed name and code.'),(36,'2012-11-18 03:56:09',1,22,'4','Flat with comic fonts',2,'Changed code.'),(37,'2012-11-18 03:57:21',1,22,'3','Psychedelic Colors',2,'Changed name and code.'),(38,'2012-11-18 03:58:17',1,22,'4','Flat with comic fonts',2,'Changed code.'),(39,'2012-11-18 03:59:40',1,22,'4','Flat with comic fonts',2,'Changed code.'),(40,'2012-11-18 04:01:10',1,22,'4','Flat with comic fonts',2,'Changed code.'),(41,'2012-11-18 04:01:45',1,22,'4','Flat with different font',2,'Changed name.'),(42,'2012-11-18 06:46:12',1,15,'5','Result object',3,''),(43,'2012-11-18 06:46:12',1,15,'4','Result object',3,''),(44,'2012-11-18 06:46:12',1,15,'3','Result object',3,''),(45,'2012-11-18 06:46:12',1,15,'2','Result object',3,''),(46,'2012-11-18 06:46:12',1,15,'1','Result object',3,''),(47,'2012-11-18 06:48:31',1,15,'8','Result object',3,''),(48,'2012-11-18 06:48:31',1,15,'7','Result object',3,''),(49,'2012-11-18 06:48:31',1,15,'6','Result object',3,''),(50,'2012-11-18 16:12:49',1,13,'2','Sample Form',2,'Changed created_by.'),(51,'2012-11-19 04:18:37',1,22,'1','Original',1,''),(52,'2012-11-19 05:42:09',1,6,'1','localhost',2,'Changed domain and name.'),(53,'2012-11-19 06:30:02',1,6,'1','localhost:8000',2,'Changed domain.'),(54,'2012-11-19 07:03:16',1,13,'1','Jump',2,'Changed created_by.'),(55,'2012-11-20 00:10:12',1,13,'1','Jump',2,'Changed image for element \"Single Image\". Changed image for element \"Image with Text on Left\". Changed image for element \"Image with Text on Right\".');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'site','sites','site'),(7,'log entry','admin','logentry'),(8,'Category','knowledge','category'),(9,'Article','knowledge','article'),(10,'Question','knowledge','question'),(11,'Response','knowledge','response'),(12,'screenshot','knowledge','screenshot'),(13,'form','forms','form'),(14,'element','forms','element'),(15,'result','forms','result'),(16,'value','forms','value'),(17,'facebook user','django_facebook','facebookuser'),(18,'facebook like','django_facebook','facebooklike'),(19,'facebook profile','django_facebook','facebookprofile'),(20,'open graph share','django_facebook','opengraphshare'),(21,'facebook invite','django_facebook','facebookinvite'),(22,'theme','forms','theme');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_facebook_facebook_invite`
--

DROP TABLE IF EXISTS `django_facebook_facebook_invite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_facebook_facebook_invite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `updated_at` datetime NOT NULL,
  `created_at` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `user_invited` varchar(255) NOT NULL,
  `message` longtext,
  `type` varchar(255) DEFAULT NULL,
  `wallpost_id` varchar(255) DEFAULT NULL,
  `error` tinyint(1) NOT NULL,
  `error_message` longtext,
  `last_attempt` datetime DEFAULT NULL,
  `reminder_wallpost_id` varchar(255) DEFAULT NULL,
  `reminder_error` tinyint(1) NOT NULL,
  `reminder_error_message` longtext,
  `reminder_last_attempt` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`user_invited`),
  KEY `django_facebook_facebook_invite_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_2487fc6` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_facebook_facebook_invite`
--

LOCK TABLES `django_facebook_facebook_invite` WRITE;
/*!40000 ALTER TABLE `django_facebook_facebook_invite` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_facebook_facebook_invite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_facebook_facebooklike`
--

DROP TABLE IF EXISTS `django_facebook_facebooklike`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_facebook_facebooklike` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `facebook_id` bigint(20) NOT NULL,
  `name` longtext,
  `category` longtext,
  `created_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`facebook_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_facebook_facebooklike`
--

LOCK TABLES `django_facebook_facebooklike` WRITE;
/*!40000 ALTER TABLE `django_facebook_facebooklike` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_facebook_facebooklike` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_facebook_facebookprofile`
--

DROP TABLE IF EXISTS `django_facebook_facebookprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_facebook_facebookprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `about_me` longtext,
  `facebook_id` bigint(20) DEFAULT NULL,
  `access_token` longtext,
  `facebook_name` varchar(255) DEFAULT NULL,
  `facebook_profile_url` longtext,
  `website_url` longtext,
  `blog_url` longtext,
  `date_of_birth` date DEFAULT NULL,
  `gender` varchar(1) DEFAULT NULL,
  `raw_data` longtext,
  `facebook_open_graph` tinyint(1) NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `facebook_id` (`facebook_id`),
  CONSTRAINT `user_id_refs_id_e9656a8b` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_facebook_facebookprofile`
--

LOCK TABLES `django_facebook_facebookprofile` WRITE;
/*!40000 ALTER TABLE `django_facebook_facebookprofile` DISABLE KEYS */;
INSERT INTO `django_facebook_facebookprofile` VALUES (2,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,'',3);
/*!40000 ALTER TABLE `django_facebook_facebookprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_facebook_facebookuser`
--

DROP TABLE IF EXISTS `django_facebook_facebookuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_facebook_facebookuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `facebook_id` bigint(20) NOT NULL,
  `name` longtext,
  `gender` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`facebook_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_facebook_facebookuser`
--

LOCK TABLES `django_facebook_facebookuser` WRITE;
/*!40000 ALTER TABLE `django_facebook_facebookuser` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_facebook_facebookuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_facebook_open_graph_share`
--

DROP TABLE IF EXISTS `django_facebook_open_graph_share`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_facebook_open_graph_share` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `action_domain` varchar(255) NOT NULL,
  `facebook_user_id` bigint(20) NOT NULL,
  `share_dict` longtext,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` int(10) unsigned DEFAULT NULL,
  `error_message` longtext,
  `last_attempt` datetime DEFAULT NULL,
  `retry_count` int(11) DEFAULT NULL,
  `share_id` varchar(255) DEFAULT NULL,
  `completed_at` datetime DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_facebook_open_graph_share_fbfc09f1` (`user_id`),
  KEY `django_facebook_open_graph_share_e4470c6e` (`content_type_id`),
  KEY `django_facebook_open_graph_share_3b1c9c31` (`created_at`),
  CONSTRAINT `content_type_id_refs_id_5c3b7c3e` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_40192e2e` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_facebook_open_graph_share`
--

LOCK TABLES `django_facebook_open_graph_share` WRITE;
/*!40000 ALTER TABLE `django_facebook_open_graph_share` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_facebook_open_graph_share` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_c25c2c28` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('513b5e03cb0e4816f639f5c05190452f','ODE1YzU4NTg4Mjg5NzIwM2U1ZDM0NzUyN2FlNmNmYzE0NjIyY2M4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2012-12-01 16:30:47'),('5813ec48bf7e7a605289bd9e85f9e0c9','N2ZkZDU1NWRhOTFlOGJjMDI1ZTI5YzE4YjJkZTcyMTc2NjE0MzVhYjqAAn1xAVUKdGVzdGNvb2tp\nZVUGd29ya2VkcQJzLg==\n','2012-12-07 20:21:54'),('7a31e4c0d4cbf54650298b0e8c870fe4','ODE1YzU4NTg4Mjg5NzIwM2U1ZDM0NzUyN2FlNmNmYzE0NjIyY2M4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2012-11-20 21:02:56'),('a23a590f08fa93d2b9fe85ebf80207b0','ODE1YzU4NTg4Mjg5NzIwM2U1ZDM0NzUyN2FlNmNmYzE0NjIyY2M4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2012-12-02 03:16:25'),('cb6084bbdd01164f366737c7be474744','ODE1YzU4NTg4Mjg5NzIwM2U1ZDM0NzUyN2FlNmNmYzE0NjIyY2M4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2012-12-01 16:07:00'),('e2f90efe759de7b651e5e5f4d72a816c','MWViZmM2YmY4ZjRkMDkwNGMwYjljNTY1NzA5M2FkMTk4NmI5Y2Y0MTqAAn1xAShVCnJldHVybl91\ncmlxAlggAAAAaHR0cDovL2xvY2FsaG9zdDo4MDAwL2Zvcm1zLzEteC9VCnRlc3Rjb29raWVVBndv\ncmtlZHUu\n','2012-12-08 06:14:29'),('ece44bab5d6f7c1389b512c8bc772c71','N2NhNzczYzBkOTNmMWYzM2ZlYzY4MmFmZWM0ZjQyMDQ4NWRkZWExYTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-12-01 16:07:34');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'localhost:8000','Localhost');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forms_element`
--

DROP TABLE IF EXISTS `forms_element`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forms_element` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `klass` varchar(2) NOT NULL,
  `required` tinyint(1) NOT NULL,
  `unique` tinyint(1) NOT NULL,
  `description` varchar(64) NOT NULL,
  `tooltip` varchar(64) NOT NULL,
  `order` int(11) NOT NULL,
  `image` varchar(100) NOT NULL,
  `details` varchar(128) NOT NULL,
  `form_id` int(11) NOT NULL,
  `required_group` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `forms_element_1d0aabf2` (`form_id`),
  CONSTRAINT `form_id_refs_id_a7646042` FOREIGN KEY (`form_id`) REFERENCES `forms_form` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forms_element`
--

LOCK TABLES `forms_element` WRITE;
/*!40000 ALTER TABLE `forms_element` DISABLE KEYS */;
INSERT INTO `forms_element` VALUES (1,'Name','TB',0,0,'','',3,'','',1,NULL),(2,'Description','TX',0,0,'','',2,'','',1,NULL),(3,'Single Image','IM',0,0,'','',1,'forms/images/parasol.jpg','',1,''),(4,'Image with Text on Left','IL',0,0,'','',4,'forms/images/clock.jpg','',1,''),(5,'Image with Text on Right','IR',0,0,'','',5,'forms/images/food.jpg','',1,''),(6,'Password','PB',0,0,'','',6,'','',1,NULL),(7,'A Text Area','TA',0,0,'','',7,'','',1,NULL),(8,'A dropdown box','DD',0,0,'','',8,'','Green, Orange, Purple',1,NULL),(9,'Radio Buttons','RD',0,0,'','',9,'','Big, Medium, Small',1,NULL),(10,'Your website URL','UL',0,0,'','',10,'','',1,NULL),(11,'Country','CT',0,0,'','',12,'','',1,NULL),(12,'Email Address','EM',0,0,'','',1,'','',1,NULL);
/*!40000 ALTER TABLE `forms_element` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forms_form`
--

DROP TABLE IF EXISTS `forms_form`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forms_form` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `success_url` varchar(64) NOT NULL,
  `submit_label` varchar(32) NOT NULL,
  `created_by_id` int(11) NOT NULL,
  `theme_id` int(11) NOT NULL,
  `key` varchar(32) DEFAULT NULL,
  `is_private` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `forms_form_b5de30be` (`created_by_id`),
  KEY `forms_form_1079d5be` (`theme_id`),
  CONSTRAINT `theme_id_refs_id_fee37f77` FOREIGN KEY (`theme_id`) REFERENCES `forms_theme` (`id`),
  CONSTRAINT `created_by_id_refs_id_705602e0` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forms_form`
--

LOCK TABLES `forms_form` WRITE;
/*!40000 ALTER TABLE `forms_form` DISABLE KEYS */;
INSERT INTO `forms_form` VALUES (1,'Jump','thankyou/','Save!',1,1,'TXJJgsZhGX83s1wOWm8mg1N2zETFyPy9',0);
/*!40000 ALTER TABLE `forms_form` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forms_result`
--

DROP TABLE IF EXISTS `forms_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forms_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `form_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `forms_result_1d0aabf2` (`form_id`),
  CONSTRAINT `form_id_refs_id_f1e1619c` FOREIGN KEY (`form_id`) REFERENCES `forms_form` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forms_result`
--

LOCK TABLES `forms_result` WRITE;
/*!40000 ALTER TABLE `forms_result` DISABLE KEYS */;
/*!40000 ALTER TABLE `forms_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forms_theme`
--

DROP TABLE IF EXISTS `forms_theme`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forms_theme` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `code` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forms_theme`
--

LOCK TABLES `forms_theme` WRITE;
/*!40000 ALTER TABLE `forms_theme` DISABLE KEYS */;
INSERT INTO `forms_theme` VALUES (1,'Original','body {\r\n/*    background: url(\"/static/img/black-stripe.gif\") repeat scroll 0 0 #282828;*/\r\n    background: none repeat scroll 0 0 #FAF0D9;\r\n}\r\n\r\n#container{\r\n}\r\n\r\n#left-panel{\r\n    width:200px;\r\n    padding: 15px;\r\n    float:left;\r\n}\r\n\r\n#content{\r\n    width:800px;\r\n    float:left;\r\n}\r\n\r\n.formWrapper {\r\n}\r\n.name-area{\r\n    width:50%;\r\n    float:left;\r\n}\r\n.preview-area{\r\n    width:50%;\r\n    float:right;\r\n}\r\n.toggle-text{\r\n    cursor:pointer;\r\n}\r\nli.toolbar-element{\r\n    list-style:none;\r\n    vertical-align:middle;\r\n}\r\nul.toolbar-elements{\r\n    padding:0;\r\n}\r\n.curved:before, .curved:after {\r\n    content: \"\";\r\n    position: absolute;\r\n    z-index: -2;\r\n    content: \"\";\r\n    position: absolute;\r\n    z-index: -2;\r\n}\r\n.curved:before {\r\n    border-radius: 100px 100px 100px 100px / 10px 10px 10px 10px;\r\n    box-shadow: 0 0 15px rgba(0, 0, 0, 0.6);\r\n    bottom: 0;\r\n    left: 10px;\r\n    right: 10px;\r\n    top: 0;\r\n    \r\n}\r\n.curved {\r\n    background: none repeat scroll 0 0 #FFFFFF;\r\n    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3), 0 0 40px rgba(0, 0, 0, 0.1) inset;\r\n    padding: 1em;\r\n    position: relative;\r\n    margin-bottom:10px;\r\n}');
/*!40000 ALTER TABLE `forms_theme` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forms_value`
--

DROP TABLE IF EXISTS `forms_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forms_value` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `element_id` int(11) NOT NULL,
  `value` varchar(128) NOT NULL,
  `result_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `forms_value_fe5d4041` (`element_id`),
  KEY `forms_value_3b529087` (`result_id`),
  CONSTRAINT `result_id_refs_id_61371cd6` FOREIGN KEY (`result_id`) REFERENCES `forms_result` (`id`),
  CONSTRAINT `element_id_refs_id_2ba3c794` FOREIGN KEY (`element_id`) REFERENCES `forms_element` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forms_value`
--

LOCK TABLES `forms_value` WRITE;
/*!40000 ALTER TABLE `forms_value` DISABLE KEYS */;
/*!40000 ALTER TABLE `forms_value` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `knowledge_article`
--

DROP TABLE IF EXISTS `knowledge_article`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `knowledge_article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `added` datetime NOT NULL,
  `lastchanged` datetime NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `email` varchar(75) DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `body` longtext,
  `status` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `knowledge_article_fbfc09f1` (`user_id`),
  KEY `knowledge_article_c9ad71dd` (`status`),
  CONSTRAINT `user_id_refs_id_b7bec9de` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `knowledge_article`
--

LOCK TABLES `knowledge_article` WRITE;
/*!40000 ALTER TABLE `knowledge_article` DISABLE KEYS */;
/*!40000 ALTER TABLE `knowledge_article` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `knowledge_article_categories`
--

DROP TABLE IF EXISTS `knowledge_article_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `knowledge_article_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `article_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `article_id` (`article_id`,`category_id`),
  KEY `category_id_refs_id_96030886` (`category_id`),
  CONSTRAINT `article_id_refs_id_27cd2169` FOREIGN KEY (`article_id`) REFERENCES `knowledge_article` (`id`),
  CONSTRAINT `category_id_refs_id_96030886` FOREIGN KEY (`category_id`) REFERENCES `knowledge_category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `knowledge_article_categories`
--

LOCK TABLES `knowledge_article_categories` WRITE;
/*!40000 ALTER TABLE `knowledge_article_categories` DISABLE KEYS */;
/*!40000 ALTER TABLE `knowledge_article_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `knowledge_category`
--

DROP TABLE IF EXISTS `knowledge_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `knowledge_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `added` datetime NOT NULL,
  `lastchanged` datetime NOT NULL,
  `title` varchar(255) NOT NULL,
  `slug` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `knowledge_category`
--

LOCK TABLES `knowledge_category` WRITE;
/*!40000 ALTER TABLE `knowledge_category` DISABLE KEYS */;
/*!40000 ALTER TABLE `knowledge_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `knowledge_question`
--

DROP TABLE IF EXISTS `knowledge_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `knowledge_question` (
  `article_ptr_id` int(11) NOT NULL,
  `locked` tinyint(1) NOT NULL,
  `screenshot_id` int(11) NOT NULL,
  PRIMARY KEY (`article_ptr_id`),
  KEY `knowledge_question_62c5ecba` (`screenshot_id`),
  CONSTRAINT `article_ptr_id_refs_id_1b323034` FOREIGN KEY (`article_ptr_id`) REFERENCES `knowledge_article` (`id`),
  CONSTRAINT `screenshot_id_refs_id_7d2b523` FOREIGN KEY (`screenshot_id`) REFERENCES `knowledge_screenshot` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `knowledge_question`
--

LOCK TABLES `knowledge_question` WRITE;
/*!40000 ALTER TABLE `knowledge_question` DISABLE KEYS */;
/*!40000 ALTER TABLE `knowledge_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `knowledge_response`
--

DROP TABLE IF EXISTS `knowledge_response`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `knowledge_response` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `added` datetime NOT NULL,
  `lastchanged` datetime NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `email` varchar(75) DEFAULT NULL,
  `question_id` int(11) NOT NULL,
  `body` longtext,
  `status` varchar(32) NOT NULL,
  `accepted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `knowledge_response_fbfc09f1` (`user_id`),
  KEY `knowledge_response_1f92e550` (`question_id`),
  KEY `knowledge_response_c9ad71dd` (`status`),
  CONSTRAINT `question_id_refs_article_ptr_id_2c85f294` FOREIGN KEY (`question_id`) REFERENCES `knowledge_question` (`article_ptr_id`),
  CONSTRAINT `user_id_refs_id_28ea9434` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `knowledge_response`
--

LOCK TABLES `knowledge_response` WRITE;
/*!40000 ALTER TABLE `knowledge_response` DISABLE KEYS */;
/*!40000 ALTER TABLE `knowledge_response` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `knowledge_screenshot`
--

DROP TABLE IF EXISTS `knowledge_screenshot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `knowledge_screenshot` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `image` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `knowledge_screenshot`
--

LOCK TABLES `knowledge_screenshot` WRITE;
/*!40000 ALTER TABLE `knowledge_screenshot` DISABLE KEYS */;
/*!40000 ALTER TABLE `knowledge_screenshot` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-11-24  1:36:32
