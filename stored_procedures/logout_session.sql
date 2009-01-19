DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS logout_session $$

CREATE PROCEDURE logout_session(IN session_id VARCHAR(64), IN usr_id VARCHAR(64))
BEGIN
    DELETE ses
    FROM session as ses
    WHERE (ses.session_id = session_id AND ses.usr_id = usr_id);
END
$$

DELIMITER ;
