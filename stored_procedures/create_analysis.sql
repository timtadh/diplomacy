DELIMITER $$

USE masran_analysis

DROP PROCEDURE IF EXISTS create_analysis $$

CREATE PROCEDURE create_analysis(IN usr_id VARCHAR(64), IN analysis_id VARCHAR(64))
BEGIN
    INSERT INTO analysis (usr_id, analysis_id)
    VALUES (usr_id, analysis_id);
END
$$

DELIMITER ;
