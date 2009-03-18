DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS count_users $$

CREATE PROCEDURE count_users(IN usr_id VARCHAR(256))
BEGIN
    SELECT COUNT(*) as num_users
    FROM users;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/count_users.sql