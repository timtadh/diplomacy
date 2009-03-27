DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS piece_info $$

CREATE PROCEDURE piece_info(IN pid INT(11))
BEGIN
    SELECT piece.pce_type, piece.pce_id, territory.name, territory.abbrev, users.usr_id
    FROM piece
    INNER JOIN territory
        ON (territory.ter_id = piece.ter_id)
    INNER JOIN country
        ON (piece.cty_id = country.cty_id)
    INNER JOIN users
        ON (country.usr_id = users.usr_id)
    WHERE piece.pce_id = pid;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/piece_info.sql