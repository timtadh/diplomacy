DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS example_stored_procedure $$

CREATE PROCEDURE example_stored_procedure()
BEGIN
    SELECT * FROM Praskac_countries;
END
$$

DELIMITER ;


--SOURCE /srv/diplomacy/stored_procedures/example_stored_procedure.sql;
