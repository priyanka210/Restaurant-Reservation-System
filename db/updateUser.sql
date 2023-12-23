DELIMITER //
DROP PROCEDURE IF EXISTS updateUser //

CREATE PROCEDURE updateUser(
  IN p_user_id varchar(255),
  IN p_name varchar(255),
  IN p_email varchar(255)
)
BEGIN
UPDATE Users
  SET name = p_name,
      email = p_email
  WHERE user_id = p_user_id;
END//
DELIMITER ;
