DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS count_games $$

CREATE PROCEDURE count_games()
BEGIN
    SELECT COUNT(*) as num_games_total
    FROM game;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/count_games.sql