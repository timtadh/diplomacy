DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS example2 $$

CREATE PROCEDURE example2(IN country_name VARCHAR(64))
BEGIN
    SELECT countries.capitol
    FROM Praskac_countries as countries
    WHERE countries.name = country_name;
END
$$

DELIMITER ;


--SOURCE /srv/diplomacy/stored_procedures/example_stored_procedure.sql;
