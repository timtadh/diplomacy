DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS terrs_in_game $$

CREATE PROCEDURE terrs_in_game(IN gid INT(11))
BEGIN
    SELECT territory.name, territory.abbrev
    FROM territory
    WHERE territory.map_id IN
        (SELECT game.map_id FROM game WHERE game.gam_id = gid);
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/terrs_in_game.sql