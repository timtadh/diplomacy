from Tkinter import *
from socket import *
import thread
import sys, re, os, nDDB, qcrypt, keyfile
import authenticator as auth
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from CommGenerics import SocketGeneric
from CommandProcessors import ClientCommandProcessor

class ClientGeneric(object):

    def __init__(self, commGeneric, keyfile, comm_link_class, activationScript, \
                 sys_processor=ClientCommandProcessor(), usr_processor=ClientCommandProcessor()):
        self.stop = False
        self.activate = activationScript
        self.keyfile = keyfile
        
        self.commGeneric = commGeneric
        self.link = comm_link_class(self.commGeneric, self.keyfile)
        
        sys_processor.init(self.link, self)
        usr_processor.init(self.link, self)
        
        def syscommands(data):
            try: cmd, msg, sig = self.link.process(data)
            except: return
            
            if cmd == 'stop': self.commGeneric.close()
            
            sys_processor.exec_command(cmd, msg, sig)
        
        self.commGeneric.set_proc_syscommand(syscommands)
        
        def commands(data):
            try: cmd, msg, sig = self.link.process(data)
            except Exception, e:
                print e
                return
            
            usr_processor.exec_command(cmd, msg, sig)
        
        self.commGeneric.set_proc_command(commands)
        
        self.exit = sys.exit

    def connect(self):
        self.commGeneric.connect()

    def send(self, data):
        if not data: return
        self.link.send_message(data)

    def stopListening(self):
        self.stop = True
        self.link.send('stop', None)
        
    def disconnect(self):
        self.commGeneric.close()

    def deactivateClient(self):
        self.stopListening()
        self.disconnect()
    
    def listen(self, lock=False):
        print 'listening'
        while not self.commGeneric.closed and self.link.authenticated and self.link.key_agreement:
            cmd, msg, sig = self.link.recieve()
        #self.disconnect()
        if lock: lock.release()
        self.exit()
    
    def activateClient(self):
        self.connect()
        
        self.activate(self)
        
        lock = thread.allocate_lock()
        lock.acquire()
        thread.start_new_thread(self.listen, (lock,))
