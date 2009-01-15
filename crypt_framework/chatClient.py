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

END_MARK = 'STOP'
END_LEN = 4

class output:
    def __init__(self, name='Tim'):
        self.name = name+':\t'

    def setGui(self, gui):
        self.gui = gui

    def setTcpClient(self, tcp_client):
        self.tcp_client = tcp_client
        
    def printInfo(self, data):
        self.gui.printText.insert(END, str(data)+'\n')

    def sendInfo(self, data):
        self.tcp_client.send(data)

class Gui:
    def __init__(self, root, printer):
        printer.setGui(self)
        self.printer = printer
        self.root = root
        self.root.title('chatter')

        self.printText = Text(self.root)
        self.enterText = Entry(self.root)
        self.exit = Button(self.root, {'text':'Exit', 'command':self.exit})
        self.get_usrlist = Button(self.root, {'text':'get user list', 'command':self.get_usrlist})

        self.printText.pack()
        self.enterText.pack()
        self.exit.pack(side=RIGHT)
        self.get_usrlist.pack(side=RIGHT)

        self.enterText.bind('<Return>', self.inputText)

    def inputText(self, event):
        printer.sendInfo(self.enterText.get())
        self.enterText.delete(0, END)
    
    def get_usrlist(self):
        self.printer.tcp_client.get_usrlist()
    
    def exit(self):
        tcpclient.deactivateClient()
        try:
            gui.root.destroy()
            self.root.quit()
        except:
            pass

class tcpClient(ClientGeneric):

    def __init__(self, printer, host, port=21567, bufsize=1024):
        printer.setTcpClient(self)
        self.HOST = host
        self.PORT = port
        self.BUFSIZE = bufsize
        self.ADDR = (self.HOST, self.PORT)
        self.stop = False
        self.printer = printer
        
        self.keyfile = keyfile.load_client_keyfile(raw_input('key file path: '))
        self.password = raw_input('password: ')
        
        commGeneric = SocketGeneric(host, port, bufsize)
        
        super(tcpClient, self).__init__(commGeneric, self.keyfile, PillowTalkLink, PillowTalkActivator, \
                                        usr_processor=ChatClientProcessor(self.printer))
        self.link.secret = self.password
        
        def customExit():
            try:
                gui.root.destroy()
                gui.root.quit()
                sys.exit()
            except: pass
        self.exit = customExit
    
    def get_usrlist(self):
        self.link.send_message(self.link.format_msg('get_usrlist', None))
    
    def send(self, data):
        m = self.link.format_msg('send_to_all', data)
        super(tcpClient, self).send(m)

if __name__ == '__main__':
    printer = output()
    tcpclient = tcpClient(printer, 'localhost')
    tcpclient.activateClient()
    master = Tk()
    gui = Gui(master, printer)
    
    master.mainloop()


