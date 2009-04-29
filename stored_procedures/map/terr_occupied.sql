DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS terr_occupied $$

CREATE PROCEDURE terr_occupied(IN ter_id INT(11))
BEGIN
    SELECT *
    FROM piece
    WHERE piece.ter_id = ter_id;
END
$$

DELIMITER ;
