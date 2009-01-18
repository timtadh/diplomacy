DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS update_session $$

CREATE PROCEDURE update_session(IN session_id VARCHAR(64), IN sig_id VARCHAR(64), IN msg_sig VARCHAR(64),
                                IN user_id VARCHAR(64), IN last_update DATETIME)
BEGIN
    UPDATE session
    SET sig_id = sig_id 
    WHERE session_id = session_id;
    
    UPDATE session
    SET msg_sig = msg_sig 
    WHERE session_id = session_id;
    
    UPDATE session
    SET user_id = user_id 
    WHERE session_id = session_id;
    
    UPDATE session
    SET last_update = last_update 
    WHERE session_id = session_id;
END
$$

DELIMITER ;
