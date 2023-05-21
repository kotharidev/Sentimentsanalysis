-- phpMyAdmin SQL Dump
-- version 3.2.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 03, 2023 at 03:37 PM
-- Server version: 5.1.41
-- PHP Version: 5.3.1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `sociamedia`
--
CREATE DATABASE `sociamedia` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `sociamedia`;

-- --------------------------------------------------------

--
-- Table structure for table `answerdetails`
--

CREATE TABLE IF NOT EXISTS `answerdetails` (
  `AnswerId` int(11) NOT NULL AUTO_INCREMENT,
  `Answer` varchar(250) NOT NULL,
  `Category` int(11) NOT NULL,
  `QuestionId` int(11) NOT NULL,
  `Recorded_Date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`AnswerId`),
  KEY `QuestionId` (`QuestionId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=39 ;

--
-- Dumping data for table `answerdetails`
--

INSERT INTO `answerdetails` (`AnswerId`, `Answer`, `Category`, `QuestionId`, `Recorded_Date`) VALUES
(1, '3 - 5 Years', 2, 1, '2023-04-27 10:50:53'),
(2, '1 Year', 1, 1, '2023-04-27 10:50:57'),
(3, '7 Years', 3, 1, '2023-04-27 10:51:05'),
(4, '1 - 3 Years', 0, 1, '2023-04-27 10:51:01'),
(6, 'Instagram', 1, 2, '2023-04-27 10:52:04'),
(7, 'Facebook', 0, 2, '2023-04-27 10:52:21'),
(9, 'Twitter', 2, 2, '2023-04-27 23:12:46'),
(10, 'Youtube', 3, 2, '2023-04-27 23:12:53'),
(11, 'Comedy', 1, 3, '2023-04-27 23:14:27'),
(12, 'Politics', 6, 3, '2023-04-27 10:53:38'),
(13, 'Education', 3, 3, '2023-04-28 20:22:23'),
(14, 'Meeting New People', 4, 3, '2023-04-27 23:13:48'),
(15, 'Entertainment', 2, 3, '2023-04-27 10:54:23'),
(16, 'Business', 0, 3, '2023-04-27 10:54:23'),
(17, 'Personal Care', 5, 3, '2023-04-27 11:04:01'),
(18, '1 - 2 Hour', 1, 4, '2023-04-27 10:55:14'),
(19, '0 - 1 Hour', 0, 4, '2023-04-27 10:55:14'),
(21, 'Greater 3 Hour', 3, 4, '2023-04-27 10:55:32'),
(22, '2 - 3 Hour', 2, 4, '2023-04-27 10:55:40'),
(23, 'Sad', 4, 5, '2023-04-27 23:18:29'),
(25, 'Politics', 2, 5, '2023-04-27 23:18:37'),
(26, 'Movies/Series', 1, 5, '2023-04-27 10:57:58'),
(27, 'Comedy', 0, 5, '2023-04-27 10:58:22'),
(28, 'Sports', 5, 5, '2023-04-27 23:18:50'),
(29, 'Romance', 3, 5, '2023-04-27 23:18:57'),
(30, 'Loneliness', 5, 6, '2023-04-27 23:22:02'),
(32, 'Sad', 6, 6, '2023-04-27 22:35:45'),
(33, 'Connection & Belongings', 1, 6, '2023-04-27 11:00:55'),
(34, 'Inspiration', 4, 6, '2023-04-27 23:21:44'),
(35, 'Happiness', 3, 6, '2023-04-27 23:21:49'),
(36, 'Calm', 0, 6, '2023-04-27 11:01:20'),
(38, 'Empowerment', 2, 6, '2023-04-27 23:22:16');

-- --------------------------------------------------------

--
-- Table structure for table `historydetails`
--

CREATE TABLE IF NOT EXISTS `historydetails` (
  `HistoryId` int(11) NOT NULL AUTO_INCREMENT,
  `PersonId` int(11) NOT NULL,
  `Question1Id` varchar(250) NOT NULL,
  `Question2Id` varchar(250) NOT NULL,
  `Question3Id` varchar(250) NOT NULL,
  `Question4Id` varchar(250) NOT NULL,
  `Question5Id` varchar(250) NOT NULL,
  `Question6Id` varchar(250) NOT NULL,
  `Result` varchar(250) NOT NULL,
  `Percentage` varchar(250) NOT NULL,
  `Recorded_Date` date NOT NULL,
  PRIMARY KEY (`HistoryId`),
  KEY `PersonId` (`PersonId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=8 ;

--
-- Dumping data for table `historydetails`
--

INSERT INTO `historydetails` (`HistoryId`, `PersonId`, `Question1Id`, `Question2Id`, `Question3Id`, `Question4Id`, `Question5Id`, `Question6Id`, `Result`, `Percentage`, `Recorded_Date`) VALUES
(1, 6, '1', '0', '0', '0', '5', '0', 'Happy', '81.0', '2023-04-28'),
(2, 6, '1', '2', '5', '1', '3', '2', 'Depression', '45.0', '2023-04-28'),
(3, 6, '1', '2', '5', '1', '3', '2', 'Depression', '45.0', '2023-04-28'),
(4, 6, '1', '2', '5', '1', '3', '2', 'Depression', '45.0', '2023-04-28'),
(5, 6, '2', '3', '2', '1', '3', '5', 'Depression', '23.0', '2023-04-28'),
(6, 6, '2', '3', '3', '1', '3', '5', 'Depression', '19.0', '2023-05-03'),
(7, 6, '2', '3', '3', '1', '3', '5', 'Depression', '19.0', '2023-05-03');

-- --------------------------------------------------------

--
-- Table structure for table `personaldetails`
--

CREATE TABLE IF NOT EXISTS `personaldetails` (
  `PersonId` int(11) NOT NULL AUTO_INCREMENT,
  `Firstname` varchar(250) NOT NULL,
  `Lastname` varchar(250) NOT NULL,
  `Phoneno` bigint(250) NOT NULL,
  `DOB` date NOT NULL,
  `Age` int(11) NOT NULL,
  `Emailid` varchar(250) NOT NULL,
  `Address` varchar(250) NOT NULL,
  `Username` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  `Recorded_Date` date NOT NULL,
  PRIMARY KEY (`PersonId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=8 ;

--
-- Dumping data for table `personaldetails`
--

INSERT INTO `personaldetails` (`PersonId`, `Firstname`, `Lastname`, `Phoneno`, `DOB`, `Age`, `Emailid`, `Address`, `Username`, `Password`, `Recorded_Date`) VALUES
(6, 'kiruba', 's', 9043963074, '2023-04-30', 40, 'kirubakarans2009@gmail.com', 'No:10,Chinna Ponnu Nagar,\r\nS.N.Chavady, Cuddalore-607002.', 'kiruba', 'kiruba', '2021-04-26'),
(7, 'hari', 's', 9043963074, '2023-04-25', 34, 'kirubakarans2009@gmail.com', 'dsfdsaasd', 'hari', 'hari', '2023-04-27');

-- --------------------------------------------------------

--
-- Table structure for table `questiondetails`
--

CREATE TABLE IF NOT EXISTS `questiondetails` (
  `QuestionId` int(11) NOT NULL AUTO_INCREMENT,
  `Question` text NOT NULL,
  `Recorded_Date` date NOT NULL,
  PRIMARY KEY (`QuestionId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

--
-- Dumping data for table `questiondetails`
--

INSERT INTO `questiondetails` (`QuestionId`, `Question`, `Recorded_Date`) VALUES
(1, 'How long you have been on Social Media?', '2023-03-12'),
(2, 'What are the Social Media tools which you use?', '2023-03-12'),
(3, 'What is the purpose for which you are going to Social Media?', '2023-03-12'),
(4, 'How time you spent on Social Media?', '2023-03-12'),
(5, 'What type of contents, you watch more about?', '2023-03-12'),
(6, 'How are the post affecting your personal life?', '2023-03-12');

-- --------------------------------------------------------

--
-- Table structure for table `taskdetails`
--

CREATE TABLE IF NOT EXISTS `taskdetails` (
  `TaskId` int(11) NOT NULL AUTO_INCREMENT,
  `TaskName` varchar(250) NOT NULL,
  `Recorded_Date` date NOT NULL,
  PRIMARY KEY (`TaskId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=19 ;

--
-- Dumping data for table `taskdetails`
--

INSERT INTO `taskdetails` (`TaskId`, `TaskName`, `Recorded_Date`) VALUES
(1, 'Restart an old hobby.', '2023-03-31'),
(2, 'Meet a friend you haven''t met from long time.', '2023-03-31'),
(3, 'Try to learn a new skill.', '2023-03-31'),
(4, 'Register for a workshop/class', '2023-03-31'),
(5, 'Finish incomplete works.', '2023-03-31'),
(6, 'Try a new cuisine.', '2023-03-31'),
(7, 'Learn a new sport.', '2023-03-31'),
(8, 'Try to go on a holiday.', '2023-03-31'),
(9, 'Spend more time with family.', '2023-03-31'),
(10, 'Try new forms of entertainment.', '2023-03-31'),
(11, 'Yoga.', '2023-03-31'),
(12, 'Arts and crafts.', '2023-03-31'),
(13, 'Journalling.', '2023-03-31'),
(14, 'Treat yourself to something you''ve wanted to purchase for a long time.', '2023-03-31'),
(15, 'Do one activity out of comfort zone.', '2023-03-31'),
(16, 'Watch your favourite movie/new movie.', '2023-03-31'),
(17, 'Redecorate your living space.', '2023-03-31'),
(18, 'Complete incomplete chores.', '2023-03-31');

-- --------------------------------------------------------

--
-- Table structure for table `useranswerdetails`
--

CREATE TABLE IF NOT EXISTS `useranswerdetails` (
  `UserAnswerId` int(11) NOT NULL AUTO_INCREMENT,
  `PersonId` int(11) NOT NULL,
  `QuestionId` int(11) NOT NULL,
  `Answer` varchar(250) NOT NULL,
  `Recorded_Date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`UserAnswerId`),
  KEY `QuestionId` (`QuestionId`),
  KEY `PersonId` (`PersonId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=326 ;

--
-- Dumping data for table `useranswerdetails`
--

INSERT INTO `useranswerdetails` (`UserAnswerId`, `PersonId`, `QuestionId`, `Answer`, `Recorded_Date`) VALUES
(320, 6, 1, '3 - 5 Years', '2023-04-28 20:12:23'),
(321, 6, 2, 'Youtube', '2023-04-28 20:12:24'),
(322, 6, 3, 'Education', '2023-04-28 20:12:33'),
(323, 6, 4, '1 - 2 Hour', '2023-04-28 20:12:34'),
(324, 6, 5, 'Romance', '2023-04-28 20:12:42'),
(325, 6, 6, 'Loneliness', '2023-04-28 20:12:43');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `historydetails`
--
ALTER TABLE `historydetails`
  ADD CONSTRAINT `historydetails_ibfk_1` FOREIGN KEY (`PersonId`) REFERENCES `personaldetails` (`PersonId`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `useranswerdetails`
--
ALTER TABLE `useranswerdetails`
  ADD CONSTRAINT `useranswerdetails_ibfk_1` FOREIGN KEY (`PersonId`) REFERENCES `personaldetails` (`PersonId`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `useranswerdetails_ibfk_2` FOREIGN KEY (`QuestionId`) REFERENCES `questiondetails` (`QuestionId`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
