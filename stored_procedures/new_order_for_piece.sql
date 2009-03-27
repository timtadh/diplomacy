DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS new_order_for_piece $$

CREATE PROCEDURE new_order_for_piece(IN pid INT(11), IN odt INT(11))
BEGIN
    DECLARE c_gam_season ENUM('spring', 'fall');
    DECLARE c_gam_year YEAR(4);
    DECLARE c_gam_id INT(11);
    DECLARE c_cty_id INT(11);
    
    SELECT game.gam_id, game.gam_season, game.gam_year, country.cty_id 
        INTO c_gam_id, c_gam_season, c_gam_year, c_cty_id
    FROM piece
    INNER JOIN country
        ON (country.cty_id = piece.cty_id)
    INNER JOIN game
        ON (country.gam_id = game.gam_id)
    WHERE piece.pce_id = pid;
    
    DELETE orders.*
    FROM orders
    WHERE orders.pce_id = pid 
        AND orders.gam_season = c_gam_season
        AND orders.gam_year = c_gam_year;
    
    INSERT INTO orders (cty_id, pce_id, gam_season, gam_year, order_type, destination, executed)
    VALUES (c_cty_id, pid, c_gam_season, c_gam_year, odt, NULL, 0);
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/new_order_for_piece.sql