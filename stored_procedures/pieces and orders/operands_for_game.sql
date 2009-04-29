DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS operands_for_game $$

CREATE PROCEDURE operands_for_game(IN gam_id INT(11))
BEGIN
    SELECT orders.pce_id, operands.*, territory.name, odt.operands AS num_operands
    FROM operands
    INNER JOIN orders
        ON (orders.ord_id = operands.ord_id)
    INNER JOIN order_type AS odt
        ON (orders.order_type = odt.odt_id)
    INNER JOIN country
        ON (country.cty_id = orders.cty_id)
    INNER JOIN game
        ON (country.gam_id = game.gam_id)
    INNER JOIN territory
        ON (operands.ter_id = territory.ter_id)
    WHERE game.gam_id = gam_id
        AND game.gam_season = orders.gam_season
        AND game.gam_year = orders.gam_year;
END
$$

DELIMITER ;