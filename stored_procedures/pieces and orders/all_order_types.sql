DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS all_order_types $$

CREATE PROCEDURE all_order_types ()
BEGIN
    SELECT *
    FROM order_type;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/order_types.sql