DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS order_types $$

CREATE PROCEDURE order_types (IN stage int(11))
BEGIN
    SELECT order_type.odt_id, order_type.order_text, order_type.operands, order_type.turn_stage
    FROM order_type
    WHERE order_type.turn_stage = stage;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/order_types.sql