DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS triangles_in_terr $$

CREATE PROCEDURE triangles_in_terr(IN tid INT(11))
BEGIN
    SELECT triangle.x1, triangle.y1, triangle.x2, triangle.y2, triangle.x3, triangle.y3
    FROM triangle
    WHERE triangle.ter_id = tid;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/triangles_in_terr.sql