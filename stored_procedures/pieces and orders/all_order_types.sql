DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS all_order_types $$

CREATE PROCEDURE all_order_types ()
BEGIN
    SELECT order_type.odt_id, order_type.order_text, order_type.operands, order_type.turn_stage
    FROM order_type;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/order_types.sql