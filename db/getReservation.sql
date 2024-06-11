DELIMITER //
DROP PROCEDURE IF EXISTS getReservation //

CREATE PROCEDURE getReservation(IN user_idIn varchar(255))
BEGIN
  SELECT *
    FROM Reservations WHERE user_id = user_idIn;
END //
DELIMITER ;
