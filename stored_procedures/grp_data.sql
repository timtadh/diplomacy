DELIMITER $$

USE masran

DROP PROCEDURE IF EXISTS grp_data $$

CREATE PROCEDURE grp_data(IN usr_id VARCHAR(64), IN exp_id VARCHAR(64), IN grp_id VARCHAR(64))
BEGIN
    SELECT exp_data.acc AS acc, sprot.uid AS human_acc, exp_data.org_id AS org_id, 
           id_types.type AS id_type, sprot.genename AS genename, sprot.description AS des
    FROM permissions AS perm
        INNER JOIN exp_groups AS exp_grps
        ON (perm.exp_id = exp_grps.exp_id)
        INNER JOIN exp_data AS exp_data
        ON (exp_grps.grp_id = exp_data.grp_id)
        INNER JOIN id_types AS id_types
        ON (exp_data.org_id_type = id_types.type_id)
        INNER JOIN uniprot.sprot as sprot
        ON (exp_data.acc = sprot.acc)
    WHERE ((perm.owner = usr_id) 
            AND (perm.exp_id = exp_id) 
            AND (exp_data.grp_id = grp_id)
            AND (exp_data.acc != ''))
    ORDER BY exp_data.acc;
    
    SELECT exp_data.org_id AS org_id, id_types.type AS id_type, exp_data.org_des AS des
    FROM permissions AS perm
    INNER JOIN exp_groups AS exp_grps
    ON (perm.exp_id = exp_grps.exp_id)
    INNER JOIN exp_data AS exp_data
    ON (exp_grps.grp_id = exp_data.grp_id)
    INNER JOIN id_types AS id_types
    ON (exp_data.org_id_type = id_types.type_id)
    WHERE ((perm.owner = usr_id) 
            AND (perm.exp_id = exp_id)
            AND (exp_data.grp_id = grp_id)
            AND (exp_data.acc = ''))
    ORDER BY exp_data.acc;
    
    SELECT exps.name AS exp_name, exps.description AS des, exp_grps.group_name AS group_name
    FROM permissions AS perm
    INNER JOIN experiments AS exps
    ON (perm.exp_id = exps.exp_id)
    INNER JOIN exp_groups AS exp_grps
    ON (perm.exp_id = exp_grps.exp_id)
    WHERE ((perm.owner = usr_id) 
            AND (perm.exp_id = exp_id) 
            AND (exp_grps.grp_id = grp_id));
    
    SELECT COUNT(exp_data.grp_id) AS group_size_acc
    FROM permissions AS perm
    INNER JOIN experiments AS exps
    ON (perm.exp_id = exps.exp_id)
    INNER JOIN exp_groups AS exp_grps
    ON (perm.exp_id = exp_grps.exp_id)
    INNER JOIN exp_data AS exp_data
    ON (exp_grps.grp_id = exp_data.grp_id)
    WHERE ((perm.owner = usr_id) 
            AND (perm.exp_id = exp_id) 
            AND (exp_grps.grp_id = grp_id)
            AND (exp_data.acc != ''))
    GROUP BY exp_data.grp_id;
    
    SELECT COUNT(exp_data.grp_id) AS group_size_noacc
    FROM permissions AS perm
    INNER JOIN experiments AS exps
    ON (perm.exp_id = exps.exp_id)
    INNER JOIN exp_groups AS exp_grps
    ON (perm.exp_id = exp_grps.exp_id)
    INNER JOIN exp_data AS exp_data
    ON (exp_grps.grp_id = exp_data.grp_id)
    WHERE ((perm.owner = usr_id) 
            AND (perm.exp_id = exp_id) 
            AND (exp_grps.grp_id = grp_id)
            AND (exp_data.acc = ''))
    GROUP BY exp_data.grp_id;
END
$$

DELIMITER ;