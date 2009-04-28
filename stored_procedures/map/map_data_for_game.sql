DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS map_data_for_game $$

CREATE PROCEDURE map_data_for_game(IN gid INT(11))
BEGIN
    SELECT map.world_name, game.pic, map.map_id
    FROM map
    INNER JOIN game
        ON (game.map_id = map.map_id)
    WHERE game.gam_id = gid;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/map/map_data_for_game.sql