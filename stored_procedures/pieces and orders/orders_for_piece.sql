DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS orders_for_piece $$

CREATE PROCEDURE orders_for_piece(IN pid INT(11))
BEGIN
    SELECT orders.*, odt.order_text, odt.destination AS has_dst, odt.operands
    FROM orders
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

--SOURCE /srv/diplomacy/stored_procedures/orders_for_piece.sql