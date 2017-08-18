import os

# HTTP-Server
SERVER_PORT = 8000
SERVER_DEFAULT_TEMPLATE = '/choose'

# PRINTER
PRINTER_TIMEOUT = 10  # in seconds
PRINTER_HOST = '172.22.26.67'
PRINTER_PORT = 9100

# error logging
SENTRY_DSN = None

# try to overwrite default vars with the local config file
try:
    from labelprinterServeConf_local import *
except ImportError:
    pass

# loop over all local vars and overwrite with found environ vars
for name in vars().keys():
    if name.isupper() and name in os.environ:
        try:
            locals()[name] = int(os.environ[name])
        except ValueError:
            locals()[name] = os.environ[name]
