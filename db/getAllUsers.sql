DELIMITER //
DROP PROCEDURE IF EXISTS getAllUsers //

CREATE PROCEDURE getAllUsers()
BEGIN
  SELECT *
    FROM Users;
END //
DELIMITER ;


