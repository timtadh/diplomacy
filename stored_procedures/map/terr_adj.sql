DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS terr_adj $$

-- adjacent (ter_id : int(11), adj_ter_id : int(11))

CREATE PROCEDURE terr_adj(IN tid INT(11))
BEGIN
    SELECT adj.adj_ter_id AS "ter_id"
    FROM adjacent AS adj
    WHERE adj.ter_id = tid;
END
$$

DELIMITER ;

