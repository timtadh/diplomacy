DELIMITER $$

USE eecs341

DROP PROCEDURE IF EXISTS hw8_steve $$

CREATE PROCEDURE hw8_steve(IN month_in VARCHAR(32), IN cid_in INT(11), IN aid_in INT(11), IN pid_in INT(11), IN qty_in INT(11), IN dollars_in FLOAT)
BEGIN
    DECLARE product_price FLOAT DEFAULT 0;
    DECLARE agent_commission FLOAT DEFAULT 0;
    DECLARE cust_discount FLOAT DEFAULT 0;
    DECLARE dollars_calculated FLOAT DEFAULT 0;
    
    SELECT products.price INTO product_price
    FROM products
    WHERE products.pid = pid_in;
    
    SELECT agents.commission INTO agent_commission
    FROM agents
    WHERE agents.aid = aid_in;
    
    SELECT customers.discnt INTO cust_discount
    FROM customers
    WHERE customers.cid = cid_in;
    
    SELECT (qty_in*product_price + agent_commission*product_price - cust_discount) INTO dollars_calculated;
    
    IF dollars_calculated = dollars_in THEN
        INSERT INTO orders (month, cid, aid, pid, qty, dollars)
        VALUES (month_in, cid_in, aid_in, pid_in, qty_in, dollars_in);
    END IF;
    
    SELECT orders.ordno
    FROM orders
    ORDER BY ordno DESC
    LIMIT 1;
END
$$

DELIMITER ;

--SOURCE /srv/diplomacy/stored_procedures/hw8_steve.sql