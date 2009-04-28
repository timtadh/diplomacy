DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS insert_operand $$

CREATE PROCEDURE insert_operand(IN pid INT(11), IN tid INT(11))
BEGIN
    DECLARE ordid INT(11) DEFAULT 0;
    
    SELECT orders.ord_id INTO ordid
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

    INSERT INTO operands (ord_id, ter_id)
    VALUES (ordid, tid);
END
$$

DELIMITER ;
