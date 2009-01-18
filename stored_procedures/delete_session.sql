DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS delete_session $$

CREATE PROCEDURE delete_session(IN session_id VARCHAR(64))
BEGIN
    DELETE ses
    FROM session as ses
    WHERE (ses.session_id = session_id);
END
$$

DELIMITER ;
