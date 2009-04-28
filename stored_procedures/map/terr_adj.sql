DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS terr_adj $$

-- adjacent (ter_id : int(11), adj_ter_id : int(11))

CREATE PROCEDURE terr_adj(IN tid INT(11))
BEGIN
    SELECT territory.*
    FROM adjacent AS adj
    INNER JOIN territory
        ON (territory.ter_id = adj.adj_ter_id)
    WHERE adj.ter_id = tid;
END
$$

DELIMITER ;

