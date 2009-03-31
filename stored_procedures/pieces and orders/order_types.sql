DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS order_types $$

CREATE PROCEDURE order_types ()
BEGIN
    SELECT order_type.odt_id, order_type.order_text
    FROM order_type;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/order_types.sql