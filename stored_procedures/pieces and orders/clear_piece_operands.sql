DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS clear_piece_operands $$

CREATE PROCEDURE clear_piece_operands(IN pid INT(11))
BEGIN
    DELETE operands
    FROM operands
    INNER JOIN orders
        ON (orders.ord_id = operands.ord_id)
    INNER JOIN order_type AS odt
        ON (orders.order_type = odt.odt_id)
    INNER JOIN country
        ON (country.cty_id = orders.cty_id)
    INNER JOIN game
        ON (country.gam_id = game.gam_id)
    WHERE orders.pce_id = pid 
        AND game.gam_season = orders.gam_season
        AND game.gam_year = orders.gam_year;
END
$$

DELIMITER ;
