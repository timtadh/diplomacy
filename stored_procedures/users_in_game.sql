DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS users_in_game $$

CREATE PROCEDURE users_in_game(IN gid INT(11))
BEGIN
    SELECT users.screen_name
    FROM (users INNER JOIN game_membership
        ON (users.usr_id = game_membership.usr_id))
    INNER JOIN game
        ON (game.gam_id = game_membership.gam_id)
    WHERE game.gam_id = gid;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/users_in_game.sql