-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 08, 2025 at 10:53 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cms`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `courier_orders`
--

CREATE TABLE `courier_orders` (
  `order_id` int(11) NOT NULL,
  `sender_name` varchar(255) NOT NULL,
  `sender_address` text NOT NULL,
  `sender_contact` varchar(15) NOT NULL,
  `receiver_name` varchar(255) NOT NULL,
  `receiver_address` text NOT NULL,
  `receiver_contact` varchar(15) NOT NULL,
  `package_type` varchar(50) NOT NULL,
  `package_size` varchar(50) NOT NULL,
  `package_weight` varchar(50) NOT NULL,
  `consignment_no` varchar(50) NOT NULL,
  `shipment_type` varchar(20) NOT NULL,
  `pickup_date` date NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `payment_status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `courier_orders`
--

INSERT INTO `courier_orders` (`order_id`, `sender_name`, `sender_address`, `sender_contact`, `receiver_name`, `receiver_address`, `receiver_contact`, `package_type`, `package_size`, `package_weight`, `consignment_no`, `shipment_type`, `pickup_date`, `total_amount`, `payment_status`) VALUES
(1, 'mama', '123 Main St, NY', '15451526151651', 'raka', '456 Elm St, CA', '9876543210', 'Electronics', 'Medium', '2.5kg', 'CN001', 'Air', '2025-02-10', 100.00, 'COD'),
(2, 'Charlie Brown', '789 Oak St, TX', '1122334455', 'David Wilson', '321 Pine St, FL', '5544332211', 'Documents', 'Small', '1.0kg', 'CN002', 'Road', '2025-02-15', 20.00, 'UPI'),
(3, 'Eve Adams', '987 Birch St, WA', '9988776655', 'Frank White', '654 Cedar St, CO', '6677889900', 'Clothing', 'Large', '4.0kg', 'CN003', 'Sea', '2025-02-12', 35.00, 'Paytm'),
(4, 'Grace Miller', '741 Spruce St, IL', '5566778899', 'Henry Clark', '852 Maple St, NV', '3344556677', 'Furniture', 'Extra Large', '15.0kg', 'CN004', 'Train', '2025-02-18', 100.00, 'Google Pay'),
(5, 'Sophia Williams', '963 Sunset Blvd, CA', '7788996655', 'Liam Johnson', '159 River Rd, NJ', '8899775566', 'Books', 'Small', '3.0kg', 'CN005', 'Air', '2025-02-20', 15.00, 'PhonePe'),
(6, 'Noah Anderson', '852 Lincoln St, OR', '4477889922', 'Olivia Martinez', '357 Park Ave, TX', '2233445566', 'Food Items', 'Medium', '5.5kg', 'CN006', 'Road', '2025-02-17', 25.00, 'Payzap'),
(7, 'Emma Harris', '123 Willow St, MA', '1122446688', 'Mason Taylor', '852 Birch St, AZ', '3322114455', 'Fragile', 'Large', '6.5kg', 'CN007', 'Sea', '2025-02-11', 40.00, 'COD'),
(8, 'William Scott', '963 Hill St, KY', '7788994455', 'Ava Clark', '147 Valley Rd, GA', '6633557799', 'Documents', 'Medium', '2.0kg', 'CN008', 'Train', '2025-02-14', 18.00, 'UPI'),
(9, 'James Lee', '852 Brook St, SC', '2244668822', 'Emily Carter', '369 Pine St, TN', '8877665544', 'Electronics', 'Small', '1.5kg', 'CN009', 'Air', '2025-02-19', 22.00, 'Paytm'),
(10, 'Olivia Evans', '369 Meadow St, MO', '9988773322', 'Benjamin Wright', '951 Spruce St, WA', '3322556677', 'Clothing', 'Medium', '3.8kg', 'CN010', 'Road', '2025-02-13', 28.00, 'Google Pay'),
(11, 'Liam Johnson', '123 Main St, NY', '1234567890', 'Sophia Lee', '456 Elm St, CA', '9876543210', 'Furniture', 'Medium', '2.5kg', 'CN011', 'Air', '2025-02-10', 50.00, 'COD'),
(12, 'Isabella White', '789 Oak St, TX', '1122334455', 'Mia Brown', '321 Pine St, FL', '5544332211', 'Books', 'Small', '1.0kg', 'CN012', 'Road', '2025-02-15', 20.00, 'UPI'),
(13, 'Lucas Garcia', '987 Birch St, WA', '9988776655', 'Amelia Adams', '654 Cedar St, CO', '6677889900', 'Food Items', 'Large', '4.0kg', 'CN013', 'Sea', '2025-02-12', 35.00, 'Paytm'),
(14, 'Alexander Martinez', '741 Spruce St, IL', '5566778899', 'Ella Cooper', '852 Maple St, NV', '3344556677', 'Fragile', 'Extra Large', '15.0kg', 'CN014', 'Train', '2025-02-18', 100.00, 'Google Pay'),
(15, 'Ethan Rodriguez', '963 Sunset Blvd, CA', '7788996655', 'Aiden Young', '159 River Rd, NJ', '8899775566', 'Documents', 'Small', '3.0kg', 'CN015', 'Air', '2025-02-20', 15.00, 'PhonePe'),
(16, 'Harper Lewis', '852 Lincoln St, OR', '4477889922', 'Mila Robinson', '357 Park Ave, TX', '2233445566', 'Electronics', 'Medium', '5.5kg', 'CN016', 'Road', '2025-02-17', 25.00, 'Payzap'),
(17, 'Daniel Walker', '123 Willow St, MA', '1122446688', 'Joseph Scott', '852 Birch St, AZ', '3322114455', 'Clothing', 'Large', '6.5kg', 'CN017', 'Sea', '2025-02-11', 40.00, 'COD');

-- --------------------------------------------------------

--
-- Table structure for table `customer_queries`
--

CREATE TABLE `customer_queries` (
  `user_name` varchar(255) NOT NULL,
  `user_email` varchar(255) NOT NULL,
  `user_query` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer_queries`
--

INSERT INTO `customer_queries` (`user_name`, `user_email`, `user_query`) VALUES
('harshil maheta', 'hik@gmail.com', 'low speed');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `courier_orders`
--
ALTER TABLE `courier_orders`
  ADD PRIMARY KEY (`order_id`),
  ADD UNIQUE KEY `consignment_no` (`consignment_no`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `courier_orders`
--
ALTER TABLE `courier_orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
