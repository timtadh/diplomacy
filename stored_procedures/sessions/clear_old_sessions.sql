DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS clear_old_sessions $$

CREATE PROCEDURE clear_old_sessions()
BEGIN
    SET @cur_time = NOW();
    
    DELETE ses
    FROM sessions as ses
    WHERE (TIMESTAMPDIFF(MINUTE, ses.last_update, @cur_time) > 45);
END
$$

DELIMITER ;
