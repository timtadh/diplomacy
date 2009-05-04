DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS terrs_to_update $$

CREATE PROCEDURE terr_occupied(IN ter_id INT(11))
BEGIN
    SELECT territory.ter_id
    FROM piece
    INNER JOIN country
        ON (piece.cty_id = country.cty_id)
    INNER JOIN territory
        ON (piece.ter_id = territory.ter_id)
    WHERE country.gam_id = gid AND territory.supply = 1;
END
$$

DELIMITER ;
