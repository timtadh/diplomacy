DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS set_session_gam_id $$

CREATE PROCEDURE set_session_gam_id(IN sessionID VARCHAR(64), IN user_id VARCHAR(64), 
                                    IN game_id INT(11))
BEGIN
    UPDATE sessions
    SET gam_id = game_id 
    WHERE session_id = sessionID AND usr_id = user_id;
END
$$

DELIMITER ;
