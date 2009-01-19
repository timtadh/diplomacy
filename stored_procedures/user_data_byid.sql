DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS user_data_byid $$

CREATE PROCEDURE user_data_byid(IN usr_id VARCHAR(64))
BEGIN
    SELECT usr_id, name, email, pass_hash, salt, last_login, creation, status
    FROM users as users
    WHERE users.usr_id = usr_id;
END
$$

DELIMITER ;
