from os import environ
import local_config

# DB_CONN_STR = local_config.DB_CONN_STR_ATLAS
# APP_API_KEY = local_config.API_KEY_LOCAL

DB_CONN_STR = environ.get('DB_CONN_STR')
APP_API_KEY = environ.get('APP_API_KEY')