DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS delete_supplier_in_game $$

CREATE PROCEDURE delete_supplier_in_game(IN gid INT(11), IN tid INT(11))
BEGIN
    DELETE supplier FROM supplier
    INNER JOIN country
        ON (country.cty_id = supplier.cty_id)
    WHERE country.gam_id = gid AND supplier.ter_id = tid;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/game/delete_supplier_in_game.sql