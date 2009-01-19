DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS session_data $$

CREATE PROCEDURE session_data(IN session_id VARCHAR(64))
BEGIN
    SELECT session_id, sig_id, msg_sig, usr_id, last_update
    FROM session as ses
    WHERE ses.session_id = session_id;
END
$$

DELIMITER ;
