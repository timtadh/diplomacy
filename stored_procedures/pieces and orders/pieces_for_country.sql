DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS pieces_for_country $$

CREATE PROCEDURE pieces_for_country(IN cid INT(11))
BEGIN
    SELECT piece.ter_id, piece.pce_type, piece.pce_id
    FROM piece
    WHERE piece.cty_id = cid;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/pieces_for_country.sql