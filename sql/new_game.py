new_game = 'INSERT INTO game (host) VALUES ("%s");'
add_user = 'INSERT INTO game_membership (usr_id, gam_id) VALUES ("%s", %s);'
del_user = 'DELETE FROM game_membership WHERE game_membership.usr_id = "%s" AND game_membership.gam_id = %s;'

give_map_to_game = """
UPDATE game
SET map_id = %s, pic = "%s", turn_stage = 1
WHERE game.gam_id = %s;
"""

give_cty_to_usr = """
UPDATE country
SET country.usr_id = "%s"
WHERE country.cty_id = %s AND country.gam_id = %s;
"""