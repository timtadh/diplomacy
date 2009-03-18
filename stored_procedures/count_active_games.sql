DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS count_active_games $$

CREATE PROCEDURE count_active_games()
BEGIN
    SELECT COUNT(*) as num_games_active
    FROM game
    WHERE game.ended = FALSE;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/count_active_games.sql