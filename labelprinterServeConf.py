import os
import logging

# HTTP-Server
SERVER_ADDRESS = '::'
SERVER_PORT = 8000
SERVER_DEFAULT_TEMPLATE = '/choose'

# PRINTER
PRINTER_TIMEOUT = 10  # in seconds
PRINTER_HOST = '172.22.26.67'
PRINTER_PORT = 9100

# error logging
SENTRY_DSN = None
DEBUG_LOG_LEVEL = logging.ERROR

# try to overwrite default vars with the local config file
try:
    from labelprinterServeConf_local import *
except ImportError:
    pass

# loop over all local vars and overwrite with found environ vars
for name in list(vars().keys()):
    if name.isupper() and name in os.environ:
        try:
            locals()[name] = int(os.environ[name])
        except ValueError:
            locals()[name] = os.environ[name]

# get SENTRY_DSN from a secret (if it exists)
if os.path.exists("/run/secrets/SENTRY_DSN"):
    SENTRY_DSN = open("/run/secrets/SENTRY_DSN").read().strip()

logging.basicConfig(level=DEBUG_LOG_LEVEL)
