# todo add ping support
# todo
import web
import atexit
import sys
import os

from settings import LOG_DIR, LOG_FILE
from utils import get_app_directory, setup_logging, \
    init_db, init_secret_token
import api

# setup logging
_log_path = os.path.join(get_app_directory(), LOG_DIR, LOG_FILE)
setup_logging(_log_path)

# setup web.py urls
url_routing = (
    '/github_hook', api.hook,
    '/force_pushes_for_ref', api.force_pushes_for_ref,
    '/force_pushes_for_branch', api.force_pushes_for_branch
)

init_secret_token()

# init app
app = web.application(url_routing, globals())

def run_at_exit():
    """
    Runs at application exit. Clean up here.
    """
    app.stop()

atexit.register(run_at_exit)

if __name__ == '__main__':
    try:
        init_db()

        app.run()
    except KeyboardInterrupt:
        # exit neatly on keyboard interrupt
        print 'Interrupted'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
