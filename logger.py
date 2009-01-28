#!/usr/bin/python
import time
import logging
import logging.handlers


class Logger(object):
    
    def __init__(self, file_name):
        self.name = file_name.split('/')[-1].split('.')[0]
        self.file_name = 'logs/' + self.name + '.log'
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.handlers.RotatingFileHandler(self.file_name, maxBytes=1000000, backupCount=5)
        self.formatter = logging.Formatter("%(message)s")
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

        try:
            self.file = open(self.file_name, 'a')
            self.writeln('\n\n')
            self.write('------------')
            self.write(time.strftime('%Y-%m-%d %H:%M:%S'))
            self.write('------------')
            self.writeln()
        except Exception, e:
            print "Content-type: text/html"
            print
            print '<h1>Logger Error</h1>'
            print e, '<br>'
            print e.args, '<br>'
    
    def __del__(self):
        self.file.close()
    
    def __prep(self, t):
        s = ' '.join([str(x) for x in t])
        return s
    
    def write(self, *args):
        self.file.write(self.__prep(args))
        self.file.flush()
    
    def writeln(self, *args):
        self.file.write(self.__prep(args))
        self.file.write('\n')
        self.file.flush()

if __name__ == '__main__':
    l = Logger('test.py')
    import time
    l.writeln()
    l.writeln(time.time())
