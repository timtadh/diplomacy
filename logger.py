#!/usr/bin/python
import time
import logging
import logging.handlers
import os


class Logger(object):
    
    def __init__(self, file_name):
        self.name = file_name.split('/')[-1].split('.')[0]
        self.file_name = 'logs/' + self.name + '.log'
        try:
            self.logger = logging.getLogger(self.name)
            self.logger.setLevel(logging.DEBUG)
            self.handler = logging.handlers.RotatingFileHandler(self.file_name, maxBytes=1000000, backupCount=5)
            self.formatter = logging.Formatter("%(message)s")
            self.handler.setFormatter(self.formatter)
            self.logger.addHandler(self.handler)
            self.writeln('\n\n', '------------', time.strftime('%Y-%m-%d %H:%M:%S'), '------------')
            try:
                self.writeln('ip-addr: ', os.environ['REMOTE_ADDR'], '   script-name: ', os.environ['SCRIPT_NAME'])
                self.writeln('user-agent: ', os.environ['HTTP_USER_AGENT'])
            except Exception, e:
                self.writeln('\nERROR: ', e)
        except Exception, e:
            print "Content-type: text/html"
            print
            print '<h1>Logger Error</h1>'
            print e, '<br>'
            print e.args, '<br>'
    
    def __prep(self, t):
        s = ' '.join([str(x) for x in t])
        return s
    
    def writeln(self, *args):
        self.logger.info(self.__prep(args))

if __name__ == '__main__':
    l = Logger('test.py')
    import time
    l.writeln(time.time())
