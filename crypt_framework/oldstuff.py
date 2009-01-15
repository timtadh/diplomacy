class tcpClient:

    def __init__(self, printer, host, port=21567, bufsize=1024):
        printer.setTcpClient(self)
        self.HOST = host
        self.PORT = port
        self.BUFSIZE = bufsize
        self.ADDR = (self.HOST, self.PORT)
        self.stop = False
        self.printer = printer
        
        self.keyfile = keyfile.load_client_keyfile(raw_input('key file path: '))
        
        sha256 = SHA256.new()
        sha256.update(os.urandom(64))
        for x in xrange(5000): sha256.update(sha256.digest())
        self.aeskey = sha256.digest()
        
        self.server_secret_hash = self.keyfile['server_secret_hash']
        self.user = self.keyfile['user']
        
        self.password = raw_input('password: ')
        
        
        self.sockg = SocketGeneric(host, port, bufsize)
        self.link = PillowTalkLink(self.sockg, self.password, self.user['salt'], self.server_secret_hash)
        
        def syscommands(data):
            try: d = nDDB.decode(data)
            except: return
            
            if (not (d.has_key('type') or d.has_key('value'))): return 
            
            command = d['type']
            msg = d['value']
            
            if command == 'stop': self.sockg.close()
        
        self.sockg.set_proc_syscommand(syscommands)
        
        #----------------DEBUG----------------#
        # self.pass_hash = self.user['pass_hash']
        # if self.pass_hash != auth.saltedhash_hex(self.password, self.user['salt']): 
            # print "passwords don't match error"
            # sys.exit()
        # else: print 'passwords match'
        #----------------DEBUG----------------#
        
        self.server_key = None

    def connect(self):
        self.sockg.connect()

    def send(self, data):
        if not data: return
        self.link.send_message(data)

    def stopListening(self):
        self.stop = True
        self.sockg.send_dict({'type':'stop', 'value':None})
        
    def disconnect(self):
        self.sockg.close()

    def deactivateClient(self):
        self.stopListening()
        self.disconnect()
    
    def listen(self, lock=False, stuff=False):
        print 'listening'
        while not self.sockg.closed and self.link.authenticated and self.link.key_agreement:
            cmd, msg, sig = self.process(self.sockg.recieve())
            
            try:
                if cmd == 'message':
                    msg = self.link.recieved_message(msg)
                    self.printer.printInfo(msg)
            except Exception, e:
                print e
                continue
        #self.disconnect()
        if lock: lock.release()
        try:
            gui.root.destroy()
            gui.root.quit()
            sys.exit()
        except: pass
    
    def process(self, data):
        d = nDDB.decode(data)
        if (not (d.has_key('type') or d.has_key('value'))): return None, None, None
        if d.has_key('signature'): return d['type'], d['value'], d['signature']
        return d['type'], d['value'], None
    
    def activateClient(self):
        self.connect()
        
        while not (self.sockg.closed or self.link.authenticated):
            self.link.begin_auth(self.user['login_name'])
            cmd, msg, sig = self.process(self.sockg.recieve())
            if cmd != 'sign_auth': continue
            self.link.sign_auth(msg)
            cmd, msg, sig = self.process(self.sockg.recieve())
            if cmd != 'verification_result': continue
            msg = qcrypt.denormalize(msg)
            msg_vr = auth.verify_signature(self.link.secret, self.link.salt, msg, sig)
            vr = bool(int(msg[0]))
            if not msg_vr: continue
            if vr: print 'server verified client'
            else: 
                cli_sockg.close()
                sys.exit()
            
            self.link.request_auth()
            cmd, msg, sig = self.process(self.sockg.recieve())
            if cmd != 'verify_auth': continue
            vr = self.link.verify_auth(msg)
            if not vr:
                cli_sockg.close()
                sys.exit()
            print 'client verified server'
        
        while not self.sockg.closed and self.link.authenticated and not self.link.pub_key:
            self.sockg.send_dict({'type':'request_pub_key', 'value':None})
            cmd, msg, sig = self.process(self.sockg.recieve())
            if cmd != 'set_pub_key': continue
            self.link.set_pub_key(msg, sig)
        
        if not self.link.authenticated and not self.link.pub_key: return
            
        while not self.sockg.closed and self.link.key_agreement == False:
            self.link.send_new_aes_key()
            cmd, msg, sig = self.process(self.sockg.recieve())
            if cmd != 'confirm_aeskey': continue
            self.link.confirm_aes_key_set(msg, sig)
        
        lock = thread.allocate_lock()
        lock.acquire()
        thread.start_new_thread(self.listen, (lock, True))

















a = None
        self.send_dict(self.tcpCliSock, {'type':'request_auth', 'value':self.user['login_name']})
        while not a:
            data = self.read_data(self.tcpCliSock)
            
            d = nDDB.decode(data)
            
            if d and d.has_key('type') and d.has_key('value') and d['type'] == 'sign_auth':
                a = d['value']
                signed_a = auth.sign_auth(self.password, self.user['salt'], self.server_secret_hash, a)
                d = {'type':'verify_auth', 'value':{'signed_a':signed_a, 'login_name':self.user['login_name']}}
                self.send_dict(self.tcpCliSock, d)
            else:
                self.send_dict(self.tcpCliSock, {'type':'request_auth', 'value':None})
        
        data = self.read_data(self.tcpCliSock)
        
        d = nDDB.decode(data)
        
        if d and d.has_key('type') and d.has_key('value') and d['type'] == 'verification_result':
            print 'asdfaef weawef awef '
            try:
                vr = bool(int(d['value']))
                if not vr: 
                    print 'verification failed'
                    sys.exit()
                print 'server verified client'
            except:
                print 'verification failed'
                sys.exit()
        else:
            print 'wtf'
            sys.exit()
        
        ran_str = os.urandom(64)
        a = auth.create_auth(self.server_secret_hash, ran_str)
        self.send_dict(self.tcpCliSock, {'type':'sign_auth', 'value':a})
        
        data = self.read_data(self.tcpCliSock)
        
        d = nDDB.decode(data)
        
        if d and d.has_key('type') and d.has_key('value') and d['type'] == 'verify_auth':
            print 'about to verify'
            signed_a = d['value']
            vr = auth.verify_auth(self.password, self.user['salt'], ran_str, signed_a)
            self.send_dict(self.tcpCliSock, {'type':'verification_result', 'value':str(int(vr))})
            if not vr: 
                print 'verification failed'
                sys.exit()
            print 'server verified'
        
        # data = ''
        # while data != 'pubkeyset':
            # k = self.pubkey.publickey().__getstate__()
            # k = qcrypt.normalize(nDDB.encode(k))
            # signature = auth.sign_msg(self.server_secret_hash, k)
            # self.send_dict(self.tcpCliSock, {'type':'setpubkey', 'value':k, 'signature':signature})
            # data = self.tcpCliSock.recv(4096)
        
        k = None
        while k is None:
            self.send_dict(self.tcpCliSock, {'type':'getkey', 'value':0})
            data = self.read_data(self.tcpCliSock)
            d = nDDB.decode(data)
            print d
            if d and d.has_key('type') and d.has_key('value') and d['type'] == 'key':
                try:
                    print 'trying to verify message'
                    signature = d['signature']
                    k_dict = d['value']
                    vr = auth.verify_signature(self.password, self.user['salt'], k_dict, signature)
                    print 'verified: ', vr
                    if vr:
                        k_dict = nDDB.decode(qcrypt.denormalize(d['value']))
                        k = RSA.generate(1, os.urandom)
                        k.__setstate__(keyfile.proc_key_dict(k_dict))
                    else:
                        print 'incorrect message signature'
                        k = None
                except:
                    k = None
        
        self.server_key = k
        print k.__getstate__()
        
        data = ''
        while data != 'aeskeyset':
            k = qcrypt.pub_encrypt(self.aeskey, self.server_key)
            signature = auth.sign_msg(self.server_secret_hash, k)
            self.send_dict(self.tcpCliSock, {'type':'setaeskey', 'value':k, 'signature':signature})
            data = self.tcpCliSock.recv(4096)
        
        lock = thread.allocate_lock()
        lock.acquire()
        thread.start_new_thread(self.listen, (lock, True))


















if d and d.has_key('type') and d.has_key('value'):
                
                if d['type'] == 'message' and cliNum in self.authenticated: 
                    l = thread.allocate_lock()
                    l.acquire()
                    thread.start_new_thread(self._process_msg, (cliNum, d, l))
                
                elif d['type'] == 'request_auth':
                    login_name = d['value']
                    cli_secret_hash = self.users[login_name]['pass_hash']
                    ran_str = os.urandom(64)
                    a = auth.create_auth(cli_secret_hash, ran_str)
                    self.authentications.update({cliNum:ran_str})
                    cli = self.cliList[cliNum]
                    self.send_dict(cli, {'type':'sign_auth', 'value':a})
                
                elif d['type'] == 'sign_auth':
                    a = d['value']
                    cli_secret_hash = self.users[login_name]['pass_hash']
                    signed_a = auth.sign_auth(self.secret, self.salt, cli_secret_hash, a)
                    cli = self.cliList[cliNum]
                    self.send_dict(cli, {'type':'verify_auth', 'value':signed_a})
                
                elif d['type'] == 'verify_auth':
                    print 'VERIFY AUTH REACHED'
                    cli = self.cliList[cliNum]
                    if self.authentications.has_key(cliNum):
                        login_name = d['value']['login_name']
                        signed_a = d['value']['signed_a']
                        ran_str = self.authentications[cliNum]
                        vr = auth.verify_auth(self.secret, self.salt, ran_str, signed_a)
                        self.send_dict(cli, {'type':'verification_result', 'value':str(int(vr))})
                        if vr:
                            print 'client verified'
                            self.authenticated.append(cliNum)
                            if self.cliInfo.has_key(cliNum):
                                self.cliInfo[cliNum]['login_name'] = login_name
                            else:
                                self.cliInfo.update({cliNum:{'pubkey':None, 'aeskey':None, 'login_name':login_name}})
                        else:
                            break
                    else:
                        self.send_dict(cli, {'type':'verification_result', 'value':'0'})
                
                elif d['type'] == 'verification_result':
                    try:
                        vr = bool(int(d['value']))
                        if not vr: 
                            print 'verification failed'
                            break
                        print 'client verified server'
                    except:
                        print 'verification failed'
                        break
                
                elif d['type'] == 'getkey' and cliNum in self.authenticated:
                    print 'about to send key'
                    cli = self.cliList[cliNum]
                    k = self.key.publickey().__getstate__()
                    k = qcrypt.normalize(nDDB.encode(k))
                    signature = self._sign_msg(cliNum, k)
                    self.send_dict(cli, {'type':'key', 'value':k, 'signature':signature})
                    print 'key sent'
                    
                elif d['type'] == 'setpubkey' and cliNum in self.authenticated:
                    print 'about to try and set pub key'
                    signature = d['signature']
                    k_dict = d['value']
                    vr = auth.verify_signature(self.secret, self.salt, k_dict, signature)
                    print 'verification: ', vr
                    if vr:
                        k_dict = nDDB.decode(qcrypt.denormalize(d['value']))
                        k = RSA.generate(1, os.urandom)
                        k.__setstate__(keyfile.proc_key_dict(k_dict))
                        if self.cliInfo.has_key(cliNum):
                            self.cliInfo[cliNum]['pubkey'] = k
                        else:
                            self.cliInfo.update({cliNum:{'pubkey':k, 'aeskey':None, 'login_name':None}})
                        self.cliList[cliNum].sendall('pubkeyset')
                    else:
                        print 'incorrect message signature'
                    
                
                elif d['type'] == 'setaeskey' and cliNum in self.authenticated:
                    signature = d['signature']
                    msg_e = d['value']
                    vr = auth.verify_signature(self.secret, self.salt, msg_e, signature)
                    if vr:
                        k = qcrypt.pub_decrypt(msg_e, self.key)
                        if self.cliInfo.has_key(cliNum):
                            self.cliInfo[cliNum]['aeskey'] = k
                        else:
                            self.cliInfo.update({cliNum:{'pubkey':None, 'aeskey':k, 'login_name':None}})
                        self.cliList[cliNum].sendall('aeskeyset')
                    else:
                        print 'incorrect message signature'
                    
                    
                elif d['type'] == 'stop':
                    break
                    
                else:
                    print 'no matching command for current state'