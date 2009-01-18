DELIMITER $$

USE masran

DROP PROCEDURE IF EXISTS update_status $$

CREATE PROCEDURE update_status(IN usrid VARCHAR(64), IN status_text VARCHAR(500))
BEGIN
    UPDATE users
    SET status = status_text
    WHERE user_id = usrid;
END
$$

DELIMITER ;
