DELIMITER //
DROP PROCEDURE IF EXISTS addReservation //

CREATE PROCEDURE addReservation(IN timeslotIn ENUM('0','1'), IN reservation_dateIn DATE, IN user_idIn varchar(255), IN table_idIn INT)
BEGIN
INSERT INTO Reservations (timeslot, reservation_date, user_id, table_id) VALUES
   (timeslotIn, reservation_dateIn, user_idIn, table_idIn);
SELECT LAST_INSERT_ID();
END//
DELIMITER ;
