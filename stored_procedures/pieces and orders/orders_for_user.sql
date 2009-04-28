DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS orders_for_user $$

CREATE PROCEDURE orders_for_user(IN gid INT(11), IN uid VARCHAR(64))
BEGIN
    SELECT piece.pce_id, orders.order_type, order_type.order_text, 
           orders.destination AS destination, territory.name AS dst_name,
           order_type.destination AS has_dst
    FROM piece
    INNER JOIN country
        ON (country.cty_id = piece.cty_id)
    INNER JOIN orders
        ON (orders.pce_id = piece.pce_id)
    INNER JOIN order_type
        ON (orders.order_type = order_type.odt_id)
    INNER JOIN territory
        ON (orders.destination = territory.ter_id OR orders.destination IS NULL)
    WHERE country.usr_id = uid AND country.gam_id = gid;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/orders_for_user.sql