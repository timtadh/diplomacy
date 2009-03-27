DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS orders_by_ter $$

CREATE PROCEDURE orders_by_ter(IN gid INT(11), IN uid VARCHAR(64))
BEGIN
    SELECT piece.pce_type, territory.name, territory.abbrev, orders.order_type
    FROM piece
    INNER JOIN territory
        ON (territory.ter_id = piece.ter_id)
    INNER JOIN country
        ON (country.cty_id = piece.cty_id)
    INNER JOIN orders
        ON (orders.pce_id = piece.pce_id)
    WHERE country.usr_id = uid AND country.gam_id = gid
    ORDER BY territory.abbrev;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/orders_by_ter.sql