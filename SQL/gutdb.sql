-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: gutdb
-- ------------------------------------------------------
-- Server version	5.7.26

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
-- Table structure for table `diseases`
--

DROP TABLE IF EXISTS `diseases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `diseases` (
  `Disease_id` varchar(10) NOT NULL,
  `Disease_name` varchar(255) NOT NULL,
  `DOID` varchar(50) DEFAULT NULL,
  `Description` text,
  PRIMARY KEY (`Disease_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `diseases`
--

/*!40000 ALTER TABLE `diseases` DISABLE KEYS */;
INSERT INTO `diseases` VALUES ('D00001','chronic kidney disease','DOID:9256','A kidney failure that is characterized by the gradual loss of kidney function.'),('D00002','human immunodeficiency virus infectious disease','DOID:526','A viral infectious disease that results in destruction of immune system, leading to life-threatening opportunistic infections and cancers, has_material_basis_in Human immunodeficiency virus 1 or has_material_basis_in Human immunodeficiency virus 2, which are transmitted by sexual contact, transmitted by transfer of blood, semen, vaginal fluid, pre-ejaculate, or breast milk, transmitted by congenital method, and transmitted by contaminated needles.'),('D00003','inflammatory bowel disease','DOID:50589','An intestinal disease characterized by inflammation located in all parts of digestive tract.'),('D00004','colon cancer','DOID:219','A colorectal cancer that is located_in the colon.'),('D00005','fed with high-fructose diet',NULL,NULL),('D00006','acute myocardial infarction','DOID:9408',NULL),('D00007','fed with high-fat diet',NULL,NULL),('D00008','myocardial infarction','DOID:5844','A coronary artery disease characterized by myocardial cell death (myocardial necrosis) due to prolonged ischaemia.'),('D00009','cardiovascular cancer','DOID:176','An organ system cancer that located_in the heart and blood vessels.'),('D00010','type 1 endometrial carcinoma','DOID:2871','A endometrial cancer that is located_in the tissue lining the uterus.'),('D00011','colitis','DOID:0060180','An inflammatory bowel disease that involves inflammation located_in colon.'),('D00012','fed wih a defined low-choline diet',NULL,NULL),('D00013','colorectal cancer','DOID:9256','A large intestine cancer that is located_in the colon and/or located_in the rectum.'),('D00014','common variable immunodeficiency','DOID:12177','An agammaglobulinemia that is characterized by low Ig levels with phenotypically normal B cells that can proliferate but do not develop into Ig-producing cells and that esults in insufficient production of antibodies needed to respond to exposure of pathogens.'),('D00015','intestinal cancers',NULL,NULL),('D00016','renal fibrosis','DOID:0050855','A kidney disease that is characterized by progressive detrimental connective tissue deposition of the kidney parenchyma leading to deterioration of renal function.'),('D00017','inflammatory bowel disease','DOID:0050589','An intestinal disease characterized by inflammation located in all parts of digestive tract.'),('D00018','fed with Urolithin A',NULL,NULL),('D00019','type 1 diabetes','DOID:9744','A diabetes mellitus that is characterized by destruction of pancreatic beta cells resulting in absent or extremely low insulin production.'),('D00020','IgG4-related sclerosing cholangitis;primary sclerosing cholangitis','DOID:0060643','A sclerosing cholangitis characterized by fibroobliterative inflammation of the biliary tract, leading to cirrhosis and portal hypertension.'),('D00021','Alzheimer\'s disease','DOID:10652','A tauopathy that is characterized by memory lapses, confusion, emotional instability and progressive loss of mental ability and results in progressive memory loss, impaired thinking, disorientation, and changes in personality and mood starting and leads in advanced cases to a profound decline in cognitive and physical functioning and is marked histologically by the degeneration of brain neurons especially in the cerebral cortex and by the presence of neurofibrillary tangles and plaques containing beta-amyloid.'),('D00022','asthma','DOID:2841','A bronchial disease that is characterized by chronic inflammation and narrowing of the airways, which is caused by a combination of environmental and genetic factors.'),('D00023','type 2 diabetes mellitus','DOID:9352','a knowledgebase integrating heterogeneous connections associated with type 2 diabetes mellitus');
/*!40000 ALTER TABLE `diseases` ENABLE KEYS */;
