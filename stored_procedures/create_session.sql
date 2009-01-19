DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS create_session $$

CREATE PROCEDURE create_session(IN session_id VARCHAR(64), IN sig_id VARCHAR(64), IN msg_sig VARCHAR(64),
                                IN user_id VARCHAR(64))
BEGIN
    SET @cur_time = NOW();

    INSERT INTO session (session_id, sig_id, msg_sig, usr_id, last_update)
    VALUES (session_id, sig_id, msg_sig, user_id, @cur_time);
END
$$

DELIMITER ;
/*
'''INSERT INTO session 
    VALUES ('%s', '%s', '%s', '%s', '%s') ''' % (sessionID, cur_sigID, cur_msgSig, user, timestr)
    */