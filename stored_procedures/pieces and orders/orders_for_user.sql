DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS orders_for_user $$

CREATE PROCEDURE orders_for_user(IN gid INT(11), IN uid VARCHAR(64))
BEGIN
    SELECT DISTINCT piece.pce_id, orders.order_type, order_type.order_text, 
           orders.destination AS destination, territory.name AS dst_name,
           order_type.destination AS has_dst
    FROM piece
    INNER JOIN country
        ON (country.cty_id = piece.cty_id)
    INNER JOIN orders
        ON (orders.pce_id = piece.pce_id)
    INNER JOIN order_type
        ON (orders.order_type = order_type.odt_id)
    LEFT JOIN territory
        ON (orders.destination = territory.ter_id)
    INNER JOIN game
        ON (country.gam_id = game.gam_id)
    WHERE country.usr_id = uid AND country.gam_id = gid
        AND game.gam_season = orders.gam_season
        AND game.gam_year = orders.gam_year;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/orders_for_user.sql