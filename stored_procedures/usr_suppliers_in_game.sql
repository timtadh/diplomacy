DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS usr_suppliers_in_game $$

CREATE PROCEDURE usr_suppliers_in_game(IN gid INT(11), IN uid VARCHAR(64))
BEGIN
    SELECT territory.name, territory.abbrev
    FROM territory
    INNER JOIN supplier
        ON (supplier.ter_id = territory.ter_id)
    INNER JOIN country
        ON (country.cty_id = supplier.cty_id)
    WHERE country.usr_id = uid AND country.gam_id = gid
    ORDER BY territory.abbrev;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/usr_suppliers_in_game.sql