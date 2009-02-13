DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS usr_messages $$

CREATE PROCEDURE usr_messages(IN usr_id VARCHAR(64))
BEGIN
    SELECT msg.msg_id, fromusr.screen_name AS 'from', tousr.screen_name AS 'to', msg.from_usr, msg.to_usr, 
           msg.time_sent, msg.subject, msg.msg, msg.have_read
    FROM message AS msg
    INNER JOIN users AS tousr
    ON (tousr.usr_id = msg.to_usr)
    INNER JOIN users AS fromusr
    ON (fromusr.usr_id = msg.from_usr)
    WHERE msg.to_usr = usr_id
    ORDER BY msg.time_sent DESC;
END
$$

DELIMITER ;
