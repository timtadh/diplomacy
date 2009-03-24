DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS lines_in_terr $$

CREATE PROCEDURE lines_in_terr(IN tid INT(11))
BEGIN
    SELECT line.x1, line.y1, line.x2, line.y2
    FROM line
    INNER JOIN ter_ln_relation
        ON (line.ln_id = ter_ln_relation.ln_id)
    INNER JOIN territory
        ON (ter_ln_relation.ter_id = territory.ter_id)
    WHERE territory.ter_id = tid;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/lines_in_terr.sql