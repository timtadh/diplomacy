DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS user_data_bysn $$

CREATE PROCEDURE user_data_bysn(IN screen_name VARCHAR(256))
BEGIN
    SELECT usr.usr_id, usr.name, usr.email, usr.screen_name, usr.pass_hash, 
           usr.salt, usr.last_login, usr.creation, usr.status
    FROM users as usr
    WHERE usr.screen_name = screen_name;
END
$$

DELIMITER ;
