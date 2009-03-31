DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS count_unread_msges $$

CREATE PROCEDURE count_unread_msges(IN usr_id VARCHAR(64))
BEGIN
    SELECT COUNT(*) as unread_msges
    FROM message AS msg
    INNER JOIN users AS tousr
    ON (tousr.usr_id = msg.to_usr)
    INNER JOIN users AS fromusr
    ON (fromusr.usr_id = msg.from_usr)
    WHERE msg.to_usr = usr_id AND msg.have_read = FALSE;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/count_unread_msges.sql