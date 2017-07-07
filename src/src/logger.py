

import os
import sys
import datetime
import traceback
import sys
import time


class Log(object):

    __shared_state = {}

    CRITICAL = 50
    ERROR = 40
    WARN = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    MAXLEVEL = CRITICAL
    MINLEVEL = NOTSET

    _level_num_to_name = {
                          NOTSET: 'NOTSET',
                          DEBUG: 'DEBUG',
                          INFO: 'INFO',
                          WARN: 'WARN',
                          ERROR: 'ERROR',
                          CRITICAL: 'CRITICAL',
                         }


    _name_to_level_num = {value:key for (key, value) in _level_num_to_name.items()}

    DefaultMaxFname = 15


    def __init__(self, logfile=None, level=NOTSET, append=False, max_fname=DefaultMaxFname, timePrefix=True):

        self.__dict__ = Log.__shared_state

        self.max_fname = max_fname
        self.sym_level = 'NOTSET'      # set in call to check_level()
        self.level = self.check_level(level)

        if logfile is None:
            logfile = '%s.log' % __name__

        if timePrefix:
            timestr = time.strftime("%Y%m%d-%H%M%S")
            logfile = timestr + '-' + logfile

        log_options = 'w'
        if append:
            log_options = 'a'

        try:
            self.logfd = open(logfile, log_options)
            self.logfd.close()
        except IOError:
            basefile = os.path.basename(logfile)
            if sys.platform == 'win32':
                logfile = os.path.join('C:\\', basefile)
            else:
                logfile = os.path.join('~', basefile)

        self.logfd = open(logfile, log_options)
        self.logfile = logfile
        self.debug('='*55)
        self.debug('Log started on %s, log level=%s'
                   % (datetime.datetime.now().ctime(),
                      self._level_num_to_name[level]))
        self.debug('-'*55)
        self.set_level(self.level)

    def check_level(self, level):
        try:
            level = int(level)
        except ValueError:
            msg = "Logging level invalid: '%s'" % str(level)
            print(msg)
            raise Exception(msg)

        if not self.NOTSET <= level <= self.CRITICAL:
            msg = "Logging level invalid: '%s'" % str(level)
            print(msg)
            raise Exception(msg)

        return level

    def set_level(self, level):
        level = self.check_level(level)
        sym = self._level_num_to_name.get(level, None)
        if sym is None:
            sym_10 = 10 * (level/10)
            sym_rem = level - sym_10
            sym = '%s+%d' % (self._level_num_to_name[sym_10], sym_rem)

        self.level = level
        self.sym_level = sym

        self.critical('Logging level set to %02d (%s)' % (level, sym))

    def __call__(self, *msg, level=None):
        if level is None:
            level = self.level

        if level < self.level or self.level < 0:
            return

        if msg is None:
            msg = ''


        to = datetime.datetime.now()
        hr = to.hour
        min = to.minute
        sec = to.second
        msec = to.microsecond

        frames = traceback.extract_stack()
        frames.reverse()
        try:
            (_, mod_name) = __name__.rsplit('.', 1)
        except ValueError:
            mod_name = __name__
        for (fpath, lnum, mname, _) in frames:
            fname = os.path.basename(fpath).rsplit('.', 1)
            if len(fname) > 1:
                fname = fname[0]
            if fname != mod_name:
                break

        loglevel = self._level_num_to_name[level]

        fname = fname[:self.max_fname]
        data= '%02d:%02d:%02d.%06d|%8s|%*s:%-4d|%s\n' % (hr, min, sec, msec, loglevel, self.max_fname,  fname, lnum, msg)
        if level==self.INFO:
            sys.stdout.write(data)

        self.logfd.write(data)
        self.logfd.flush()

    def critical(self, msg):
        self(msg, self.CRITICAL)

    def error(self, msg):
        self(msg, self.ERROR)

    def warn(self, msg):
        self(msg, self.WARN)

    def info(self, msg):
        self(msg, self.INFO)

    def debug(self, msg):
        self(msg, self.DEBUG)

    def __del__(self):
        self.logfd.close()

