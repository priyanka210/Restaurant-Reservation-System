DELIMITER //
DROP PROCEDURE IF EXISTS updateReservation //

CREATE PROCEDURE updateReservation(
  IN p_user_id varchar(255),
  IN p_reservation_id INT,
  IN p_timeslot varchar(255),
  IN p_table_id INT,
  IN p_reservation_date varchar(255)
)
BEGIN
UPDATE Reservations
  SET timeslot = p_timeslot,
      reservation_date = p_reservation_date,
	table_id = p_table_id
  WHERE reservation_id = p_reservation_id AND user_id = p_user_id;
END//
DELIMITER ;
