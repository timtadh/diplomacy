DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS example3 $$

CREATE PROCEDURE example3(IN country_name VARCHAR(64), OUT capitol VARCHAR(64))
BEGIN
    SELECT countries.capitol
    INTO capitol
    FROM Praskac_countries as countries
    WHERE countries.name = country_name;
END
$$

DELIMITER ;


--SOURCE /srv/diplomacy/stored_procedures/example_stored_procedure.sql;
