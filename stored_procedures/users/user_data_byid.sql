DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS user_data_byid $$

CREATE PROCEDURE user_data_byid(IN usr_id VARCHAR(64))
BEGIN
    SELECT usr.usr_id, usr.name, usr.email, usr.screen_name, usr.pass_hash, 
           usr.salt, usr.last_login, usr.creation, usr.status
    FROM users as usr
    WHERE usr.usr_id = usr_id;
END
$$

DELIMITER ;
