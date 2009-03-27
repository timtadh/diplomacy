DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS pieces_for_user $$

CREATE PROCEDURE pieces_for_user(IN gid INT(11), IN uid VARCHAR(64))
BEGIN
    SELECT piece.pce_id, piece.pce_type, piece.pce_id, territory.name, territory.abbrev
    FROM piece
    INNER JOIN country
        ON (piece.cty_id = country.cty_id)
    INNER JOIN territory
        ON (territory.ter_id = piece.ter_id)
    WHERE country.usr_id = uid AND country.gam_id = gid
    ORDER BY territory.abbrev;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/pieces_for_user.sql