DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS game_membership_data $$

CREATE PROCEDURE game_membership_data(IN gid INT(11))
BEGIN
    SELECT *
    FROM game_membership
    WHERE game_membership.gam_id = gid;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/game_membership_data.sql