DELIMITER $$

USE masran

DROP PROCEDURE IF EXISTS delete_grp $$

CREATE PROCEDURE delete_grp(IN usr_id VARCHAR(64), IN exp_id VARCHAR(64), IN grp_id VARCHAR(64))
BEGIN
    DELETE exp_data
    FROM exp_data AS exp_data
        INNER JOIN exp_groups AS exp_grps
        ON (exp_data.grp_id LIKE exp_grps.grp_id)
        INNER JOIN permissions AS perm
        ON (exp_grps.exp_id LIKE perm.exp_id)
    WHERE ((perm.owner LIKE usr_id) 
           AND (perm.exp_id LIKE exp_id)
           AND (exp_grps.grp_id LIKE grp_id));
    
    DELETE exp_grps
    FROM exp_groups AS exp_grps
    INNER JOIN permissions AS perm
    ON (exp_grps.exp_id LIKE perm.exp_id)
    WHERE ((perm.owner LIKE usr_id) 
           AND (perm.exp_id LIKE exp_id)
           AND (exp_grps.grp_id LIKE grp_id));
END
$$

DELIMITER ;