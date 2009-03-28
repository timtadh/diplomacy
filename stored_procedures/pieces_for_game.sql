DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS pieces_for_game $$

CREATE PROCEDURE pieces_for_game(IN gid INT(11))
BEGIN
    SELECT piece.ter_id, piece.pce_id, piece.pce_type, piece.cty_id
    FROM piece
    INNER JOIN country
        ON (piece.cty_id = country.cty_id)
    WHERE country.gam_id = gid;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/pieces_for_game.sql