new_game = 'INSERT INTO game (host) VALUES ("%s");'
add_user = 'INSERT INTO game_membership (usr_id, gam_id) VALUES ("%s", %s);'
del_user = 'DELETE FROM game_membership WHERE game_membership.usr_id = "%s" AND game_membership.gam_id = %s;'

give_map_to_game = """
UPDATE game
SET map_id = %s, pic = "%s", turn_stage = 1
WHERE game.gam_id = %s;
"""

give_cty_to_usr = """
UPDATE game_membership
SET game_membership.cty_id = %s
WHERE game_membership.usr_id = "%s" AND game_membership.gam_id = %s;
"""