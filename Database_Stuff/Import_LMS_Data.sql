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

DROP DATABASE IF EXISTS `is212_ALL_IN_ONE`;
CREATE DATABASE IF NOT EXISTS `is212_ALL_IN_ONE` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `is212_ALL_IN_ONE`;

CREATE TABLE `Role` (
  `Role_ID` int PRIMARY KEY,
  `Role_Name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `Course` (
  `Course_ID` varchar(20) PRIMARY KEY,
  `Course_Name` varchar(50) NOT NULL,
  `Course_Desc` varchar(255) DEFAULT NULL,
  `Course_Status` varchar(15) DEFAULT NULL,
  `Course_Type` varchar(10) DEFAULT NULL,
  `Course_Category` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `Staff` (
  `Staff_ID` int PRIMARY KEY,
  `Staff_FName` varchar(50) NOT NULL,
  `Staff_LName` varchar(50) NOT NULL,
  `Dept` varchar(50) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Role` int,
  FOREIGN KEY (`Role`) REFERENCES Role(`Role_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Save staff enroled in courses and courses which enrolled by staff
CREATE TABLE `Registration` (
  `Reg_ID` int PRIMARY KEY,
  `Course_ID` varchar(20),
  `Staff_ID` int,
  `Reg_Status` varchar(20) NOT NULL,
  `Completion_Status` varchar(20) NOT NULL,
  FOREIGN KEY (`Course_ID`) REFERENCES Course(`Course_ID`),
  FOREIGN KEY (`Staff_ID`) REFERENCES Staff(`Staff_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
