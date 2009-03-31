DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS logout_session $$

CREATE PROCEDURE logout_session(IN sessionID VARCHAR(64), IN usrID VARCHAR(64))
BEGIN
    DELETE ses
    FROM sessions as ses
    WHERE (ses.session_id = sessionID AND usr_id = usrID);
END
$$

DELIMITER ;
