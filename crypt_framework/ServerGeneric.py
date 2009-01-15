from socket import *
import thread
import sys, re, os, nDDB, qcrypt, keyfile
import authenticator as auth
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from CommGenerics import SocketGeneric
from CommandProcessors import ServerCommandProcessor

class GenericServer_Listener(object):
    
    def __init__(self, commGeneric, keyfile, comm_link_class, client_handler_class, \
                 sys_processor_class=ServerCommandProcessor, usr_processor_class=ServerCommandProcessor):
        self.commGeneric = commGeneric
        self.keyfile = keyfile
        self.client_handler_class = client_handler_class
        self.sys_processor_class = sys_processor_class
        self.comm_link_class = comm_link_class
        self.clients = {}
        self.usr_processor_class = usr_processor_class
    
    def start_listening(self):
        self.commGeneric.listen()
        
        handler = self.client_handler_class(self, self.sys_processor_class, self.usr_processor_class)
        
        print 'waiting for connections...'
        while 1:
            socket_generic = self.commGeneric.accept()
            comm_link = self.comm_link_class(socket_generic, self.keyfile)
            
            uid = self.get_uid()
            self.clients.update({uid:comm_link})
            
            print "new connection to " + str(socket_generic.ADDR) + " with a uid of " + uid
            
            lock = thread.allocate_lock()
            lock.acquire()
            thread.start_new_thread(handler.handle, (uid, comm_link, lock))
    
    def get_uid(self):
        uid = None
        while uid == None or self.clients.has_key(uid): uid = qcrypt.normalize(os.urandom(8))
        return uid
    
    def get_client(self, uid):
        if self.clients.has_key(uid): return self.clients[uid]
        else: return None
    
    def remove_client(self, uid):
        if self.clients.has_key(uid) and self.clients[uid].comm.closed:
            del self.clients[uid]
        else: raise Exception, 'tried to delete a non-existant or in-use client link'

class GenericServer_ClientHandler(object):
    
    def __init__(self, server_listener, sys_processor_class, usr_processor_class):
        self.server_listener = server_listener
        self.active_clients = []
        self.sys_processor_class = sys_processor_class
        self.usr_processor_class = usr_processor_class
        print sys_processor_class
    
    def handle(self, uid, comm_link, lock):
        self.active_clients.append(uid)
        comm_generic = comm_link.comm
        sys_proc = self.sys_processor_class(uid, comm_link, self.server_listener, self)
        usr_proc = self.usr_processor_class(uid, comm_link, self.server_listener, self)
        
        def syscommands(data):
            try: cmd, msg, sig = comm_link.process(data)
            except: return
            
            if cmd == 'stop':  
                comm_generic.close()
                return
            
            sys_proc.exec_command(cmd, msg, sig)
        
        comm_generic.set_proc_syscommand(syscommands)
        
        def commands(data):
            try: cmd, msg, sig = comm_link.process(data)
            except: return
            
            usr_proc.exec_command(cmd, msg, sig)
        
        comm_generic.set_proc_command(commands)
        
        print 'about to listen'
        while not comm_generic.closed:
            try:
                cmd, msg, sig = comm_link.recieve()
            except Exception, e:
                print e
        
        for i, item in enumerate(self.active_clients):
            if item == uid:
                del self.active_clients[i]
                break
        
        self.server_listener.remove_client(uid)
        
        print 'disconnected from: ', comm_generic.ADDR, uid
        lock.release()

class ServerGeneric(object):
    
    def __init__(self, commGeneric, keyfile, comm_link_class, listener_class, \
                 client_handler_class, sys_processor_class, usr_processor_class):
        self.listener = listener_class(commGeneric, keyfile, comm_link_class, \
                                       client_handler_class, sys_processor_class, usr_processor_class)
        self.keyfile = keyfile
        
    def startServer(self): self.listener.start_listening()

