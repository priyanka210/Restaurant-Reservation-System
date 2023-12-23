DELIMITER //
DROP PROCEDURE IF EXISTS getUser //

CREATE PROCEDURE getUser(IN userIdIn varchar(255))
BEGIN
  SELECT *
    FROM Users WHERE user_id = userIdIn;
END //
DELIMITER ;

