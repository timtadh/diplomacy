DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS countries_in_game $$

CREATE PROCEDURE countries_in_game(IN gid INT(11))
BEGIN
    SELECT country.cty_id, country.name, country.color
    FROM country
    WHERE country.gam_id = gid;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/countries_in_game.sql