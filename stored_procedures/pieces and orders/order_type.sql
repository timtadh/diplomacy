DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS order_type $$

CREATE PROCEDURE order_type (IN odt_id int(11))
BEGIN
    SELECT *
    FROM order_type
    WHERE order_type.odt_id = odt_id;
END
$$

DELIMITER ;
