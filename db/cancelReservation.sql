DELIMITER //
DROP PROCEDURE IF EXISTS cancelReservation //

CREATE PROCEDURE cancelReservation(IN user_idIN varchar(255),IN reservation_IdIN INT)
BEGIN
DELETE FROM Reservations 
WHERE 
  	user_id = user_idIN
AND	reservation_Id = reservation_IdIN;

END//
DELIMITER ;
