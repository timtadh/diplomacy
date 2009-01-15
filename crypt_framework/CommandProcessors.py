from socket import *
import thread
import sys, re, os, nDDB, qcrypt, keyfile, traceback
import authenticator as auth
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from CommGenerics import SocketGeneric
from CommunicationLink import PillowTalkLink
from dec_factories import create_existance_check_dec, create_value_check_dec

class CommandProcessor(object):
    
    def exec_command(self, cmd, msg, sig): pass

class ServerCommandProcessor(CommandProcessor):
    
    def __init__(self, uid, comm_link, listener, client_handler):
        self.uid = uid
        self.link = comm_link
        self.listener = listener
        self.client_handler = client_handler
        self.users = self.listener.keyfile['users'] 
    
    def exec_command(self, cmd, msg, sig): pass

class ClientCommandProcessor(CommandProcessor):
    
    def init(self, comm_link, client_generic):
        self.client = client_generic
        self.link = comm_link
    
    def exec_command(self, cmd, msg, sig): pass

class PillowTalkProcessor(ServerCommandProcessor):
    
    def __init__(self, uid, comm_link, listener, client_handler):
        super(PillowTalkProcessor, self).__init__(uid, comm_link, listener, client_handler)
    
    def exec_command(self, cmd, msg, sig):
        #print cmd, msg, sig
        def request_auth(msg): 
            self.link.name = msg
            self.link.partner_secret_hash = self.users[self.link.name]['pass_hash']
            self.link.request_auth()
            
        def sign_auth(msg): self.link.sign_auth(msg)
        def verify_auth(msg): 
            if self.link.verify_auth(msg): print 'server verified client'
        
        def verification_result(msg, sig):
            msg = qcrypt.denormalize(msg)
            msg_vr = auth.verify_signature(self.link.secret, self.link.salt, msg, sig)
            vr = bool(int(msg[0]))
            if not msg_vr: return
            if vr: print 'client verified server'
            else: self.link.comm.close()
            
        def request_pub_key(): self.link.request_pub_key()
        def set_pub_key(msg, sig): self.link.set_pub_key(msg, sig)
        def set_aes_key(msg, sig): self.link.set_aes_key(msg, sig)
        
        if not locals().has_key(cmd): return
        cmd = locals()[cmd]
        
        try:
            if 'sig' in cmd.func_code.co_varnames and 'msg' in cmd.func_code.co_varnames: cmd(msg, sig)
            elif 'msg' in cmd.func_code.co_varnames: cmd(msg)
            else: cmd()
        except Exception, e:
            print '-----------ERROR-----------\n'
            print 'error: ', e
            print 'Error proccessing: ', cmd.__name__
            print 'Message: ', msg
            print 'Sig: ', sig
            print '\n-----------ERROR-----------'

class BroadcastMessageProcessor(ServerCommandProcessor):
    
    def __init__(self, uid, comm_link, listener, client_handler):
        super(BroadcastMessageProcessor, self).__init__(uid, comm_link, listener, client_handler)
    
    def exec_command(self, cmd, msg, sig):
        
        def message(msg):
            m = self.link.recieved_message(msg)
            self.send_to_all(m, self.uid)
        
        if not locals().has_key(cmd): return
        cmd = locals()[cmd]
        
        try:
            if 'sig' in cmd.func_code.co_varnames and 'msg' in cmd.func_code.co_varnames: cmd(msg, sig)
            elif 'msg' in cmd.func_code.co_varnames: cmd(msg)
            else: cmd()
        except Exception, e:
            print '-----------ERROR-----------\n'
            print 'error: ', e
            print 'Error proccessing: ', cmd.__name__
            print 'Message: ', msg
            print 'Sig: ', sig
            print '\n-----------ERROR-----------'
            
    def send_to_all(self, mesg, fromCli):
        name = self.listener.get_client(fromCli).name
        u = self.users[name]
        n = u['l_name'] + ', ' + u['f_name']
        msg = n+': '+mesg
        for x in self.client_handler.active_clients:
            try:
                link = self.listener.get_client(x)
                link.send_message(msg)
            except:
                pass


class FexibleMessageProcessor(ServerCommandProcessor):
    
    def __init__(self, uid, comm_link, listener, client_handler):
        super(FexibleMessageProcessor, self).__init__(uid, comm_link, listener, client_handler)

    def exec_command(self, cmd, msg, sig):
        
        def message(msg):
            a = self.link.process(self.link.recieved_message(msg))
            self.exec_command(*a)
        
        def get_usrlist():
            usrs = dict()
            for k in self.listener.clients:
                l = self.listener.clients[k]
                usrs.update({l.name:k})
            self.link.send_message(self.link.format_msg('set_usrlist', usrs))
        
        def send_to_all(msg):
            self.send_to_all(msg, self.uid)
        
        def send_to_some(msg):
            m = msg['message']
            users = msg['users'].split(',')
            self.send_to_some(m, users, self.uid)
        
        if not locals().has_key(cmd): return
        cmd = locals()[cmd]
        
        try:
            if 'sig' in cmd.func_code.co_varnames and 'msg' in cmd.func_code.co_varnames: cmd(msg, sig)
            elif 'msg' in cmd.func_code.co_varnames: cmd(msg)
            else: cmd()
        except Exception, e:
            print '\n-----------ERROR-----------'
            print 'error: ', e
            print 'Error proccessing: ', cmd.__name__
            print 'Message: ', msg
            print 'Sig: ', sig
            print '-----------ERROR-----------\n'
            
    def send_to_all(self, mesg, from_usr):
        name = self.listener.get_client(from_usr).name
        u = self.users[name]
        n = u['l_name'] + ', ' + u['f_name']
        msg = n+': '+mesg
        for x in self.client_handler.active_clients:
            link = self.listener.get_client(x)
            link.send_message(self.link.format_msg('chatmessage', msg))
    
    def send_to_some(self, mesg, users, from_usr):
        name = self.listener.get_client(from_usr).name
        u = self.users[name]
        n = u['l_name'] + ', ' + u['f_name']
        msg = n+': '+mesg
        for x in users:
            link = self.listener.get_client(x)
            if link: link.send_message(self.link.format_msg('chatmessage', msg))
            else:
                self.link.send_message(self.link.format_msg('error', 'user id %s did not exist' % (x,)))
                return
        self.link.send_message(self.link.format_msg('chatmessage', msg))


class ChatClientProcessor(ClientCommandProcessor):
    
    def __init__(self, printer): self.printer = printer
    
    def exec_command(self, cmd, msg, sig):
        
        def message(msg):
            a = self.link.process(self.link.recieved_message(msg))
            self.exec_command(*a)
        
        def error(msg):
            self.printer.printInfo(msg)
        
        def set_usrlist(msg):
            self.client.connected_users = msg
        
        def chatmessage(msg):
            self.printer.printInfo(msg)
            
        if not locals().has_key(cmd): return
        cmd = locals()[cmd]
        
        try:
            if 'sig' in cmd.func_code.co_varnames and 'msg' in cmd.func_code.co_varnames: cmd(msg, sig)
            elif 'msg' in cmd.func_code.co_varnames: cmd(msg)
            else: cmd()
        except Exception, e:
            print '\n-----------ERROR-----------'
            print 'error: ', e
            print 'Error proccessing: ', cmd.__name__
            print 'Message: ', msg
            print 'Sig: ', sig
            print '-----------ERROR-----------\n'
