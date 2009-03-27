DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS supply_count $$

CREATE PROCEDURE supply_count (IN gam_id INT(11))
BEGIN
    SELECT t.name AS 'tname', c.name AS 'cname'
	FROM territory AS t, piece AS p, country AS c
	WHERE supply = 1 AND t.gam_id = gam_id AND p.ter_id = t.ter_id AND p.cty_id = c.cty_id
	-- Last statement won't work because gam_id is not in territory, 
	-- but map_id is? How do I match
    
END
$$

DELIMITER ;