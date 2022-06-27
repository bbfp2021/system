-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jun 27, 2022 at 11:34 AM
-- Server version: 5.7.31
-- PHP Version: 7.3.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bbfp`
--

-- --------------------------------------------------------

--
-- Table structure for table `layout`
--

DROP TABLE IF EXISTS `layout`;
CREATE TABLE IF NOT EXISTS `layout` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `x` smallint(5) UNSIGNED NOT NULL,
  `y` smallint(5) UNSIGNED NOT NULL,
  `z` smallint(5) UNSIGNED NOT NULL,
  `box_num` smallint(5) UNSIGNED NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=67 DEFAULT CHARSET=latin1 COLLATE=latin1_german1_ci;

--
-- Dumping data for table `layout`
--

INSERT INTO `layout` (`id`, `x`, `y`, `z`, `box_num`) VALUES
(1, 0, 0, 0, 0),
(7, 1, 0, 0, 0),
(8, 1, 1, 0, 101),
(13, 2, 0, 0, 0),
(14, 2, 1, 0, 102),
(19, 3, 0, 0, 0),
(66, 3, 0, 1, 0),
(65, 2, 1, 1, 104),
(64, 2, 0, 1, 0),
(63, 1, 1, 1, 103),
(62, 1, 0, 1, 0),
(61, 0, 0, 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `storage`
--

DROP TABLE IF EXISTS `storage`;
CREATE TABLE IF NOT EXISTS `storage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `box_num` int(11) NOT NULL,
  `content` varchar(200) COLLATE latin1_german1_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=87 DEFAULT CHARSET=latin1 COLLATE=latin1_german1_ci;

--
-- Dumping data for table `storage`
--

INSERT INTO `storage` (`id`, `box_num`, `content`) VALUES
(74, 101, 'Schraube'),
(73, 101, 'Mutter'),
(72, 101, 'Scheibe'),
(82, 102, 'Pins'),
(81, 102, 'Plants'),
(85, 103, 'Nieten'),
(84, 103, 'Schraube'),
(83, 103, 'Mutter'),
(79, 104, 'Akku'),
(80, 104, 'Akkupack'),
(86, 103, 'ULS');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) COLLATE latin1_german1_ci NOT NULL,
  `email` varchar(120) COLLATE latin1_german1_ci NOT NULL,
  `password_hash` varchar(128) COLLATE latin1_german1_ci NOT NULL,
  `last_seen` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_german1_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password_hash`, `last_seen`) VALUES
(2, 'user', 'user@example.com', 'pbkdf2:sha256:150000$dvniTXaq$a54c8c1da035d7fa4ec29cd2c1569f0e8298946595b4d8cb55e450996d6a330a', '2022-06-21 11:08:13');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
