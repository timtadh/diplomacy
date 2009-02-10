DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS delete_msg $$

CREATE PROCEDURE delete_msg(IN usr_id VARCHAR(64), IN msg_id INT)
BEGIN
    DELETE msg
    FROM message AS msg
    WHERE msg.msg_id = msg_id AND msg.to_usr = usr_id;
END
$$

DELIMITER ;
