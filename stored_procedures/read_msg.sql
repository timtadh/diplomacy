DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS read_msg $$

CREATE PROCEDURE read_msg(IN msg_id INT)
BEGIN
    UPDATE message AS msg
    SET msg.have_read = 1 
    WHERE msg.msg_id = msg_id;
END
$$

DELIMITER ;
