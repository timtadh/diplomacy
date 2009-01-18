DELIMITER $$

USE masran

DROP PROCEDURE IF EXISTS exp_id_exists_results $$

CREATE PROCEDURE exp_id_exists_results()
BEGIN
    SELECT @_exp_id_exists_1 as 'exists';
END
$$

DELIMITER ;