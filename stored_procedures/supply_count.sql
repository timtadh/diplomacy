DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS supply_count $$

CREATE PROCEDURE supply_count ()
BEGIN
    SELECT u.screen_name, u.email
	FROM users AS u;
	-- Eventually I need to get into the current game's supplier table
    
END
$$

DELIMITER ;