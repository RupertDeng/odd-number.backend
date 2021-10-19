from os import environ
import local_config

# local keys for development
# DB_CONN_STR = local_config.DB_CONN_STR_ATLAS
DB_CONN_STR = local_config.DB_CONN_STR_LOCAL
APP_API_KEY = local_config.API_KEY_LOCAL
FE_STR = local_config.FE_STR_LOCAL

# remote keys from backend server environment variables
# DB_CONN_STR = environ.get('DB_CONN_STR')
# APP_API_KEY = environ.get('APP_API_KEY')
# FE_STR = environ.get('FE_STR')