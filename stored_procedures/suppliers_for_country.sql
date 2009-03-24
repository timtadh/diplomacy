DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS suppliers_for_country $$

CREATE PROCEDURE suppliers_for_country(IN cid INT(11))
BEGIN
    SELECT supplier.ter_id
    FROM supplier
    WHERE supplier.cty_id = cid;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/suppliers_for_country.sql