"""
General utils
"""

import os
import sqlite3
import sys
import logging
import logging.handlers

import settings


def setup_logging(log_path):
    """
    Setup logging to log to console and log file.
    :return:
    """
    # create dir if it does not exist
    log_dir = os.path.dirname(log_path)
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # setup log file
    one_MB = 1000000
    handler = logging.handlers.RotatingFileHandler(
        log_path, maxBytes=(one_MB * 20), backupCount=5
    )
    fmt = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    handler.setFormatter(fmt)
    root_logger.addHandler(handler)

    # setup logging to console
    # strm_hndlr = logging.StreamHandler(sys.stdout)
    # strm_hndlr.setFormatter(fmt)
    # root_logger.addHandler(strm_hndlr)

    # redirect stdout/err to log file
    StreamToLogger.setup_stdout()
    StreamToLogger.setup_stderr()


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, stream, logger, log_level=logging.INFO,
                 also_log_to_stream=False):
        """
        :param stream to redirect
        :param logger: logger to log to
        :param log_level: log level to log at
        :param also_log_to_stream: if true, log to logger and to stream
        """
        self.logger = logger
        self.stream = stream
        self.log_level = log_level
        self.linebuf = ''
        self.also_log_to_stream = also_log_to_stream

    @classmethod
    def setup_stdout(cls, also_log_to_stream=True):
        """
        Setup logger for stdout
        """
        stdout_logger = logging.getLogger('STDOUT')
        sl = StreamToLogger(
            sys.stdout, stdout_logger, logging.INFO, also_log_to_stream
        )
        sys.stdout = sl

    @classmethod
    def setup_stderr(cls, also_log_to_stream=True):
        """
        Setup logger for stdout
        """
        stderr_logger = logging.getLogger('STDERR')
        sl = StreamToLogger(
            sys.stderr, stderr_logger, logging.ERROR, also_log_to_stream
        )
        sys.stderr = sl

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
        self.stream.write(buf)


_app_dir = None

def get_app_directory():
    """
    Get the parent directory of this file. A bit hacky, but easy way to get
    the directory of this app as long as this file is in the root folder.

    sys.argv[0] will not be the right path if you use some other script to
    start this script, so this works adequetly for now
    """
    global _app_dir
    if not _app_dir:
        _app_dir = os.path.dirname(__file__)
    return _app_dir

_db_path = None


def get_db_path():
    global _db_path
    if not _db_path:
        _db_path = os.path.join(get_app_directory(), settings.DB_NAME)
    return _db_path


def init_db():
    """
    Create database and setup tables if they do not exist. Doesn't handle
    schema changes. If this schema needs to change, add some migration logic.
    """
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, repo_name TEXT, ref TEXT, event TEXT)''')
    conn.commit()
    conn.close()


def find_force_push_events_for_ref(ref_name):
    """
    Check db for any events with this git ref name.
    :return: list of dicts. Each dict is the json push event data
    """

    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT created_at, event from data WHERE ref=?', (ref_name,))
    results = c.fetchall()
    conn.close()
    return results


def init_secret_token():
    if settings.USE_SECRET_TOKEN:
        # pull github hook secret key from system env
        try:
            settings.SECRET_TOKEN = os.environ[
                settings.SECRET_TOKEN_ENV_VAR_NAME]
        except KeyError:
            print "Setup webhook secret as " \
                  "OS environmental variable {}".format(
                settings.SECRET_TOKEN_ENV_VAR_NAME)
            sys.exit(1)

