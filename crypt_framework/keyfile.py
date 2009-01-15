#Administration tools for eChat

import re, os, nDDB, qcrypt
import authenticator as auth
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

def create_client_user(login_name, f_name, l_name, salt_hex, email):
    d = {'login_name':login_name, 'f_name':f_name, 'l_name':l_name, 'salt':salt_hex, 'email':email}
    return d

def create_server_user(login_name, f_name, l_name, pass_hash, email):
    d = {'login_name':login_name, 'f_name':f_name, 'l_name':l_name, 'pass_hash':pass_hash, 'email':email}
    return d

def create_key():
    key = RSA.generate(4096, os.urandom)
    return key.__getstate__()

def create_secret():
    return qcrypt.normalize(os.urandom(256))
    
def create_server_keyfile(server_stub_path, user_file_list):
    server_stub = nDDB.openAdvanceDDB(server_stub_path)
    secret = server_stub['secret']
    salt_hex = server_stub['salt']
    user_dict = {}
    for path in user_file_list:
        user = nDDB.openAdvanceDDB(path)
        user_dict.update({user['login_name']:user})
    print 'about to create secret'
    key = create_key()
    print 'secret created'
    d = {'key':key, 'secret':secret, 'salt':salt_hex, 'users':user_dict}
    return d

def add_user_to_server(server_keyfile_path, user_file):
    key = load_server_keyfile(server_keyfile_path)
    user = nDDB.openAdvanceDDB(user_file)
    key['users'].update({user['login_name']:user})
    save_keyfile(key, server_keyfile_path)

def create_server_keystub():
    secret = create_secret()
    salt = qcrypt.normalize(os.urandom(64))
    d = {'secret':secret, 'salt':salt}
    return d
    
def save_stub_files(server_stub):
    secret_hash = auth.saltedhash_hex(qcrypt.denormalize(server_stub['secret']), server_stub['salt'])
    f = open('client_stub', 'w')
    f.write(secret_hash)
    f.close()
    nDDB.saveAdvanceDDB('server_stub', server_stub)

def create_client_keyfile(server_secret_hash, user):
    d = {'server_secret_hash':server_secret_hash, 'user':user}
    return d
    
def save_keyfile(k, path):
    nDDB.saveAdvanceDDB(path, k)

def proc_key_dict(d):
    for k in d.keys():
        try:
            d[k] = long(d[k])
        except:
            pass
    return d

def load_server_keyfile(path):
    k = nDDB.openAdvanceDDB(path)
    k['key'] = proc_key_dict(k['key'])
    return k
    
def load_client_keyfile(path):
    k = nDDB.openAdvanceDDB(path)
    return k
