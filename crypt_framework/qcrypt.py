#methods for AES encryption of stream

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import os

def create_aes_key():
    sha256 = SHA256.new()
    sha256.update(os.urandom(64))
    for x in xrange(5000): sha256.update(sha256.digest())
    return sha256.digest()

def pub_decrypt(ciphertext, key):
    try:
        ciphertext = denormalize(ciphertext)
        plaintext = key.decrypt(ciphertext)
        #print s
        return plaintext
    except:
        return ciphertext

def pub_encrypt(plaintext, key):
    try:
        ciphertext = key.encrypt(plaintext, 0)[0]
        return normalize(ciphertext)
    except:
        return plaintext

def _appendSpaces(plaintext):
    x = 0
    if len(plaintext)%16 != 0:
        x = 16 - len(plaintext)%16
        plaintext += ' '*x
    return plaintext, x
    return d

def aes_encrypt(plaintext, key):
    plaintext, spaces_added = _appendSpaces(plaintext)
    aes = AES.new(key, AES.MODE_CBC)
    ciphertext = normalize(aes.encrypt(plaintext))
    spaces_added = str(spaces_added)
    spaces_added = (2 - len(spaces_added))*'0' + spaces_added
    return ciphertext + spaces_added
    
def aes_decrypt(ciphertext, key):
    try:
        #print 'aes_decrypt try'
        spaces_added = -1*int(ciphertext[-2:])
    except:
        #print 'aes_decrypt except'
        spaces_added = 0
    finally:
        #print 'aes_decrypt finally'
        ciphertext = denormalize(ciphertext[:-2])
    aes = AES.new(key, AES.MODE_CBC)
    plaintext =  aes.decrypt(ciphertext)
    #print plaintext
    if spaces_added: plaintext = plaintext[:spaces_added]
    return plaintext
    
def normalize(text):
    s = ''
    for c in text:
        c = hex(ord(c))[2:]
        c = (2-len(c))*'0'+c
        s += c
    return s

def denormalize(text):
    s = ''
    buf = ''
    for c in text:
        buf += c
        if len(buf) == 2:
            s += chr(int(buf, 16))
            buf = ''
    return s
    
if __name__ == '__main__':
    sha256 = SHA256.new()
    sha256.update('test')
    
    plaintext = 'this is the plaintext'
    ciphertext = encrypt(plaintext, sha256.digest())
    print plaintext
    print ciphertext
    print decrypt(ciphertext, sha256.digest())
