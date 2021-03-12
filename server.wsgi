# !/usr/bin/python3.7
import logging
import sys

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/causal_website/')
from causal_website import app as application
application.secret_key = 'secret'
