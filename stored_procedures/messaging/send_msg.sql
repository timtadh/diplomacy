DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS send_msg $$

CREATE PROCEDURE send_msg(IN to_screen_name VARCHAR(128), IN from_usr VARCHAR(64),
                          IN subject VARCHAR(256), IN msg VARCHAR(10000))
BEGIN
    START TRANSACTION;

    SET @cur_time = NOW();

    CREATE TEMPORARY TABLE temptable (touser VARCHAR(128), fromusr VARCHAR(64), 
                                      sub VARCHAR(256), mesg VARCHAR(10000));
    
    INSERT INTO temptable (touser, fromusr, sub, mesg)
    VALUES (to_screen_name, from_usr, subject, msg);
    
    INSERT INTO message (from_usr, to_usr, time_sent, subject, msg)
    SELECT temp.fromusr AS from_usr,  usr.usr_id AS to_usr, @cur_time AS time_sent, 
           temp.sub, temp.mesg AS msg
    FROM temptable AS temp
    INNER JOIN users as usr
    ON (temp.touser = usr.screen_name);
    
    DROP TABLE temptable;

    COMMIT;
    
END
$$

DELIMITER ;
