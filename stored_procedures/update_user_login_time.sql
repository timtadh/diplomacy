DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS update_user_login_time $$

CREATE PROCEDURE update_user_login_time(IN usr_id VARCHAR(64))
BEGIN
    UPDATE users
    SET last_login = NOW() 
    WHERE usr_id = usr_id;
END
$$

DELIMITER ;
