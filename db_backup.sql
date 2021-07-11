-- MySQL dump 10.13  Distrib 8.0.25, for Win64 (x86_64)
--
-- Host: localhost    Database: lifechoicesonline
-- ------------------------------------------------------
-- Server version	8.0.25

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
-- Table structure for table `emergency`
--

DROP TABLE IF EXISTS `emergency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emergency` (
  `IDNum` varchar(255) DEFAULT NULL,
  `NextOfKin` varchar(255) NOT NULL,
  `NextOfKinNum` int NOT NULL,
  `EmergencyID` int unsigned NOT NULL AUTO_INCREMENT,
  `UserID` int unsigned NOT NULL,
  PRIMARY KEY (`EmergencyID`),
  KEY `UserID` (`UserID`),
  CONSTRAINT `emergency_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `register` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emergency`
--

LOCK TABLES `emergency` WRITE;
/*!40000 ALTER TABLE `emergency` DISABLE KEYS */;
INSERT INTO `emergency` VALUES ('9804205251081','Delaine Awood',836967357,33,39),('9512285835083','Justin Calvert',679150663,34,40),('9610055082082','Abdullah Isaacs',679150663,35,41),('0002035200084','Uthmaan Breda',794637741,36,42),('9609095470083','Adul-Malik Mohamed',764971338,37,43);
/*!40000 ALTER TABLE `emergency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `register`
--

DROP TABLE IF EXISTS `register`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `register` (
  `FullName` varchar(255) NOT NULL,
  `IDNumber` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `CellNum` int NOT NULL,
  `Unit` varchar(255) DEFAULT NULL,
  `UserID` int unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `register`
--

LOCK TABLES `register` WRITE;
/*!40000 ALTER TABLE `register` DISABLE KEYS */;
INSERT INTO `register` VALUES ('Jeandre Awood','9804205251081','lifechoices',835851644,'Staff',39),('Abdullah Isaacs','9512285835083','fortnite',734425442,'Academy',40),('Justin Calvert','9610055082082','cars',679150663,'Academy',41),('Adul-Malik Mohamed','0002035200084','uthmaan',764971338,'Academy',42),('Uthmaan Breda','9609095470083','adullyboi',794637741,'Academy',43);
/*!40000 ALTER TABLE `register` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timesheet`
--

DROP TABLE IF EXISTS `timesheet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timesheet` (
  `Tracker` int unsigned NOT NULL AUTO_INCREMENT,
  `IDNum` varchar(255) DEFAULT NULL,
  `LoggedInDate` date DEFAULT NULL,
  `LoggedInTime` time DEFAULT NULL,
  `LoggedOutDate` date DEFAULT NULL,
  `LoggedOutTime` time DEFAULT NULL,
  `UserID` int unsigned NOT NULL,
  PRIMARY KEY (`Tracker`),
  KEY `UserID` (`UserID`),
  CONSTRAINT `timesheet_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `register` (`UserID`),
  CONSTRAINT `timesheet_ibfk_2` FOREIGN KEY (`UserID`) REFERENCES `register` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timesheet`
--

LOCK TABLES `timesheet` WRITE;
/*!40000 ALTER TABLE `timesheet` DISABLE KEYS */;
INSERT INTO `timesheet` VALUES (14,'9804205251081','2021-07-11','02:57:29','2021-07-11','02:57:29',39),(15,'9512285835083','2021-07-11','02:57:29','2021-07-11','02:57:29',40),(16,'9610055082082','2021-07-11','02:57:29','2021-07-11','02:57:29',41),(17,'0002035200084','2021-07-11','02:57:29','2021-07-11','02:57:29',42),(18,'9609095470083','2021-07-11','02:57:29','2021-07-11','02:57:29',43);
/*!40000 ALTER TABLE `timesheet` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-11  3:46:34
