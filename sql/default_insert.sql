
--  turn_stages (trs_id : int(11), name : varchar(64), description : varchar(256), 
--               fall : tinyint(1))
--  order_type (odt_id : int(11), order_text : varchar(128))

USE diplomacy;

START TRANSACTION;

INSERT INTO turn_stages (name, description, fall)
VALUES 
    ('new', 'game has been created but not start', 0),
    ('wrt_moves', 'writing movement orders', 0),
    ('ex_moves', 'executing moves', 0),
    ('wrt_retreats', 'writing retreat and disband orders', 0),
    ('ex_retreats', 'executing retreats', 0),
    ('wrt_builds', 'writing build and disband orders', 1),
    ('ex_builds', 'executing builds', 1),
    ('end', 'game completed', 0);

INSERT INTO order_type (order_text)
VALUES ('move'), ('move via convoy'), ('support'), ('convoy'), ('hold'), 
       ('retreat'), ('disband'), ('build');

COMMIT;
