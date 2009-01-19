DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS user_data_byemail $$

CREATE PROCEDURE user_data_byemail(IN email VARCHAR(256))
BEGIN
    SELECT usr_id, name, email, pass_hash, salt, last_login, creation, status
    FROM users as users
    WHERE users.email = email;
END
$$

DELIMITER ;
