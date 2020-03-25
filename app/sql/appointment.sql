-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Mar 21, 2020 at 07:44 PM
-- Server version: 5.7.25
-- PHP Version: 7.3.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `esd_appointment`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointment`
--

CREATE TABLE `appointment` (
  `appointment_id` int(11) NOT NULL,
  `doctor_id` varchar(11) NOT NULL,
  `patient_id` varchar(11) NOT NULL,
  `date` varchar(15) NOT NULL,
  `time` varchar(12) NOT NULL,
  `payment_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `appointment`
--

INSERT INTO `appointment` (`appointment_id`, `doctor_id`, `patient_id`, `date`, `time`, `payment_id`) VALUES
(19, '2', '1', '04-04-20', '4.00 AM', 41),
(20, '3', '2', '04-04-20', '5.00 AM', 30),
(21, '2', '3', '04-04-20', '6.00 AM', 41),
(22, '1', '1', '04-04-20', '7.00 AM', 20),
(23, '2', '2', '04-04-20', '8.00 AM', 41),
(24, '2', '1', '04-04-20', '9.00 AM', 41);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointment`
--
ALTER TABLE `appointment`
  ADD PRIMARY KEY (`appointment_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointment`
--
ALTER TABLE `appointment`
  MODIFY `appointment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
