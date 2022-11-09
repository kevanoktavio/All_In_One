-- phpMyAdmin SQL Dump
-- version 4.9.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Sep 27, 2021 at 08:33 AM
-- Server version: 5.7.26
-- PHP Version: 7.4.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

SET foreign_key_checks = 0;
DROP TABLE IF EXISTS `Skill`, `Positions`, `Skill_set`, `Skill_Rewarded`, `Learning_Journey`;
SET foreign_key_checks = 1;
USE `is212_ALL_IN_ONE`;

CREATE TABLE `Skill` (
  `Skill_Name` varchar(50) PRIMARY KEY
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `Positions` (
  `Position_Name` varchar(50) PRIMARY KEY 
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- save skills required by positions and positions which require which skills
CREATE TABLE `Skill_Set` (
  `Skill_Set_ID` int PRIMARY KEY AUTO_INCREMENT,
  `Position_Name` varchar(50) NOT NULL,
  `Skill_Name` varchar(50) NOT NULL,
  FOREIGN KEY (`Position_Name`) REFERENCES Positions(`Position_Name`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`Skill_Name`) REFERENCES Skill(`Skill_Name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- save skills rewarded by a course and save courses which give which skill
CREATE TABLE `Skill_Rewarded` (
  `Skill_Rewarded_ID` int PRIMARY KEY AUTO_INCREMENT,
  `Skill_Name` varchar(50) NOT NULL,
  `Course_ID` varchar(20) NOT NULL,
  FOREIGN KEY (`Skill_Name`) REFERENCES Skill(`Skill_Name`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`Course_ID`) REFERENCES Course(`Course_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- save which positions aspired by staff and save which staff aspire to be which positions
CREATE TABLE `Learning_Journey` (
  `Learning_Journey_ID` int PRIMARY KEY AUTO_INCREMENT,
  `Staff_ID` int NOT NULL,
  `Position_Name` varchar(50) NOT NULL,
  `Skill_Name` varchar(50) NOT NULL,
  `Course_ID` varchar(20)  NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ------------------------------------ DUMMY DATA STARTS HERE -------------------------------------------------------------------------------

-- **Given tables from LMS are: Course, Role, Staff, Registration**

INSERT INTO `Positions` (`Position_Name`) VALUES
('Data Analyst'),
('Human Resource'),
('Head of Security'),
('Financial Analyst');

INSERT INTO `Skill` (`Skill_Name`) VALUES
('Python'),
('Advanced Python'),
('R'),
('Tableau'),
('Interpersonal Skills'),
('Martial Arts'),
('CISSP Certification'),
('OCSP Certification'),
('Team Building'),
('Public Speaking');

INSERT INTO `Skill_Set` (`Position_Name`, `Skill_Name`) VALUES
('Data Analyst', 'Python'),
('Data Analyst', 'R'),
('Data Analyst', 'Tableau'),
('Head of Security', 'Martial Arts'),
('Head of Security', 'CISSP Certification'),
('Head of Security', 'OCSP Certification'),
('Human Resource', 'Interpersonal Skills'),
('Human Resource', 'Team Building'),
('Human Resource', 'Public Speaking'),
('Financial Analyst', 'Python'),
('Financial Analyst', 'Advanced Python');

INSERT INTO `Skill_Rewarded` (`Skill_Name`, `Course_ID`) VALUES
("Python", 'FIN001'),
('Python', 'tch006'),
('Python', 'tch009'),
('Advanced Python', 'tch006'),	
('Advanced Python', 'tch008'),	
('R', 'COR001'),
('R', 'tch004'),
('Tableau', 'COR001'),
('Interpersonal Skills', 'MGT001'),
('Interpersonal Skills', 'SAL004'),
('Martial Arts', 'MGT001'),
('CISSP Certification', 'COR006'),
('CISSP Certification', 'COR002'),
('OCSP Certification', 'tch002'),
('OCSP Certification', 'tch003'),
('Team Building', 'COR004'),
('Team Building', 'MGT004'),
('Public Speaking', 'MGT001'),
('Public Speaking', 'COR006');

INSERT INTO `Learning_Journey` (`Staff_ID`, `Position_Name`, `Skill_Name`, `Course_ID`) VALUES
(130001,'Data Analyst', 'Python', 'FIN001'),
(130001, 'Data Analyst', 'R', 'tch004'),
(130001, 'Data Analyst', 'Tableau', 'COR001'),
(130001, 'Human Resource', 'Team Building', 'MGT004'),
(130001, 'Human Resource', 'Interpersonal Skills', 'MGT001'),
(130001, 'Human Resource', 'Public Speaking', 'COR006'),
(130002,'Data Analyst', 'Python', 'tch009'),
(130002, 'Data Analyst', 'R', 'tch004'),
(130002, 'Data Analyst', 'Tableau', 'COR001'),
(140002, 'Head of Security', 'Martial Arts', 'MGT001'),
(140002, 'Head of Security', 'CISSP Certification', 'COR002'),
(140002, 'Head of Security', 'OCSP Certification', 'tch003'),
(170233, 'Financial Analyst', 'Python', 'FIN001'),
(170233, 'Financial Analyst', 'Advanced Python', 'tch006'),
(170216, 'Financial Analyst', 'Python', 'tch009'),
(170216, 'Financial Analyst', 'Advanced Python', 'tch008'),
(170166, 'Financial Analyst', 'Python', 'tch006'),
(170166, 'Financial Analyst', 'Advanced Python', 'tch008'),
(160008, 'Human Resource', 'Team Building', 'COR004'),
(160008, 'Human Resource', 'Interpersonal Skills', 'SAL004'),
(160008, 'Human Resource', 'Public Speaking', 'MGT001'),
(160075, 'Human Resource', 'Team Building', 'MGT004'),
(160075, 'Human Resource', 'Interpersonal Skills', 'MGT001'),
(160075, 'Human Resource', 'Public Speaking', 'COR006'),
(160143, 'Human Resource', 'Team Building', 'MGT004'),
(160143, 'Human Resource', 'Interpersonal Skills', 'SAL004'),
(160143, 'Human Resource', 'Public Speaking', 'COR006');