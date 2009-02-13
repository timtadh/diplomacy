DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS session_data $$

CREATE PROCEDURE session_data(IN session_id VARCHAR(64))
BEGIN
    SELECT ses.session_id, ses.sig_id, ses.msg_sig, ses.usr_id, ses.last_update
    FROM sessions AS ses
    WHERE ses.session_id = session_id;
END
$$

DELIMITER ;
