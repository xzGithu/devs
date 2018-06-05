import logging
import time

rq = time.strftime('%Y%m%d',time.localtime(time.time()))
setting = {
           'logpath':'d:/',
           'filename':'xxx_' + rq + '.log'
           }

class Log(object):
    ''' '''
    def __init__(self, name,logname):
        # self.path = setting['logpath']
        # self.filename = setting['filename']
        self.logname=logname
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)
        self.fh = logging.FileHandler(self.logname)
        self.fh.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(threadName)s - %(name)s - %(message)s')
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def close(self):
        self.logger.removeHandler(self.fh)
