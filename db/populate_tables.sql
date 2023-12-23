-- Sample data for Users table
INSERT INTO Users (name, email, user_password, user_type) VALUES
('John Doe', 'johndoe@example.com', 'password', 'customer'),
('Jane Smith', 'janesmith@example.com', 'password', 'customer'),
('Bob Johnson', 'bobjohnson@example.com', 'password', 'manager'),
('Alice Brown', 'alicebrown@example.com', 'password', 'customer'),
('Tom Wilson', 'tomwilson@example.com', 'password', 'customer'),
('Sarah Lee', 'sarahlee@example.com', 'password', 'customer'),
('David Kim', 'davidkim@example.com', 'password', 'manager'),
('Emily Park', 'emilypark@example.com', 'password', 'customer'),
('James Lee', 'jameslee@example.com', 'password', 'customer'),
('Grace Lee', 'gracelee@example.com', 'password', 'manager'),
('Michael Smith', 'michaelsmith@example.com', 'password', 'customer'),
('Eric Johnson', 'ericjohnson@example.com', 'password', 'customer'),
('Lucy Davis', 'lucydavis@example.com', 'password', 'customer'),
('Jessica Brown', 'jessicabrown@example.com', 'password', 'manager'),
('Mark Wilson', 'markwilson@example.com', 'password', 'customer'),
('Anna Lee', 'annalee@example.com', 'password', 'customer'),
('Alex Kim', 'alexkim@example.com', 'password', 'manager'),
('Rachel Park', 'rachelpark@example.com', 'password', 'customer'),
('Daniel Lee', 'daniellee@example.com', 'password', 'customer'),
('Samantha Lee', 'samanthalee@example.com', 'password', 'manager');

-- Sample data for DiningTables table
INSERT INTO DiningTables (seats) VALUES
(4),
(4),
(4),
(4),
(4),
(4),
(4),
(4);


-- Sample data for Reservations table
INSERT INTO Reservations (timeslot, reservation_date, user_id, table_id) VALUES
('0', '2023-03-15', 'g7vfx', 1),
('1', '2023-03-16', 'g7vfx', 2),
('0', '2023-03-17', 'g7vfx', 3),
('1', '2023-03-18', 'z9h8f', 4),
('0', '2023-03-19', 'z9h8f', 5),
('1', '2023-03-20', 'z9h8f', 6);

