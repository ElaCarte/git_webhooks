
# basename for logging file. When log files role details will be appended
# to the base name
LOG_FILE = 'output.log'
# name of directory to keep log files in, will be a sub direcotry in this
# directory
LOG_DIR = 'logs'

# name of db used to store force push events
DB_NAME = 'force_push_data.db'

USE_SECRET_TOKEN = False

# don't put a token here in case it gets committed, use init_secret_token
# to pull it from an os environmental var SECRET_TOKEN_ENV_VAR_NAME
SECRET_TOKEN = None

# name of the os env var to pull the secret token from
SECRET_TOKEN_ENV_VAR_NAME = 'GITHUB_HOOK_SECRET_TOKEN'
