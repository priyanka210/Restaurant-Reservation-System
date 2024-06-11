DELIMITER //
DROP PROCEDURE IF EXISTS deleteUser //

CREATE PROCEDURE deleteUser(IN user_idIN varchar(255))
BEGIN
DELETE FROM Reservations WHERE user_id = user_idIN;

DELETE FROM Users WHERE user_id = user_idIN;

END//
DELIMITER ;
