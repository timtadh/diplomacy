DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS users_table $$

CREATE PROCEDURE users_table()
BEGIN
    SELECT usr.usr_id, usr.name, usr.email, usr.screen_name, usr.pass_hash, usr.salt, 
           usr.last_login, usr.creation, usr.status
    FROM users AS usr;
END
$$

DELIMITER ;
