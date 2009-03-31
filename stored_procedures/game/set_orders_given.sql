DELIMITER $$

USE diplomacy

DROP PROCEDURE IF EXISTS set_orders_given $$

CREATE PROCEDURE set_orders_given(IN uid VARCHAR(64), IN gid INT(11))
BEGIN
    UPDATE game_membership
    SET game_membership.orders_given = TRUE
    WHERE game_membership.gam_id = gid AND game_membership.usr_id = uid;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/set_orders_given.sql