#Implements a challenge-response authentication scheme
#
#PillowTalk_Auth

from Crypto.Cipher import AES, XOR
from Crypto.Hash import SHA256
import qcrypt, os, stat

#note: it turns out that two way single secrete authentication may be harder than it seems
      #I need to rethink my entire scheme as it is subject to replay attacks against it

debug = False
HASH_REPS = 50000

def __saltedhash(string, salt):
    sha256 = SHA256.new()
    sha256.update(string)
    sha256.update(qcrypt.denormalize(salt))
    for x in xrange(HASH_REPS): 
        sha256.update(sha256.digest())
        if x % 10: sha256.update(salt)
    return sha256

def saltedhash_bin(string, salt):
    return __saltedhash(string, salt).digest()

def saltedhash_hex(string, salt):
    return __saltedhash(string, salt).hexdigest()

def __hash(string):
    sha256 = SHA256.new()
    sha256.update(string)
    for x in xrange(HASH_REPS): sha256.update(sha256.digest())
    return sha256

def hash_bin(string):
    return __hash(string).digest()

def hash_hex(string):
    return __hash(string).hexdigest()
    
def get_some_pi(max_start, message_hex):
    p = int(message_hex[:4], 16)
    while (p > max_start): p = p/2
    f = open('pi.bin', 'rb')
    f.seek(p)
    pi = f.read(len(message_hex)/2)
    f.close()
    return pi

def xor_in_pi(text_bin):
    flen = int(os.stat('pi.bin')[stat.ST_SIZE])
    max_start = flen - len(text_bin)
    some_pi = get_some_pi(max_start, qcrypt.normalize(text_bin))
    xor = XOR.new(some_pi)
    ciphertext = xor.encrypt(text_bin)
    if debug:
        print '\n------xor_in_pi------'
        print qcrypt.normalize(text_bin)
        print qcrypt.normalize(some_pi)
        print qcrypt.normalize(ciphertext)
        print '------xor_in_pi------\n'
    
    return ciphertext

def create_auth(secret_hash_normalized, random_str):
    if len(random_str)%16 != 0: raise Exception, 'not len(random_str) === 16 mod 16'
    aes = AES.new(qcrypt.denormalize(secret_hash_normalized), AES.MODE_CBC)
    ciphertext = qcrypt.normalize(aes.encrypt(random_str))
    if debug:
        print '\n------create_auth------'
        print secret_hash_normalized
        print ciphertext
        print '-----create_auth-------\n'
    return ciphertext

def sign_auth(secret, salt, secret_hash_normalized, auth_normalized):
    auth = qcrypt.denormalize(auth_normalized)
    aes = AES.new(saltedhash_bin(secret, salt), AES.MODE_CBC)
    plaintext = aes.decrypt(auth)
    new_plaintext = xor_in_pi(plaintext)
    aes = AES.new(qcrypt.denormalize(secret_hash_normalized), AES.MODE_CBC)
    ciphertext = qcrypt.normalize(aes.encrypt(new_plaintext))
    if debug:
        print '\n------sign_auth------'
        print saltedhash_hex(secret, salt)
        print secret_hash_normalized
        print ciphertext
        print '-----sign_auth-------\n'
    return ciphertext

def verify_auth(secret, salt, org_random_str, auth_normalized):
    xored_random_str = xor_in_pi(org_random_str)
    auth = qcrypt.denormalize(auth_normalized)
    aes = AES.new(saltedhash_bin(secret, salt), AES.MODE_CBC)
    new_random_str = aes.decrypt(auth)
    if debug:
        print '\n------verify_auth------'
        print saltedhash_hex(secret, salt)
        print qcrypt.normalize(xored_random_str)
        print qcrypt.normalize(new_random_str)
        print '------verify_auth------\n'
    return bool(xored_random_str == new_random_str)

def sign_msg(secret_hash_normalized, msg):
    plaintext, spaces_added = qcrypt._appendSpaces(msg)
    aes = AES.new(qcrypt.denormalize(secret_hash_normalized), AES.MODE_CBC)
    ciphertext = aes.encrypt(plaintext)
    signature = hash_hex(ciphertext)
    return signature

def verify_signature(secret, salt, msg, signature):
    plaintext, spaces_added = qcrypt._appendSpaces(msg)
    aes = AES.new(saltedhash_bin(secret, salt), AES.MODE_CBC)
    ciphertext = aes.encrypt(plaintext)
    new_signature = hash_hex(ciphertext)
    return bool(new_signature == signature)

if __name__ == '__main__':
    debug = True
    
    s_pass = 'leigh'
    c_pass = 'tim'
    s_salt = qcrypt.normalize(os.urandom(32))
    c_salt = qcrypt.normalize(os.urandom(32))
    s_ps_h = saltedhash_hex(s_pass, s_salt)
    c_ps_h = saltedhash_hex(c_pass, c_salt)
    ran_str = os.urandom(32) #should be larger in reality. this is so it fits on my screen
    
    print '\n------random_str------'
    print qcrypt.normalize(ran_str)
    print '------random_str------\n'
    
    a1 = create_auth(c_ps_h, ran_str)
    a2 = sign_auth(c_pass, c_salt, s_ps_h, a1)
    r = verify_auth(s_pass, s_salt, ran_str, a2)
    print r