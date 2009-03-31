DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS terrs_in_map $$

CREATE PROCEDURE terrs_in_map(IN mid INT(11))
BEGIN
    SELECT territory.ter_id, territory.name, territory.abbrev, 
        territory.piece_x, territory.piece_y, territory.label_x, territory.label_y, 
        territory.ter_type, territory.supply, territory.home_supply, territory.coastal
    FROM territory
    WHERE territory.map_id = mid;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/terrs_in_map.sql