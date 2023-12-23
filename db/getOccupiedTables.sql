DELIMITER //
DROP PROCEDURE IF EXISTS getOccupiedTables //

CREATE PROCEDURE getOccupiedTables(IN currentDateIn DATE)
BEGIN
  SELECT *
    FROM Reservations WHERE reservation_date = currentDateIn;
END //
DELIMITER ;
