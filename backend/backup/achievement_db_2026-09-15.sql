-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: achievement_db
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `achievement_attachments`
--

DROP TABLE IF EXISTS `achievement_attachments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `achievement_attachments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `achievement_id` int DEFAULT NULL,
  `file_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `file_path` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `file_size` bigint DEFAULT NULL,
  `file_type` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `uploaded_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `achievement_id` (`achievement_id`),
  CONSTRAINT `achievement_attachments_ibfk_1` FOREIGN KEY (`achievement_id`) REFERENCES `achievements` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `achievement_attachments`
--

LOCK TABLES `achievement_attachments` WRITE;
/*!40000 ALTER TABLE `achievement_attachments` DISABLE KEYS */;
INSERT INTO `achievement_attachments` VALUES (1,NULL,'大一新生校园适应优化设计方案.png','/uploads/6aa168b6d86a4dbc8f67036d4f32d101_png',4060431,'image/png','2026-08-01 07:20:18'),(2,NULL,'大一新生校园适应优化设计方案.png','/uploads/11d9b773aafe4fe18732d170122f4a78_png',4060431,'image/png','2026-08-01 07:21:08'),(3,12,'大一新生校园适应优化设计方案.png','/uploads/94397ed104a74f76b40c9b69a5df6c81_png',4060431,'image/png','2026-08-01 07:21:45'),(4,13,'屏幕截图 2026-08-03 144507.png','/uploads/37f714b3b24c445c981afbbda546aa8f_2026-08-03_144507.png',283147,'image/png','2026-09-07 06:39:40'),(5,14,'屏幕截图 2026-08-03 144507.png','/uploads/0de9347917874b30a8eb3ad17cbf5228_2026-08-03_144507.png',283147,'image/png','2026-09-11 08:36:13');
/*!40000 ALTER TABLE `achievement_attachments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `achievement_categories`
--

DROP TABLE IF EXISTS `achievement_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `achievement_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `main_category` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '一级分类',
  `sub_category` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '二级细分',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_category` (`main_category`,`sub_category`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='成果分类表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `achievement_categories`
--

LOCK TABLES `achievement_categories` WRITE;
/*!40000 ALTER TABLE `achievement_categories` DISABLE KEYS */;
INSERT INTO `achievement_categories` VALUES (1,'学科竞赛类','ACM','2026-07-08 03:53:28','2026-07-08 03:53:28'),(2,'学科竞赛类','数学建模','2026-07-08 03:53:28','2026-07-08 03:53:28'),(3,'学科竞赛类','互联网+','2026-07-08 03:53:28','2026-07-08 03:53:28'),(4,'学科竞赛类','挑战杯','2026-07-08 03:53:28','2026-07-08 03:53:28'),(5,'学科竞赛类','电子设计','2026-07-08 03:53:28','2026-07-08 03:53:28'),(6,'学科竞赛类','智能车','2026-07-08 03:53:28','2026-07-08 03:53:28'),(7,'学科竞赛类','其他','2026-07-08 03:53:28','2026-07-08 03:53:28'),(8,'学术论文类','SCI','2026-07-08 03:53:28','2026-07-08 03:53:28'),(9,'学术论文类','EI','2026-07-08 03:53:28','2026-07-08 03:53:28'),(10,'学术论文类','核心期刊','2026-07-08 03:53:28','2026-07-08 03:53:28'),(11,'学术论文类','普通期刊','2026-07-08 03:53:28','2026-07-08 03:53:28'),(12,'学术论文类','会议论文','2026-07-08 03:53:28','2026-07-08 03:53:28'),(13,'知识产权类','发明专利','2026-07-08 03:53:28','2026-07-08 03:53:28'),(14,'知识产权类','实用新型','2026-07-08 03:53:28','2026-07-08 03:53:28'),(15,'知识产权类','外观设计','2026-07-08 03:53:28','2026-07-08 03:53:28'),(16,'知识产权类','软件著作权','2026-07-08 03:53:28','2026-07-08 03:53:28'),(17,'科研项目类','国家级大创','2026-07-08 03:53:28','2026-07-08 03:53:28'),(18,'科研项目类','省级大创','2026-07-08 03:53:28','2026-07-08 03:53:28'),(19,'科研项目类','校级大创','2026-07-08 03:53:28','2026-07-08 03:53:28'),(20,'科研项目类','参与教师科研','2026-07-08 03:53:28','2026-07-08 03:53:28'),(21,'荣誉表彰类','国家奖学金','2026-07-08 03:53:28','2026-07-08 03:53:28'),(22,'荣誉表彰类','励志奖学金','2026-07-08 03:53:28','2026-07-08 03:53:28'),(23,'荣誉表彰类','三好学生','2026-07-08 03:53:28','2026-07-08 03:53:28'),(24,'荣誉表彰类','优秀干部','2026-07-08 03:53:28','2026-07-08 03:53:28'),(25,'荣誉表彰类','优秀团员','2026-07-08 03:53:28','2026-07-08 03:53:28'),(26,'技能证书类','英语四六级','2026-07-08 03:53:28','2026-07-08 03:53:28'),(27,'技能证书类','计算机等级','2026-07-08 03:53:28','2026-07-08 03:53:28'),(28,'技能证书类','教师资格证','2026-07-08 03:53:28','2026-07-08 03:53:28'),(29,'技能证书类','普通话','2026-07-08 03:53:28','2026-07-08 03:53:28'),(30,'技能证书类','职业资格证','2026-07-08 03:53:28','2026-07-08 03:53:28'),(31,'社会实践类','志愿服务','2026-07-08 03:53:28','2026-07-08 03:53:28'),(32,'社会实践类','社会实践','2026-07-08 03:53:28','2026-07-08 03:53:28'),(33,'社会实践类','社团活动','2026-07-08 03:53:28','2026-07-08 03:53:28');
/*!40000 ALTER TABLE `achievement_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `achievement_knowledge`
--

DROP TABLE IF EXISTS `achievement_knowledge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `achievement_knowledge` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sub_category` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `level` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `level_priority` int DEFAULT NULL,
  `keywords` text COLLATE utf8mb4_unicode_ci,
  `proof_required` text COLLATE utf8mb4_unicode_ci,
  `school_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `achievement_knowledge`
--

LOCK TABLES `achievement_knowledge` WRITE;
/*!40000 ALTER TABLE `achievement_knowledge` DISABLE KEYS */;
INSERT INTO `achievement_knowledge` VALUES (2,'全国大学生数学建模竞赛','学科竞赛类','数学建模','国家级',NULL,'数学建模,竞赛','获奖证书',NULL,NULL,NULL),(3,'互联网+大学生创新创业大赛','学科竞赛类','互联网+','国家级',NULL,'互联网+,创新创业','获奖证书',NULL,NULL,NULL),(4,'挑战杯大学生课外学术科技作品竞赛','学科竞赛类','挑战杯','国家级',NULL,'挑战杯,学术科技','获奖证书',NULL,NULL,NULL),(5,'全国大学生电子设计竞赛','学科竞赛类','电子设计','国家级',NULL,'电子设计,竞赛','获奖证书',NULL,NULL,NULL),(6,'全国大学生智能汽车竞赛','学科竞赛类','智能车','国家级',NULL,'智能车,竞赛','获奖证书',NULL,NULL,NULL),(7,'其他学科竞赛','学科竞赛类','其他','校级',NULL,'竞赛,其他','获奖证书',NULL,NULL,NULL),(8,'SCI收录论文','学术论文类','SCI','国际级',NULL,'SCI,论文,学术','期刊发表证明',NULL,NULL,NULL),(9,'EI收录论文','学术论文类','EI','国家级',NULL,'EI,论文,学术','期刊发表证明',NULL,NULL,NULL),(10,'中文核心期刊论文','学术论文类','核心期刊','省级',NULL,'核心期刊,论文','期刊发表证明',NULL,NULL,NULL),(11,'普通期刊论文','学术论文类','普通期刊','校级',NULL,'期刊,论文','期刊发表证明',NULL,NULL,NULL),(12,'学术会议论文','学术论文类','会议论文','省级',NULL,'会议论文','会议录用证明',NULL,NULL,NULL),(13,'发明专利','知识产权类','发明专利','国家级',NULL,'发明专利,知识产权','专利证书',NULL,NULL,NULL),(14,'实用新型专利','知识产权类','实用新型','省级',NULL,'实用新型,专利','专利证书',NULL,NULL,NULL),(15,'外观设计专利','知识产权类','外观设计','省级',NULL,'外观设计,专利','专利证书',NULL,NULL,NULL),(16,'软件著作权','知识产权类','软件著作权','省级',NULL,'软件著作权','著作权登记证书',NULL,NULL,NULL),(17,'国家级大学生创新创业训练计划','科研项目类','国家级大创','国家级',NULL,'大创,创新创业','立项通知书',NULL,NULL,NULL),(18,'省级大学生创新创业训练计划','科研项目类','省级大创','省级',NULL,'大创,创新创业','立项通知书',NULL,NULL,NULL),(19,'校级大学生创新创业训练计划','科研项目类','校级大创','校级',NULL,'大创,创新创业','立项通知书',NULL,NULL,NULL),(20,'参与教师科研项目','科研项目类','参与教师科研','校级',NULL,'科研项目,参与','项目证明',NULL,NULL,NULL),(21,'国家奖学金','荣誉表彰类','国家奖学金','国家级',NULL,'奖学金,国家','获奖证书',NULL,NULL,NULL),(22,'国家励志奖学金','荣誉表彰类','励志奖学金','国家级',NULL,'励志奖学金','获奖证书',NULL,NULL,NULL),(23,'三好学生','荣誉表彰类','三好学生','校级',NULL,'三好学生,表彰','获奖证书',NULL,NULL,NULL),(24,'优秀学生干部','荣誉表彰类','优秀干部','校级',NULL,'优秀干部,表彰','获奖证书',NULL,NULL,NULL),(25,'优秀共青团员','荣誉表彰类','优秀团员','校级',NULL,'优秀团员,表彰','获奖证书',NULL,NULL,NULL),(26,'大学英语四六级证书','技能证书类','英语四六级','校级',NULL,'英语,四六级','证书',NULL,NULL,NULL),(27,'计算机等级考试证书','技能证书类','计算机等级','校级',NULL,'计算机等级','证书',NULL,NULL,NULL),(28,'教师资格证','技能证书类','教师资格证','国家级',NULL,'教师资格证','证书',NULL,NULL,NULL),(29,'普通话水平测试证书','技能证书类','普通话','省级',NULL,'普通话','证书',NULL,NULL,NULL),(30,'职业资格证书','技能证书类','职业资格证','国家级',NULL,'职业资格','证书',NULL,NULL,NULL),(31,'志愿服务','社会实践类','志愿服务','校级',NULL,'志愿,服务','服务证明',NULL,NULL,NULL),(32,'社会实践活动','社会实践类','社会实践','校级',NULL,'社会实践','实践证明',NULL,NULL,NULL),(33,'社团活动','社会实践类','社团活动','校级',NULL,'社团,活动','活动证明',NULL,NULL,NULL),(35,'学科竞赛类','学科竞赛类','ACM','校级',0,'','获奖证书',0,'2026-08-01 13:21:35','2026-08-01 13:21:35');
/*!40000 ALTER TABLE `achievement_knowledge` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `achievements`
--

DROP TABLE IF EXISTS `achievements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `achievements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `teacher_id` int DEFAULT NULL,
  `main_category` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sub_category` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `level` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `achieved_date` date DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'pending',
  `submitted_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `reviewed_at` timestamp NULL DEFAULT NULL,
  `review_comment` text COLLATE utf8mb4_unicode_ci,
  `keywords` text COLLATE utf8mb4_unicode_ci COMMENT '关键词',
  `auditor_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `teacher_id` (`teacher_id`),
  CONSTRAINT `achievements_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  CONSTRAINT `achievements_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `achievements`
--

LOCK TABLES `achievements` WRITE;
/*!40000 ALTER TABLE `achievements` DISABLE KEYS */;
INSERT INTO `achievements` VALUES (5,1,3,'Xue Ke Jing Sai Lei','ACM','班级1','Xiao Ji','2026-06-30','1111111111','approved','2026-07-23 12:29:40','2026-07-23 12:32:39','1',NULL,3),(6,1,3,'Xue Ke Jing Sai Lei','ACM','成果2','Xiao Ji','2026-06-30','1111111111','rejected','2026-07-23 12:30:03','2026-07-23 12:32:47','2',NULL,3),(7,3,3,'Xue Ke Jing Sai Lei','ACM','成果3','Xiao Ji','2026-06-30','1111111111','approved','2026-07-23 12:31:32','2026-07-23 15:15:06','3',NULL,3),(8,3,3,'Xue Ke Jing Sai Lei','ACM','成果4','Xiao Ji','2026-06-30','1111111111','approved','2026-07-23 12:32:08','2026-07-23 15:14:53','4',NULL,1),(9,1,3,'Xue Ke Jing Sai Lei','ACM','成果5','Xiao Ji','2026-06-29','111111111111111111','approved','2026-07-23 15:21:44','2026-07-23 15:22:14','',NULL,1),(10,1,NULL,'Xue Ke Jing Sai Lei','ACM','成果6','Xiao Ji','2026-07-28','1111111111','rejected','2026-08-01 05:29:09',NULL,'班级已删除',NULL,NULL),(11,1,NULL,'Xue Ke Jing Sai Lei','ACM','成果7','Xiao Ji','2026-07-27','1111111111','rejected','2026-08-01 06:49:28',NULL,'班级已删除',NULL,NULL),(12,1,NULL,'Xue Ke Jing Sai Lei','ACM','成果8','Xiao Ji','2026-07-28','1111111111111','approved','2026-08-01 07:21:50','2026-09-07 00:58:27','6',NULL,3),(13,1,NULL,'Ji Neng Zheng Shu Lei','Pu Tong Hua','成果9','Sheng Ji','2026-09-08','11111111111','approved','2026-09-07 06:39:42','2026-09-07 06:41:22','m',NULL,3),(14,1,NULL,'Ji Neng Zheng Shu Lei','Ji Suan Ji Deng Ji','成果10','Guo Jia Ji','2026-08-03','6666666666','approved','2026-09-11 08:36:16','2026-09-11 08:36:48','666',NULL,3);
/*!40000 ALTER TABLE `achievements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `achievements_backup`
--

DROP TABLE IF EXISTS `achievements_backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `achievements_backup` (
  `id` int NOT NULL DEFAULT '0',
  `student_id` int NOT NULL,
  `teacher_id` int DEFAULT NULL,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `main_category` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sub_category` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `level` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `achieved_date` date DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'pending',
  `submitted_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `reviewed_at` timestamp NULL DEFAULT NULL,
  `review_comment` text COLLATE utf8mb4_unicode_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `achievements_backup`
--

LOCK TABLES `achievements_backup` WRITE;
/*!40000 ALTER TABLE `achievements_backup` DISABLE KEYS */;
INSERT INTO `achievements_backup` VALUES (1,1,NULL,'Quan Guo Da Xue Sheng Shu Xue Jian Mo Jing Sai Sheng Yi Deng Jiang','Xue Ke Jing Sai Lei','Shu Xue Jian Mo','Sheng Ji','2024-09-15','Can Jia Quan Guo Da Xue Sheng Shu Xue Jian Mo Jing Sai, Huo De Sheng Ji Yi Deng Jiang','approved','2026-07-03 07:21:56',NULL,NULL),(2,1,NULL,'Da Xue Ying Yu Liu Ji CET-6','Ji Neng Zheng Shu Lei','Ying Yu Si Liu Ji','Xiao Ji','2024-06-10','Tong Guo Da Xue Ying Yu Liu Ji Kao Shi','approved','2026-07-03 07:21:56',NULL,NULL),(3,1,NULL,'2023-2024 Xue Nian San Hao Xue Sheng','Rong Yu Biao Zhang Lei','San Hao Xue Sheng','Xiao Ji','2024-10-20','Huo Ping 2023-2024 Xue Nian Xiao Ji San Hao Xue Sheng','approved','2026-07-03 07:21:56',NULL,NULL),(4,2,NULL,'Hu Lian Wang + Da Xue Sheng Chuang Xin Chuang Ye Da Sai Sheng Ji Yin Jiang','Xue Ke Jing Sai Lei','Hu Lian Wang +','Sheng Ji','2024-08-20','Can Jia Hu Lian Wang + Da Xue Sheng Chuang Xin Chuang Ye Da Sai, Huo De Sheng Ji Yin Jiang','approved','2026-07-03 07:21:56',NULL,NULL),(5,2,NULL,'Zhi Hui Xiao Yuan Guan Li Xi Tong Ruan Jian Zhu Zuo Quan','Zhi Shi Chan Quan Lei','Ruan Jian Zhu Zuo Quan','Guo Jia Ji','2024-11-01','Shen Qing Bing Huo De Zhi Hui Xiao Yuan Guan Li Xi Tong Ruan Jian Zhu Zuo Quan','approved','2026-07-03 07:21:56',NULL,NULL),(6,2,NULL,'You Xiu Gong Qing Tuan Yuan','Rong Yu Biao Zhang Lei','You Xiu Tuan Yuan','Xiao Ji','2024-05-04','Huo Ping Xiao Ji You Xiu Gong Qing Tuan Yuan','approved','2026-07-03 07:21:56',NULL,NULL),(7,3,NULL,'Ji Yu Shen Du Xue Xi De Tu Xiang Shi Bie Yan Jiu','Xue Shu Lun Wen Lei','Pu Tong Qi Kan','Sheng Ji','2024-10-15','Zai Sheng Ji Qi Kan Fa Biao Xue Shu Lun Wen Yi Pian','approved','2026-07-03 07:21:56',NULL,NULL),(8,3,NULL,'Quan Guo Ji Suan Ji Deng Ji Kao Shi San Ji Shuo Ju Ku','Ji Neng Zheng Shu Lei','Ji Suan Ji Deng Ji','Guo Jia Ji','2024-03-20','Tong Guo Quan Guo Ji Suan Ji Deng Ji Kao Shi San Ji','approved','2026-07-03 07:21:56',NULL,NULL),(9,3,NULL,'Guo Jia Ji Da Chuang Xiang Mu Zhi Neng La Ji Fen Lei Xi Tong','Ke Yan Xiang Mu Lei','Guo Jia Ji Da Chuang','Guo Jia Ji','2024-12-01','Zhu Chi Guo Jia Ji Da Xue Sheng Chuang Xin Chuang Ye Xun Lian Ji Hua Xiang Mu','pending','2026-07-03 07:21:56',NULL,NULL),(10,4,NULL,'Tiao Zhan Bei Ke Wai Xue Shu Ke Ji Zuo Pin Jing Sai Sheng Er Deng Jiang','Xue Ke Jing Sai Lei','Tiao Zhan Bei','Sheng Ji','2024-06-30','Can Jia Tiao Zhan Bei Jing Sai, Huo De Sheng Ji Er Deng Jiang','approved','2026-07-03 07:21:56',NULL,NULL),(11,4,NULL,'Yi Zhong Xin Xing Zhi Neng Tai Deng Shi Yong Xin Xing Zhuan Li','Zhi Shi Chan Quan Lei','Shi Yong Xin Xing','Guo Jia Ji','2024-09-10','Shen Qing Bing Huo De Shi Yong Xin Xing Zhuan Li Yi Xiang','approved','2026-07-03 07:21:56',NULL,NULL),(12,4,NULL,'Guo Jia Jiang Xue Jin','Rong Yu Biao Zhang Lei','Guo Jia Jiang Xue Jin','Guo Jia Ji','2024-11-15','Huo De Guo Jia Jiang Xue Jin','approved','2026-07-03 07:21:56',NULL,NULL),(13,5,NULL,'ACM-ICPC Guo Ji Da Xue Sheng Cheng Xu She Ji Jing Sai Ya Zhou Qu Yu Sai Tong Jiang','Xue Ke Jing Sai Lei','ACM','Guo Ji Ji','2024-11-20','Can Jia ACM-ICPC Jing Sai, Huo De Ya Zhou Qu Yu Sai Tong Jiang','approved','2026-07-03 07:21:56',NULL,NULL),(14,5,NULL,'EI Hui Yi Lun Wen AI Zai Yi Liao Zhen Duan Zhong De Ying Yong','Xue Shu Lun Wen Lei','EI','Guo Jia Ji','2024-12-05','Fa Biao EI Hui Yi Lun Wen Yi Pian','pending','2026-07-03 07:21:56',NULL,NULL),(15,5,NULL,'Gao Zhong Xin Xi Ji Shu Jiao Shi Zi Ge Zheng','Ji Neng Zheng Shu Lei','Jiao Shi Zi Ge Zheng','Guo Jia Ji','2024-07-15','Huo De Gao Zhong Xin Xi Ji Shu Jiao Shi Zi Ge Zheng','approved','2026-07-03 07:21:56',NULL,NULL),(16,6,NULL,'Pu Tong Hua Shui Ping Ce Shi Er Ji Jia Deng','Ji Neng Zheng Shu Lei','Pu Tong Hua','Xiao Ji','2024-05-20','Tong Guo Pu Tong Hua Shui Ping Ce Shi Er Ji Jia Deng','approved','2026-07-03 07:21:56',NULL,NULL),(17,6,NULL,'Shu Qi San Xia Xiang She Hui Shi Jian You Xiu Ge Ren','She Hui Shi Jian Lei','Zhi Yuan Fu Wu','Xiao Ji','2024-08-30','Can Jia Shu Qi San Xia Xiang She Hui Shi Jian Huo Dong, Huo Ping You Xiu Ge Ren','approved','2026-07-03 07:21:56',NULL,NULL),(18,6,NULL,'Guo Jia Li Zhi Jiang Xue Jin','Rong Yu Biao Zhang Lei','Li Zhi Jiang Xue Jin','Guo Jia Ji','2024-11-15','Huo De Guo Jia Li Zhi Jiang Xue Jin','approved','2026-07-03 07:21:56',NULL,NULL);
/*!40000 ALTER TABLE `achievements_backup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_applications`
--

DROP TABLE IF EXISTS `class_applications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_applications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `class_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'pending',
  `applied_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `processed_at` timestamp NULL DEFAULT NULL,
  `processed_by` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `class_id` (`class_id`),
  KEY `processed_by` (`processed_by`),
  CONSTRAINT `class_applications_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  CONSTRAINT `class_applications_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `class_applications_ibfk_3` FOREIGN KEY (`processed_by`) REFERENCES `teachers` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_applications`
--

LOCK TABLES `class_applications` WRITE;
/*!40000 ALTER TABLE `class_applications` DISABLE KEYS */;
/*!40000 ALTER TABLE `class_applications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classes`
--

DROP TABLE IF EXISTS `classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classes` (
  `id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `department` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `advisor_id` int DEFAULT NULL,
  `grade` int DEFAULT NULL,
  `student_count` int DEFAULT '0',
  `is_locked` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `advisor_id` (`advisor_id`),
  CONSTRAINT `classes_ibfk_1` FOREIGN KEY (`advisor_id`) REFERENCES `teachers` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classes`
--

LOCK TABLES `classes` WRITE;
/*!40000 ALTER TABLE `classes` DISABLE KEYS */;
INSERT INTO `classes` VALUES ('CS2024-1','计算机2024级1班','计算机学院',3,2024,2,1,'2026-07-28 14:41:46'),('CS2024-2','计算机2024级2班','计算机学院',3,2024,0,0,'2026-07-28 14:41:46');
/*!40000 ALTER TABLE `classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_students`
--

DROP TABLE IF EXISTS `course_students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course_students` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_id` int NOT NULL,
  `student_id` int NOT NULL,
  `is_starred` tinyint(1) DEFAULT '0',
  `joined_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `course_id` (`course_id`,`student_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `course_students_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE,
  CONSTRAINT `course_students_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_students`
--

LOCK TABLES `course_students` WRITE;
/*!40000 ALTER TABLE `course_students` DISABLE KEYS */;
INSERT INTO `course_students` VALUES (5,9,1,0,'2026-09-07 06:40:48'),(6,11,1,0,'2026-09-08 02:58:04'),(7,11,3,0,'2026-09-08 02:58:04'),(8,11,4,0,'2026-09-08 02:58:04'),(10,10,1,0,'2026-09-08 04:03:09');
/*!40000 ALTER TABLE `course_students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `invite_code` varchar(6) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `teacher_id` int DEFAULT NULL,
  `type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'regular',
  `description` text COLLATE utf8mb4_unicode_ci,
  `max_students` int DEFAULT '100',
  `student_count` int DEFAULT '0',
  `is_locked` tinyint NOT NULL DEFAULT '0',
  `semester` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `invite_code` (`invite_code`),
  KEY `teacher_id` (`teacher_id`),
  CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (9,'11111','COURSE26090709J9','N2ETXQ',3,'regular','1111111111',50,1,0,'11111111','2026-09-07 06:40:22','2026-09-07 06:40:48'),(10,'22222','COURSE260908B4NY','BMDNDW',3,'regular','22222222222222',50,1,0,'2222222','2026-09-08 02:00:04','2026-09-08 06:19:12'),(11,'计算机2024级1班','CS2024-1',NULL,3,'regular','由原班级[CS2024-1]迁移',NULL,3,1,'2024级','2026-07-28 14:41:46','2026-09-08 02:58:04'),(12,'计算机2024级2班','CS2024-2',NULL,3,'regular','由原班级[CS2024-2]迁移',NULL,0,0,'2024级','2026-07-28 14:41:46','2026-09-08 02:58:04');
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `knowledge_base`
--

DROP TABLE IF EXISTS `knowledge_base`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `knowledge_base` (
  `id` int NOT NULL AUTO_INCREMENT,
  `source_achievement_id` int DEFAULT NULL COMMENT '来源成果ID（关联原成果）',
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '成果标题',
  `category_level1` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '一级分类',
  `category_level2` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '二级细分',
  `level` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '级别',
  `student_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '学生姓名',
  `class_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '班级',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '描述',
  `proof_material` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '证明材料备份路径',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '状态（固定为 approved）',
  `auditor_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '审核人',
  `audit_comment` text COLLATE utf8mb4_unicode_ci COMMENT '审核意见',
  `submitted_at` timestamp NULL DEFAULT NULL COMMENT '提交时间',
  `reviewed_at` timestamp NULL DEFAULT NULL COMMENT '审核时间',
  `created_at` timestamp NULL DEFAULT NULL COMMENT '录入知识库时间',
  `updated_at` timestamp NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `knowledge_base`
--

LOCK TABLES `knowledge_base` WRITE;
/*!40000 ALTER TABLE `knowledge_base` DISABLE KEYS */;
INSERT INTO `knowledge_base` VALUES (1,5,'班级1','Xue Ke Jing Sai Lei','ACM','Xiao Ji','王小明','','1111111111','','approved','周教师','1','2026-07-23 12:29:40','2026-07-23 12:32:39','2026-07-23 12:32:39','2026-07-23 12:32:39'),(2,8,'成果4','Xue Ke Jing Sai Lei','ACM','Xiao Ji','李四','','1111111111','','approved','李院长','4','2026-07-23 12:32:08','2026-07-23 15:14:53','2026-07-23 15:14:53','2026-07-23 15:14:53'),(3,7,'成果3','Xue Ke Jing Sai Lei','ACM','Xiao Ji','李四','','1111111111','','approved','周教师','3','2026-07-23 12:31:32','2026-07-23 15:15:06','2026-07-23 15:15:06','2026-07-23 15:15:06'),(4,9,'成果5','Xue Ke Jing Sai Lei','ACM','Xiao Ji','王小明','','111111111111111111','','approved','李院长','','2026-07-23 15:21:44','2026-07-23 15:22:14','2026-07-23 15:22:14','2026-07-23 15:22:14'),(5,12,'成果8','Xue Ke Jing Sai Lei','ACM','Xiao Ji','王小明','计算机2024级1班','1111111111111','','approved','周教师','6','2026-08-01 07:21:50','2026-09-07 00:58:27','2026-09-07 00:58:27','2026-09-07 00:58:27'),(6,13,'成果9','Ji Neng Zheng Shu Lei','Pu Tong Hua','Sheng Ji','王小明','计算机2024级1班','11111111111','','approved','周教师','m','2026-09-07 06:39:42','2026-09-07 06:41:22','2026-09-07 06:41:22','2026-09-07 06:41:22'),(7,14,'成果10','Ji Neng Zheng Shu Lei','Ji Suan Ji Deng Ji','Guo Jia Ji','王小明','11111','6666666666','','approved','周教师','666','2026-09-11 08:36:16','2026-09-11 08:36:48','2026-09-11 08:36:49','2026-09-11 08:36:49');
/*!40000 ALTER TABLE `knowledge_base` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `migration_class_to_course`
--

DROP TABLE IF EXISTS `migration_class_to_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `migration_class_to_course` (
  `class_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `course_id` int NOT NULL,
  `migrated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`class_id`),
  UNIQUE KEY `course_id` (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `migration_class_to_course`
--

LOCK TABLES `migration_class_to_course` WRITE;
/*!40000 ALTER TABLE `migration_class_to_course` DISABLE KEYS */;
INSERT INTO `migration_class_to_course` VALUES ('CS2024-1',11,'2026-09-08 10:58:04'),('CS2024-2',12,'2026-09-08 10:58:04');
/*!40000 ALTER TABLE `migration_class_to_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permissions`
--

DROP TABLE IF EXISTS `permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '权限码，如 student:view',
  `module` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模块名称',
  `action` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '权限操作名称',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '权限描述',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permissions`
--

LOCK TABLES `permissions` WRITE;
/*!40000 ALTER TABLE `permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proof_requirements`
--

DROP TABLE IF EXISTS `proof_requirements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proof_requirements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sub_category` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `proof_type` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_required` tinyint(1) DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proof_requirements`
--

LOCK TABLES `proof_requirements` WRITE;
/*!40000 ALTER TABLE `proof_requirements` DISABLE KEYS */;
/*!40000 ALTER TABLE `proof_requirements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_permissions`
--

DROP TABLE IF EXISTS `role_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `role_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_id` (`role_id`,`permission_id`),
  KEY `permission_id` (`permission_id`),
  CONSTRAINT `role_permissions_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE,
  CONSTRAINT `role_permissions_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_permissions`
--

LOCK TABLES `role_permissions` WRITE;
/*!40000 ALTER TABLE `role_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `role_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `is_system` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `permissions` text COLLATE utf8mb4_unicode_ci,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (6,'院系负责人',NULL,0,'2026-07-15 12:00:41','[\"student:add\", \"student:delete\", \"student:reset_pwd\", \"achievement:view\", \"achievement:audit\", \"course:create\", \"course:edit\", \"course:delete\", \"course:lock\", \"teacher:add\", \"teacher:edit\", \"teacher:delete\", \"teacher:audit\", \"team:create\", \"team:delete\", \"team:remove_member\"]','2026-09-08 03:39:47'),(7,'辅导员',NULL,0,'2026-07-15 12:00:41','[\"student:add\", \"student:delete\", \"student:reset_pwd\", \"achievement:view\", \"achievement:audit\", \"team:create\", \"team:delete\", \"team:remove_member\"]','2026-09-01 03:31:03'),(8,'教师',NULL,0,'2026-07-15 12:00:41','[\"student:add\", \"student:delete\", \"student:reset_pwd\", \"achievement:view\", \"achievement:audit\", \"course:create\", \"course:edit\", \"course:delete\", \"course:lock\", \"team:create\", \"team:delete\", \"team:remove_member\"]','2026-09-09 03:14:27'),(11,'助教',NULL,0,'2026-07-21 13:14:54','[\"student:add\", \"student:delete\", \"student:reset_pwd\", \"achievement:view\", \"achievement:audit\", \"course:create\", \"course:edit\", \"course:delete\", \"teacher:add\", \"teacher:edit\", \"teacher:delete\", \"teacher:audit\", \"team:create\", \"team:delete\", \"team:remove_member\"]','2026-09-08 03:39:47'),(12,'教务管理员',NULL,0,'2026-07-21 13:24:11','[\"student:add\", \"student:delete\", \"student:reset_pwd\", \"achievement:view\", \"achievement:audit\", \"course:create\", \"course:edit\", \"course:delete\", \"course:lock\", \"teacher:add\", \"teacher:edit\", \"teacher:delete\", \"teacher:audit\", \"team:create\", \"team:delete\", \"team:remove_member\"]','2026-09-08 03:39:47'),(13,'啥也不是',NULL,0,'2026-07-21 13:31:11','[]','2026-07-21 13:31:11');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `student_no` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `class_id` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `major` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `avatar` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `enrolled_at` date DEFAULT NULL,
  `department` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '院系',
  `id_card` varchar(18) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `student_no` (`student_no`),
  KEY `class_id` (`class_id`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `students_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,6,'s001001','CS2024-1','软件工程','13800138005','/uploads/avatars/6_ef1790ce7bea4897b4630bf3f3251f05.png',NULL,'e',NULL),(3,13,'s001002','CS2024-1',NULL,'',NULL,NULL,'a校','111'),(4,14,'TEST001','CS2024-1','测试专业',NULL,NULL,NULL,'测试院系',NULL),(6,31,'12345',NULL,NULL,'',NULL,NULL,'a校','1234'),(7,33,'1111',NULL,NULL,'',NULL,NULL,'a校','11111111111'),(8,34,'2222',NULL,NULL,'',NULL,NULL,'b校','22222'),(10,37,'3333',NULL,NULL,'',NULL,NULL,'b校','33333'),(11,38,'stu_t1',NULL,NULL,'',NULL,NULL,'a校','');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_logs`
--

DROP TABLE IF EXISTS `system_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `role` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `action_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `action_detail` text COLLATE utf8mb4_unicode_ci,
  `ip_address` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `result` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `level` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_logs`
--

LOCK TABLES `system_logs` WRITE;
/*!40000 ALTER TABLE `system_logs` DISABLE KEYS */;
INSERT INTO `system_logs` VALUES (3,6,'s001001','student','login','用户登录成功（student）','127.0.0.1','success','INFO','2026-09-15 03:29:08'),(4,1,'admin','admin','login','用户登录成功（admin）','127.0.0.1','success','INFO','2026-09-15 03:37:50'),(7,1,'admin','admin','login','用户登录成功（admin）','127.0.0.1','success','INFO','2026-09-15 03:38:04'),(9,1,'admin','admin','login','用户登录成功（admin）','127.0.0.1','success','INFO','2026-09-15 03:38:30'),(10,1,'admin','admin','login','用户登录成功（admin）','127.0.0.1','success','INFO','2026-09-15 03:39:15'),(11,1,'admin','admin','login','用户登录成功（admin）','127.0.0.1','success','INFO','2026-09-15 03:39:24'),(13,1,'admin','admin','login','用户登录成功（admin）','127.0.0.1','success','INFO','2026-09-15 03:39:32'),(14,1,'admin','admin','login','用户登录成功（admin）','127.0.0.1','success','INFO','2026-09-15 03:39:44'),(16,1,'admin','admin','login','用户登录成功（admin）','127.0.0.1','success','INFO','2026-09-15 03:40:10'),(18,6,'s001001','student','login','用户登录成功（student）','127.0.0.1','success','INFO','2026-09-15 03:46:21'),(20,1,'admin','admin','login','用户登录成功（admin）','127.0.0.1','success','INFO','2026-09-15 03:46:22');
/*!40000 ALTER TABLE `system_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teachers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `teacher_no` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `department` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `title` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `role` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'faculty',
  `department_id` int DEFAULT '0',
  `role_id` int DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'pending' COMMENT '账号状态：pending(待审核), approved(已通过)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `teacher_no` (`teacher_no`),
  KEY `fk_teacher_role` (`role_id`),
  CONSTRAINT `fk_teacher_role` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`),
  CONSTRAINT `teachers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teachers`
--

LOCK TABLES `teachers` WRITE;
/*!40000 ALTER TABLE `teachers` DISABLE KEYS */;
INSERT INTO `teachers` VALUES (1,2,'h001','计算机学院','院长','13800138001','院系负责人',0,6,'approved'),(3,4,'t001','计算机学院','讲师','13800138003','啥也不是',0,13,'approved'),(8,16,'t002','a校','','','教师',0,8,'approved'),(9,17,'1','1','1','1','院系负责人',0,6,'approved'),(14,32,'123456','a校','','','faculty',0,NULL,'pending'),(16,39,'tea_t1','a校','','','faculty',0,NULL,'approved');
/*!40000 ALTER TABLE `teachers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team_members`
--

DROP TABLE IF EXISTS `team_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `team_members` (
  `id` int NOT NULL AUTO_INCREMENT,
  `team_id` int NOT NULL,
  `teacher_id` int NOT NULL,
  `role` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '角色：leader(负责人), member(成员)',
  `joined_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `teacher_id` (`teacher_id`),
  KEY `team_members_ibfk_1` (`team_id`),
  CONSTRAINT `team_members_ibfk_1` FOREIGN KEY (`team_id`) REFERENCES `teams` (`id`) ON DELETE CASCADE,
  CONSTRAINT `team_members_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team_members`
--

LOCK TABLES `team_members` WRITE;
/*!40000 ALTER TABLE `team_members` DISABLE KEYS */;
INSERT INTO `team_members` VALUES (6,5,3,'leader','2026-07-29 09:46:11'),(8,7,1,'leader','2026-09-01 03:19:05'),(10,9,1,'leader','2026-09-01 03:57:41'),(11,5,1,'member','2026-09-07 02:12:55');
/*!40000 ALTER TABLE `team_members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teams`
--

DROP TABLE IF EXISTS `teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teams` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `creator_id` int DEFAULT NULL,
  `invite_code` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `join_method` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '加入方式：code(邀请码), qr(扫码), both(两者皆可)',
  `created_at` timestamp NULL DEFAULT NULL,
  `team_type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'other',
  `type` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT 'department' COMMENT '团队类型：department院系, subject_group科组, campus校区, grade年级, other其他',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `invite_code` (`invite_code`),
  KEY `creator_id` (`creator_id`),
  CONSTRAINT `teams_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `teachers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teams`
--

LOCK TABLES `teams` WRITE;
/*!40000 ALTER TABLE `teams` DISABLE KEYS */;
INSERT INTO `teams` VALUES (5,'计算机教学团队','',3,'V74LBACS','code','2026-07-29 09:46:11','department','department'),(7,'外语系教学团队','',1,'TFUGDIIV','code','2026-09-01 03:19:05','other','department'),(9,'2026级教学人员','',1,'PPOHFLIC','code','2026-09-01 03:57:41','other','grade');
/*!40000 ALTER TABLE `teams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` enum('student','teacher','admin') COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','pbkdf2:sha256:600000$4AEwUo8swAlDy0QC$d24ab864481db8ffd4763798aba57ee854eff73531fffde0eefb517ae2a63efb','admin','系统管理员',NULL,'2026-07-09 01:46:01'),(2,'h001','pbkdf2:sha256:600000$4AEwUo8swAlDy0QC$d24ab864481db8ffd4763798aba57ee854eff73531fffde0eefb517ae2a63efb','teacher','李院长',NULL,'2026-07-09 01:46:01'),(4,'t001','pbkdf2:sha256:600000$4AEwUo8swAlDy0QC$d24ab864481db8ffd4763798aba57ee854eff73531fffde0eefb517ae2a63efb','teacher','周教师',NULL,'2026-07-09 01:46:01'),(6,'s001001','pbkdf2:sha256:600000$NiApDBCJIxATjhvd$768e927e806f81e422614423bceab3edd30e67b8f69faa55541a0eda3f4b293c','student','王小明',NULL,'2026-07-09 01:46:01'),(10,'test_student003','pbkdf2:sha256:600000$VdkUeqn7HigYlGhQ$a87a4e03cf9fcae9c1b672c135eb24600f4483304d40a74f11a231aa54648c99','student','test',NULL,'2026-07-21 11:16:02'),(13,'s001002','pbkdf2:sha256:600000$Q9i3UVrjGBlAXAsB$daac8437f1814e21ae5752d4f7bc5b420b1d616ca4ed29e41ecd22ae01507312','student','李四',NULL,'2026-07-23 12:21:17'),(14,'teststu001','pbkdf2:sha256:600000$qsLQfCpNwVhqzmEN$cf04695a1e6f259c545dca96a849172a8382ba16510a142eddec8964e25a30b3','student','测试学生',NULL,'2026-09-01 02:19:59'),(16,'t002','pbkdf2:sha256:600000$QDoacxawIDc3QcNz$e0244a29bd7cb75193c158943288c9ff03f2903fc6b440fd29653f1513cc378c','teacher','陈教师',NULL,'2026-09-07 02:26:03'),(17,'1','pbkdf2:sha256:600000$PqjFMLhXg7feH8Py$f83f9b18a77cf063f4aea2837a91f0e2cc6162c989988d5eec9a80b09601914f','teacher','1',NULL,'2026-09-08 09:16:47'),(31,'12345','pbkdf2:sha256:600000$bgVxcsb9DzqYnefU$48cbc6a2133e76ce2e738d6d11907cca022fc3d4d96d1120f74ff63546260b6d','student','q\'q\'q\'q',NULL,'2026-09-09 01:58:58'),(32,'123456','pbkdf2:sha256:600000$FLMW4tVmoczS8u5a$22161c4838a300264b6f947ffe9b1436475fac05587a99498c950ea559fb5efb','teacher','1wr',NULL,'2026-09-09 01:59:19'),(33,'1111','pbkdf2:sha256:600000$xflMoaJ3FN1owsLt$a97fb51d06ad6200df713d376e005ea4d735f81732a7c9cce2960dff1c0131ef','student','111',NULL,'2026-09-09 02:03:17'),(34,'2222','pbkdf2:sha256:600000$EHkWbWrldAZSPZp8$7f2602dafe62e5f573105093e025e48d635dcf4193833819cc4d7b596092646f','student','2222',NULL,'2026-09-09 02:03:41'),(37,'3333','pbkdf2:sha256:600000$d4BedIQTbNumWX0E$d32593d7ba6dc59cea241c5ee87923476253c98055cf55073b060b9dee4999ca','student','3333',NULL,'2026-09-09 02:17:03'),(38,'stu_t1','pbkdf2:sha256:600000$Kqir72eB4Qz7IPV1$fce427913e810c879abbc4b7288004d2ab795ed9bb2b5cefc0d1207f9fbd701b','student','学生一',NULL,'2026-09-09 02:23:56'),(39,'tea_t1','pbkdf2:sha256:600000$V7FKF3BE5yAiNoKG$8455a764fd721506d517b52d67eaf7d6deba17fa3fef6fba26d9bc598842b1af','teacher','教师一',NULL,'2026-09-09 02:23:56');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `verification_codes`
--

DROP TABLE IF EXISTS `verification_codes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `verification_codes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(6) COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires_at` timestamp NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `verification_codes`
--

LOCK TABLES `verification_codes` WRITE;
/*!40000 ALTER TABLE `verification_codes` DISABLE KEYS */;
INSERT INTO `verification_codes` VALUES (1,'13729243361','707304','2026-07-21 11:21:18','2026-07-21 11:16:18');
/*!40000 ALTER TABLE `verification_codes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'achievement_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-15 11:49:08
