from flask import Flask

app = Flask(__name__)
from app import views
import logging
import os
from logging.handlers import TimedRotatingFileHandler

LOGGING_FORMAT = '[%(asctime)s][%(levelname)s][%(name)s] : %(message)s'

class ClosingTimeRotatingFileHandler(TimedRotatingFileHandler):
    def close(self):
        self.flush()
        super(ClosingTimeRotatingFileHandler, self).close()

def setup_logging(name, log_dir='/var/log/playground', log_file='app',
                  propagate=True, trace=True, level='DEBUG'):
    """ Creates a new logger or updates existing logger with
    log location from settings and formatting from const file.
    Creates log dir structure if it doesn't exist
    :param name: str() the name of the logger to set. __name__
    :param log_dir: list() or str(). Sub dir to save logs into
    :param log_file: str() name the log file
    :param propagate: Bool. If false a new hierarchy is created. If true
    existing logging configs will be used.
    :param trace: print logs to your console. Defaults to true when
    in debug mode.
    :return: None
    """
    # get or create the logger by name
    # set log save location
    # set the format
    log           = logging.getLogger(name)
    log.propagate = propagate
    formatter     = logging.Formatter(LOGGING_FORMAT)
    # construct the log file location
    log_file = set_log_file(log_dir, log_file, '.log')

    # creates a new log file handler
    hdlr = ClosingTimeRotatingFileHandler(log_file,
                                          when='midnight',
                                          backupCount=5)
    hdlr.setFormatter(formatter)

    # add the file handler and format to logger if it doesn't exist
    # in the logging hierarchy
    if hdlr.stream.name not in [x.stream.name for x in log.handlers if x
                                and hasattr(x, 'stream')]:
        log.addHandler(hdlr)
    # creates a new log stream handler to the console
    # defaults to console printing when in debug
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    if trace:
        if ch.__class__ not in map(type, log.handlers):
            log.addHandler(ch)
    # set logging level specified from current running config
    log.setLevel(level)


def set_log_file(log_dir, log_file, ext):
    """ Set path where we'll put the log or json files
    If the path doesn't yet exist, create it
    :param log_dir: list() or str(). Sub dir to save logs into
    :param log_file: str() name the log file
    :param ext: log file extension.
    :return: log file save path
    """
    log_dir = "/".join(log_dir) if type(log_dir) in (list, tuple) else log_dir
    log_path = os.path.abspath(log_dir)
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    if not log_file.endswith('%s' % ext):
        log_file = '{0}/{1}{2}'.format(log_path, log_file, ext)
    else:
        log_file = '{0}/{1}'.format(log_path, log_file)
    return log_file

setup_logging('app')