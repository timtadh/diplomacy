
--  turn_stages (trs_id : int(11), name : varchar(64), description : varchar(256), 
--               fall : tinyint(1))
--  order_type (odt_id : int(11), order_text : varchar(128))

USE diplomacy;

START TRANSACTION;

INSERT INTO turn_stages (name, description, fall)
VALUES 
    ('new', 'game has been created but not start', 0),
    ('wrt_moves', 'writing movement orders', 0), -- 1
    ('ex_moves', 'executing moves', 0),
    ('wrt_retreats', 'writing retreat and disband orders', 0), -- 3
    ('ex_retreats', 'executing retreats', 0),
    ('wrt_builds', 'writing build and disband orders', 1), -- 5
    ('ex_builds', 'executing builds', 1),
    ('end', 'game completed', 0);

INSERT INTO order_type (order_text, destination, operands, turn_stage, dest_text, op_text)
VALUES ('move', 1, 0, 1, 'Choose Destination', ''), 
       ('support', 1, 1, 1, 'Choose Support Into', 'Choose Territory You Support'), 
       ('hold', 0, 0, 1, '', ''), 
--        ('move via convoy', -1, 1), 
--        ('convoy', 1, 1), 
       ('retreat', 1, 0, 3, 'Choose Where to Retreat', ''), 
       ('disband', 0, 0, 3, '', ''), 
       ('build', 1, 0, 5, 'Choose Where to Build', '');

COMMIT;
