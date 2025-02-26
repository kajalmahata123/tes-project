-- MySQL dump 10.13  Distrib 5.7.41, for osx10.18 (x86_64)
--
-- Host: 103.185.74.157    Database: smart_ql
-- ------------------------------------------------------
-- Server version	8.0.33

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
-- Table structure for table `audit_logs`
--

DROP TABLE IF EXISTS `audit_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `audit_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `connection_id` int DEFAULT NULL,
  `action` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `details` json DEFAULT NULL,
  `ip_address` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_agent` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_audit_connection` (`connection_id`),
  KEY `idx_audit_action` (`action`),
  KEY `idx_audit_created` (`created_at`),
  CONSTRAINT `audit_logs_ibfk_1` FOREIGN KEY (`connection_id`) REFERENCES `database_connections` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_logs`
--

LOCK TABLES `audit_logs` WRITE;
/*!40000 ALTER TABLE `audit_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `audit_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `connection_types`
--

DROP TABLE IF EXISTS `connection_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `connection_types` (
  `type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `connection_types`
--

LOCK TABLES `connection_types` WRITE;
/*!40000 ALTER TABLE `connection_types` DISABLE KEYS */;
INSERT INTO `connection_types` VALUES ('cloud_service'),('direct'),('iam'),('service_account'),('ssh_tunnel');
/*!40000 ALTER TABLE `connection_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `database_configs`
--

DROP TABLE IF EXISTS `database_configs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_configs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `connection_id` int NOT NULL,
  `host` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `port` int DEFAULT NULL,
  `database_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `db_schema` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `params` json DEFAULT NULL,
  `connection_timeout` int DEFAULT '30',
  `query_timeout` int DEFAULT '60',
  `pool_size` int DEFAULT '5',
  `max_overflow` int DEFAULT '10',
  `pool_timeout` int DEFAULT '30',
  `pool_recycle` int DEFAULT '1800',
  `ssl_enabled` tinyint(1) DEFAULT '0',
  `ssl_verify` tinyint(1) DEFAULT '1',
  `ssl_ca` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_configs_connection` (`connection_id`),
  CONSTRAINT `database_configs_ibfk_1` FOREIGN KEY (`connection_id`) REFERENCES `database_connections` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `database_configs`
--

LOCK TABLES `database_configs` WRITE;
/*!40000 ALTER TABLE `database_configs` DISABLE KEYS */;
INSERT INTO `database_configs` VALUES (22,22,'103.185.74.157',3306,'alpha_ai_service',NULL,'{}',30,60,5,10,30,1800,0,1,NULL,'2025-01-20 11:03:43','2025-01-20 11:03:43'),(23,23,'127.0.0.1',3306,'TestDB',NULL,'{}',30,60,5,10,30,1800,0,1,NULL,'2025-01-29 10:59:40','2025-01-29 10:59:40'),(24,24,'mmxcmx,m,xc',3306,'xzlmlmxzlmxm',NULL,'{}',30,60,5,10,30,1800,0,1,NULL,'2025-02-02 02:13:15','2025-02-02 02:13:15'),(25,25,'cxnknkxcnkxcnn',3306,'dcncdnnxcn',NULL,'{}',30,60,5,10,30,1800,0,1,NULL,'2025-02-02 06:04:44','2025-02-02 06:04:44'),(26,26,'cxkkxckcxknkncxnk',3308,'ckckjvkcxkcvkxk',NULL,'{}',30,60,5,10,30,1800,0,1,NULL,'2025-02-02 06:52:27','2025-02-02 06:52:27'),(27,27,'cxkkxckcxknkncxnk',3308,'ckckjvkcxkcvkxk',NULL,'{}',30,60,5,10,30,1800,0,1,NULL,'2025-02-02 06:52:57','2025-02-02 06:52:57'),(28,28,'sxkncknxkncnk',3306,'xjxcjlcjcd',NULL,'{}',30,60,5,10,30,1800,0,1,NULL,'2025-02-02 07:21:53','2025-02-02 07:21:53');
/*!40000 ALTER TABLE `database_configs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `database_connections`
--

DROP TABLE IF EXISTS `database_connections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_connections` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `vendor` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `connection_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `last_connected_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `connection_type` (`connection_type`),
  KEY `idx_connections_vendor` (`vendor`),
  KEY `idx_connections_active` (`is_active`),
  KEY `idx_connections_name` (`name`),
  CONSTRAINT `database_connections_ibfk_1` FOREIGN KEY (`vendor`) REFERENCES `database_vendors` (`vendor`),
  CONSTRAINT `database_connections_ibfk_2` FOREIGN KEY (`connection_type`) REFERENCES `connection_types` (`type`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `database_connections`
--

LOCK TABLES `database_connections` WRITE;
/*!40000 ALTER TABLE `database_connections` DISABLE KEYS */;
INSERT INTO `database_connections` VALUES (22,'Alpha AI Service','','MYSQL','DIRECT',1,NULL,'2025-01-20 11:03:43','2025-01-20 11:03:43'),(23,'Test122','','MYSQL','DIRECT',1,NULL,'2025-01-29 10:59:40','2025-01-29 10:59:40'),(24,'xmmxcmxmxm','','MYSQL','DIRECT',1,NULL,'2025-02-02 02:13:15','2025-02-02 02:13:15'),(25,'dcnkxkcnkdc','','MYSQL','DIRECT',1,NULL,'2025-02-02 06:04:44','2025-02-02 06:04:44'),(26,'cdjnkcdkncdnkdc','','MYSQL','DIRECT',1,NULL,'2025-02-02 06:52:27','2025-02-02 06:52:27'),(27,'cdjnkcdkncdnkdc','','MYSQL','DIRECT',1,NULL,'2025-02-02 06:52:57','2025-02-02 06:52:57'),(28,'sdljsdjkcdj','','MYSQL','DIRECT',1,NULL,'2025-02-02 07:21:52','2025-02-02 07:21:52');
/*!40000 ALTER TABLE `database_connections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `database_credentials`
--

DROP TABLE IF EXISTS `database_credentials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_credentials` (
  `id` int NOT NULL AUTO_INCREMENT,
  `connection_id` int NOT NULL,
  `username` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `access_key` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `secret_key` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `token` text COLLATE utf8mb4_unicode_ci,
  `service_account_json` json DEFAULT NULL,
  `certificate` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_credentials_connection` (`connection_id`),
  CONSTRAINT `database_credentials_ibfk_1` FOREIGN KEY (`connection_id`) REFERENCES `database_connections` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `database_credentials`
--

LOCK TABLES `database_credentials` WRITE;
/*!40000 ALTER TABLE `database_credentials` DISABLE KEYS */;
INSERT INTO `database_credentials` VALUES (22,22,'root','Onlykajal111#',NULL,NULL,NULL,'null',NULL,'2025-01-20 11:03:43','2025-01-20 11:03:43'),(23,23,'test','testeee',NULL,NULL,NULL,'null',NULL,'2025-01-29 10:59:40','2025-01-29 10:59:40'),(24,24,'zxmmzxmmxm','mzcxmnmnlcxmcxn',NULL,NULL,NULL,'null',NULL,'2025-02-02 02:13:15','2025-02-02 02:13:15'),(25,25,'xclnnxcnxcn','xcjocxjkjkcxjkjcx',NULL,NULL,NULL,'null',NULL,'2025-02-02 06:04:44','2025-02-02 06:04:44'),(26,26,'xcknkncxnkcxnk','xcknkcxnkcxnkcx',NULL,NULL,NULL,'null',NULL,'2025-02-02 06:52:27','2025-02-02 06:52:27'),(27,27,'xcknkncxnkcxnk','xcknkcxnkcxnkcx',NULL,NULL,NULL,'null',NULL,'2025-02-02 06:52:57','2025-02-02 06:52:57'),(28,28,'xcjkjcjckcxjkcx','xcjocxjkhxckhcjkx',NULL,NULL,NULL,'null',NULL,'2025-02-02 07:21:53','2025-02-02 07:21:53');
/*!40000 ALTER TABLE `database_credentials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `database_health`
--

DROP TABLE IF EXISTS `database_health`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_health` (
  `id` int NOT NULL AUTO_INCREMENT,
  `connection_id` int NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `uptime` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `latency` int DEFAULT NULL,
  `connections` int DEFAULT NULL,
  `last_error` text COLLATE utf8mb4_unicode_ci,
  `last_checked_at` timestamp NOT NULL,
  `consecutive_failures` int DEFAULT '0',
  `metrics` json DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_health_connection` (`connection_id`),
  KEY `idx_health_status` (`status`),
  KEY `idx_health_checked` (`last_checked_at`),
  CONSTRAINT `database_health_ibfk_1` FOREIGN KEY (`connection_id`) REFERENCES `database_connections` (`id`) ON DELETE CASCADE,
  CONSTRAINT `database_health_ibfk_2` FOREIGN KEY (`status`) REFERENCES `health_statuses` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `database_health`
--

LOCK TABLES `database_health` WRITE;
/*!40000 ALTER TABLE `database_health` DISABLE KEYS */;
INSERT INTO `database_health` VALUES (10,22,'WARNING','30.95 days',1675,2,NULL,'2025-02-07 01:45:51',0,'{\"uptime\": \"30.95 days\", \"bytes_sent\": \"212494665\", \"bytes_received\": \"67362570\", \"total_connections\": 36, \"active_connections\": 2, \"queries_per_second\": 0.11045898705196752}','2025-01-20 11:03:49','2025-02-07 01:45:51'),(11,23,'HEALTHY','100%',0,0,NULL,'2025-01-29 10:59:40',0,'{}','2025-01-29 10:59:40','2025-01-29 10:59:40'),(12,24,'HEALTHY','100%',0,0,NULL,'2025-02-02 02:13:15',0,'{}','2025-02-02 02:13:15','2025-02-02 02:13:15'),(13,25,'HEALTHY','100%',0,0,NULL,'2025-02-02 06:04:45',0,'{}','2025-02-02 06:04:45','2025-02-02 06:04:45'),(14,26,'HEALTHY','100%',0,0,NULL,'2025-02-02 06:52:28',0,'{}','2025-02-02 06:52:28','2025-02-02 06:52:28'),(15,27,'HEALTHY','100%',0,0,NULL,'2025-02-02 06:52:58',0,'{}','2025-02-02 06:52:58','2025-02-02 06:52:58'),(16,28,'HEALTHY','100%',0,0,NULL,'2025-02-02 07:21:54',0,'{}','2025-02-02 07:21:54','2025-02-02 07:21:54');
/*!40000 ALTER TABLE `database_health` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `database_vendors`
--

DROP TABLE IF EXISTS `database_vendors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_vendors` (
  `vendor` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`vendor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `database_vendors`
--

LOCK TABLES `database_vendors` WRITE;
/*!40000 ALTER TABLE `database_vendors` DISABLE KEYS */;
INSERT INTO `database_vendors` VALUES ('clickhouse'),('mongodb'),('mssql'),('mysql'),('oracle'),('postgresql'),('redshift'),('snowflake');
/*!40000 ALTER TABLE `database_vendors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `health_statuses`
--

DROP TABLE IF EXISTS `health_statuses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `health_statuses` (
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `health_statuses`
--

LOCK TABLES `health_statuses` WRITE;
/*!40000 ALTER TABLE `health_statuses` DISABLE KEYS */;
INSERT INTO `health_statuses` VALUES ('critical'),('healthy'),('warning');
/*!40000 ALTER TABLE `health_statuses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schema_analyses`
--

DROP TABLE IF EXISTS `schema_analyses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `schema_analyses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `connection_id` int NOT NULL,
  `schema_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `schema_analysis` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `analyzed_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'completed',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_schema_analyses_connection` (`connection_id`),
  CONSTRAINT `schema_analyses_ibfk_1` FOREIGN KEY (`connection_id`) REFERENCES `database_connections` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schema_analyses`
--

LOCK TABLES `schema_analyses` WRITE;
/*!40000 ALTER TABLE `schema_analyses` DISABLE KEYS */;
/*!40000 ALTER TABLE `schema_analyses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `table_analyses`
--

DROP TABLE IF EXISTS `table_analyses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `table_analyses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `schema_analysis_id` int NOT NULL,
  `table_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `analysis` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `analyzed_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_table_analyses_schema` (`schema_analysis_id`),
  CONSTRAINT `table_analyses_ibfk_1` FOREIGN KEY (`schema_analysis_id`) REFERENCES `schema_analyses` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `table_analyses`
--

LOCK TABLES `table_analyses` WRITE;
/*!40000 ALTER TABLE `table_analyses` DISABLE KEYS */;
/*!40000 ALTER TABLE `table_analyses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `hashed_password` varchar(255) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `is_superuser` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_email` (`email`),
  UNIQUE KEY `idx_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'user@example.com','testuser','$2b$12$AMu/xXHF0iyWUfJy3Rrliuva7oLLBJZaw33YgMMjFUABuE5ho.3Aq',1,0,'2025-01-14 16:18:13',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'smart_ql'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-27  1:54:18
