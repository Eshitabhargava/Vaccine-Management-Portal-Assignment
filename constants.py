"""
Utils script containing commmon constants required across modules
"""
import os
import re

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
bcrypt = Bcrypt()
CWD = os.getcwd()
PROTECTED_PATH = "{}/app/preview/protected".format(CWD)
ADD_MODELS = "sed -ie 's/# from myapp import mymodel/from app.models import {}/g' migrations/env.py"
REQUEST_TIMEOUT = 120
LOG_CAPACITY = 100
BASE_HEADERS = {"access-control-allow-origin": "*"}
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")