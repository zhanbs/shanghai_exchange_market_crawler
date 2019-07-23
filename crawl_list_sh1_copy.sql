/*
Navicat MySQL Data Transfer

Source Server         : lcoalhost
Source Server Version : 80016
Source Host           : localhost:3306
Source Database       : listed_company

Target Server Type    : MYSQL
Target Server Version : 80016
File Encoding         : 65001

Date: 2019-07-23 17:12:34
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for crawl_list_sh1_copy
-- ----------------------------
DROP TABLE IF EXISTS `crawl_list_sh1_copy`;
CREATE TABLE `crawl_list_sh1_copy` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `SECURITY_CODE_A` varchar(30) NOT NULL,
  `COMPANY_ABBR` varchar(30) NOT NULL,
  `AREA_NAME_DESC` varchar(30) NOT NULL,
  `CSRC_CODE_DESC` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `LEGAL_REPRESENTATIVE` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2374 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
