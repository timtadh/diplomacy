DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS current_game_orders $$

CREATE PROCEDURE current_game_orders(IN gid INT(11))
BEGIN
    SELECT piece.pce_id, orders.order_type, order_type.order_text, country.cty_id
    FROM piece
    INNER JOIN country
        ON (country.cty_id = piece.cty_id)
    INNER JOIN orders
        ON (orders.pce_id = piece.pce_id)
    INNER JOIN order_type
        ON (orders.order_type = order_type.odt_id)
    INNER JOIN game
        ON (country.gam_id = game.gam_id)
    WHERE country.gam_id = gid
        AND game.gam_season = orders.gam_season
        AND game.gam_year = orders.gam_year
    ORDER BY piece.pce_id;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/orders_for_user.sql 
