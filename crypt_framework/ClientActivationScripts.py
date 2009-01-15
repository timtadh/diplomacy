from Tkinter import *
from socket import *
import thread
import sys, re, os, nDDB, qcrypt, keyfile
import authenticator as auth
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from CommGenerics import SocketGeneric
from CommunicationLink import PillowTalkLink

def PillowTalkActivator(client):
    client.link.name = client.keyfile['user']['login_name']
    while not (client.commGeneric.closed or client.link.authenticated):
        client.link.begin_auth(client.link.name)
        cmd, msg, sig = client.link.recieve()
        if cmd != 'sign_auth': continue
        client.link.sign_auth(msg)
        cmd, msg, sig = client.link.recieve()
        if cmd != 'verification_result': continue
        msg = qcrypt.denormalize(msg)
        msg_vr = auth.verify_signature(client.link.secret, client.link.salt, msg, sig)
        vr = bool(int(msg[0]))
        if not msg_vr: continue
        if vr: print 'server verified client'
        else: 
            client.link.comm.close()
            sys.exit()
        
        client.link.request_auth()
        cmd, msg, sig = client.link.recieve()
        if cmd != 'verify_auth': continue
        vr = client.link.verify_auth(msg)
        if not vr:
            client.link.comm.close()
            sys.exit()
        print 'client verified server'
    
    while not client.commGeneric.closed and client.link.authenticated and not client.link.pub_key:
        client.link.send('request_pub_key', None)
        cmd, msg, sig = client.link.recieve()
        if cmd != 'set_pub_key': continue
        client.link.set_pub_key(msg, sig)
    
    if not client.link.authenticated and not client.link.pub_key: return
        
    while not client.commGeneric.closed and client.link.key_agreement == False:
        client.link.send_new_aes_key()
        cmd, msg, sig = client.link.recieve()
        if cmd != 'confirm_aeskey': continue
        client.link.confirm_aes_key_set(msg, sig)
