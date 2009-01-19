DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS create_user $$

CREATE PROCEDURE create_user(IN usr_id VARCHAR(64), IN name VARCHAR(256), IN email VARCHAR(256),
                                IN pass_hash VARCHAR(64), IN salt VARCHAR(64))
BEGIN
    SET @cur_time = NOW();

    INSERT INTO users (usr_id, name, email, pass_hash, salt, last_login, creation)
    VALUES (usr_id, name, email, pass_hash, salt, @cur_time, @cur_time);
END
$$

DELIMITER ;
/*
'''INSERT INTO session 
    VALUES ('%s', '%s', '%s', '%s', '%s') ''' % (sessionID, cur_sigID, cur_msgSig, user, timestr)
    */