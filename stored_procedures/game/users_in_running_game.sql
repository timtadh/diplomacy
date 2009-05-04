DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS users_in_running_game $$

CREATE PROCEDURE users_in_running_game(IN gid INT(11))
BEGIN
    SELECT users.screen_name, users.usr_id, country.name, country.color, country.cty_id
    FROM (users INNER JOIN game_membership
        ON (users.usr_id = game_membership.usr_id))
    INNER JOIN game
        ON (game.gam_id = game_membership.gam_id)
    INNER JOIN country
        ON (users.usr_id = country.usr_id)
    WHERE game.gam_id = gid AND country.gam_id = game.gam_id;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/game/users_in_running_game.sql