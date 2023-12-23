DELIMITER //
DROP PROCEDURE IF EXISTS getAllReservations //

CREATE PROCEDURE getAllReservations()
BEGIN
  SELECT *
    FROM Reservations;
END //
DELIMITER ;
