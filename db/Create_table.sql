CREATE TABLE Users (
  user_id varchar(255) NOT NULL,
  name varchar(255) NOT NULL,
  email varchar(255) DEFAULT NULL,
  user_type ENUM('customer','manager'),
  PRIMARY KEY (user_id)
);

CREATE TABLE DiningTables (
  table_id INT NOT NULL AUTO_INCREMENT,
  seats INT NOT NULL,
  PRIMARY KEY (table_id)
);

CREATE TABLE Reservations (
  reservation_id INT NOT NULL AUTO_INCREMENT,
  timeslot ENUM('0','1'),
  reservation_date DATE,
  user_id varchar(255) NOT NULL,
  table_id INT NOT NULL,
  PRIMARY KEY (reservation_id),
  FOREIGN KEY (user_id) REFERENCES Users(user_id),
  FOREIGN KEY (table_id) REFERENCES DiningTables(table_id)
);
