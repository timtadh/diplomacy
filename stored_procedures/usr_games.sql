DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS usr_games $$

CREATE PROCEDURE usr_games(IN usr_id VARCHAR(256))
BEGIN
    SELECT g.gam_id, g.pic, g.gam_season, g.gam_year, g.turn_start, g.turn_length, g.turn_stage, g.ended
    FROM users AS usr
    INNER JOIN game_membership AS gm
        ON (gm.usr_id = usr.usr_id)
    INNER JOIN game AS g
        ON (g.gam_id = gm.gam_id)
    WHERE
        usr.usr_id = usr_id;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/usr_games.sql