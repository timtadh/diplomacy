from socket import *
import thread
import sys, re, os, nDDB, qcrypt, keyfile
import authenticator as auth
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from CommGenerics import SocketGeneric
from CommunicationLink import PillowTalkLink
from ServerGeneric import ServerGeneric, GenericServer_ClientHandler, GenericServer_Listener
from CommandProcessors import PillowTalkProcessor, BroadcastMessageProcessor, FexibleMessageProcessor

END_MARK = 'STOP'
END_LEN = 4

class tcpServer(ServerGeneric):

    def __init__(self, host='', port=21567, bufsize=4096):
        self.HOST = host
        self.PORT = port
        self.BUFSIZE = bufsize
        self.ADDR = (self.HOST, self.PORT)
        self.cliList = []
        self.activeCli = []
        self.hosts = {}
        self.hosts_cliNum = {}
        
        self.keyfile = keyfile.load_server_keyfile('server_key')
        self.pri_key = RSA.generate(1, os.urandom)
        self.pri_key.__setstate__(self.keyfile['key'])
        
        self.secret = qcrypt.denormalize(self.keyfile['secret'])
        self.salt = self.keyfile['salt']
        
        self.users = self.keyfile['users']
        
        self.sock_generic = SocketGeneric(self.HOST, self.PORT, self.BUFSIZE)
        
        super(tcpServer, self).__init__(self.sock_generic, self.keyfile, PillowTalkLink, GenericServer_Listener, \
                                        GenericServer_ClientHandler, PillowTalkProcessor, FexibleMessageProcessor)

server = tcpServer()
server.startServer()
