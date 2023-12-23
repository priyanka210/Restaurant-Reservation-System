DELIMITER //
DROP PROCEDURE IF EXISTS addUser //

CREATE PROCEDURE addUser(IN user_idIn varchar(255), IN nameIn varchar(255), IN emailIn varchar(255), IN user_typeIn ENUM('customer','manager'))
BEGIN
INSERT INTO Users (user_id,name, email, user_type) VALUES
   (user_idIn,nameIn, emailIn, user_typeIn);
SELECT LAST_INSERT_ID();
END//
DELIMITER ;
