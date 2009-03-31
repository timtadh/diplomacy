DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS example3_results $$

CREATE PROCEDURE example3_results()
BEGIN
    SELECT @_example3_1 as 'capitol';
END
$$

DELIMITER ;