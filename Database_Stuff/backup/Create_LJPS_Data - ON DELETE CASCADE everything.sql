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
DROP TABLE IF EXISTS `SKill`, `Positions`, `Skill_set`, `Skill_Rewarded`, `Learning_Journey`;
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
  `Course_ID` varchar(20)  NOT NULL,
  FOREIGN KEY (`Staff_ID`) REFERENCES Staff(`Staff_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`Position_Name`) REFERENCES Positions(`Position_Name`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`Skill_Name`) REFERENCES Skill(`Skill_Name`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`Course_ID`) REFERENCES Course(`Course_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ------------------------------------ DUMMY DATA STARTS HERE -------------------------------------------------------------------------------

-- **Given tables from LMS are: Course, Role, Staff, Registration**

INSERT INTO `Positions` (`Position_Name`) VALUES
('Data Analyst'),
('Human Resource'),
('Head of Security');

INSERT INTO `Skill` (`Skill_Name`) VALUES
('Python'),
('Advanced Python'),
('R'),
('Tableau'),
('Interpersonal Skills'),
('Public Speaking');

INSERT INTO `Skill_Set` (`Position_Name`, `Skill_Name`) VALUES
('Data Analyst', 'Python'),
('Data Analyst', 'R'),
('Data Analyst', 'Tableau'),
('Head of Security', 'Interpersonal Skills'),
('Human Resource', 'Public Speaking');

INSERT INTO `Skill_Rewarded` (`Skill_Name`, `Course_ID`) VALUES
("Python", 'FIN001'),
('Python', 'tch006'),
('Python', 'tch009'),
('R', 'COR001'),
('Tableau', 'COR001'),
('Interpersonal Skills', 'MGT001'),
('Public Speaking', 'MGT001');

INSERT INTO `Learning_Journey` (`Staff_ID`, `Position_Name`, `Skill_Name`, `Course_ID`) VALUES
(130001,'Data Analyst', 'Python', 'FIN001'),
(130001,'Human Resource', 'Public Speaking', 'MGT001'),
(130002,'Data Analyst', 'Python', 'FIN001');