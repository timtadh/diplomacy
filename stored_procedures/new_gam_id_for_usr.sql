DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS new_gam_id_for_usr $$

CREATE PROCEDURE new_gam_id_for_usr(IN sn VARCHAR(256))
BEGIN
    SELECT game.gam_id, game.pic
    FROM users
    INNER JOIN game
        ON (game.host = users.usr_id)
    WHERE users.screen_name = sn AND game.turn_stage = 0;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/new_gam_id_for_usr.sql