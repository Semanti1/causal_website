# !/usr/bin/python3.7
import logging
import sys

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/causal_website_dev/')
from causal_website import app as application
from flask import Flask
from flask_session import Session
application.secret_key = 'secret'
application.config["SESSION_PERMANENT"]=False
application.config["SESSION_TYPE"]="filesystem"
application.config["SESSION_FILE_DIR"]='/var/www/causal_website_dev/flask_session'
Session(application)
