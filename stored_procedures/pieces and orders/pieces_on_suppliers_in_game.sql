DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS pieces_on_suppliers_in_game $$

CREATE PROCEDURE pieces_on_suppliers_in_game(IN gid INT(11))
BEGIN
    SELECT piece.ter_id, piece.pce_id, piece.pce_type, piece.cty_id
    FROM piece
    INNER JOIN country
        ON (piece.cty_id = country.cty_id)
    INNER JOIN territory
        ON (piece.ter_id = territory.ter_id)
    WHERE country.gam_id = gid AND territory.supply = 1;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/pieces and orders/pieces_on_suppliers_in_game.sql