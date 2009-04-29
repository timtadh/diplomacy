DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS move_piece $$

CREATE PROCEDURE move_piece(IN pid INT(11), IN ter_id INT(11))
BEGIN
    UPDATE piece
    SET piece.ter_id = ter_id
    WHERE piece.pce_id = pid;
END
$$

DELIMITER ;
