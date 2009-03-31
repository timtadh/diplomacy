DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS game_data $$

CREATE PROCEDURE game_data(IN gid INT(11))
BEGIN
    SELECT *
    FROM game
    WHERE game.gam_id = gid;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/game_data.sql