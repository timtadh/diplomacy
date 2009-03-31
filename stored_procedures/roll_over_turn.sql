DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS roll_over_turn $$

CREATE PROCEDURE roll_over_turn(
    IN gid INT(11), 
    IN img VARCHAR(64), 
    IN season enum('spring', 'fall'),
    IN yr YEAR(4))
BEGIN
    UPDATE game
    SET pic = img, 
        gam_season = season, 
        gam_year = yr, 
        turn_stage = 1, 
        ended = FALSE
    WHERE game.gam_id = gid;
    
    UPDATE game_membership
    SET game_membership.orders_given = FALSE
    WHERE game_membership.gam_id = gid;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/roll_over_turn.sql