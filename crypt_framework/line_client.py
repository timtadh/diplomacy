from Tkinter import *
from socket import *
import thread
import sys, re, os, nDDB, qcrypt, keyfile
import authenticator as auth
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from CommGenerics import SocketGeneric
from CommunicationLink import PillowTalkLink
from ClientGeneric import ClientGeneric
from ClientActivationScripts import PillowTalkActivator
from CommandProcessors import ClientCommandProcessor, ChatClientProcessor

class output(object):
    def __init__(self): self.l = list()
    def printInfo(self, x): self.l.append(x)
    def recieve(self): return self.l.pop()

class tcpClient(ClientGeneric):

    def __init__(self, printer, host, port=21567, bufsize=1024):
        self.HOST = host
        self.PORT = port
        self.BUFSIZE = bufsize
        self.ADDR = (self.HOST, self.PORT)
        self.stop = False
        self.printer = printer
        
        self.keyfile = keyfile.load_client_keyfile('user1_keyfile')
        self.password = 'user1_password'
        
        commGeneric = SocketGeneric(host, port, bufsize)
        
        super(tcpClient, self).__init__(commGeneric, self.keyfile, PillowTalkLink, PillowTalkActivator, \
                                        usr_processor=ChatClientProcessor(self.printer))
        self.link.secret = self.password
    
    def get_usrlist(self):
        self.link.send_message(self.link.format_msg('get_usrlist', None))
    
    def send(self, data):
        m = self.link.format_msg('send_to_all', data)
        super(tcpClient, self).send(m)

client = None

def _start(lock):
    global client
    client = tcpClient(p(), 'localhost')
    try:
        client.activateClient()
    except Exception, e:
        print e
    while 1: pass


def start():
    lock = thread.allocate_lock()
    lock.acquire()
    thread.start_new_thread(_start, (lock,))

if __name__ == '__main__':
    start()
