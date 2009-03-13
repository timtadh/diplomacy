new_game = 'INSERT INTO game (map_id) VALUES (NULL);'    
add_user = 'INSERT INTO game_membership (usr_id, gam_id) VALUES ("%s", %s);'
del_user = 'DELETE FROM game_membership WHERE game_membership.usr_id = "%s" AND game_membership.gam_id = %s;'