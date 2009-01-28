DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS update_session $$

CREATE PROCEDURE update_session(IN sessionID VARCHAR(64), IN sigID VARCHAR(64), IN msgSig VARCHAR(64),
                                IN user_id VARCHAR(64))
BEGIN
    UPDATE session
    SET sig_id = sigID 
    WHERE session_id = sessionID;
    
    UPDATE session
    SET msg_sig = msgSig 
    WHERE session_id = sessionID;
    
    UPDATE session
    SET usr_id = user_id 
    WHERE session_id = sessionID;
    
    UPDATE session
    SET last_update = NOW() 
    WHERE session_id = sessionID;
    
    SELECT *
    FROM session
    WHERE session_id = sessionID;
END
$$

DELIMITER ;
