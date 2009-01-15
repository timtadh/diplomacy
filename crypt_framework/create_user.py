import authenticator as auth
import os, qcrypt, keyfile, nDDB

f = open(raw_input('path of server secret: '), 'r')
s_secret_hash = f.read()
f.close()

f_name = raw_input('first name: ')
l_name = raw_input('last name: ')
print 'the login name is used as a part of the keyfile name so make it conform'
print 'to os standards. Thank you. there is *no* validation.'
login_name = raw_input('login name: ')
email = raw_input('email: ')
password = raw_input('password: ')
salt_hex = qcrypt.normalize(os.urandom(64))
pass_hash = auth.saltedhash_hex(password, salt_hex)

c_user = keyfile.create_client_user(login_name, f_name, l_name, salt_hex, email)
s_user = keyfile.create_server_user(login_name, f_name, l_name, pass_hash, email)

c_keyfile = keyfile.create_client_keyfile(s_secret_hash, c_user)

keyfile.save_keyfile(c_keyfile, login_name+'_keyfile')
nDDB.saveAdvanceDDB(login_name+'_serveruser', s_user)
