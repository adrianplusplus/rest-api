# server/extensions.py

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_cache import Cache

bcrypt = Bcrypt()
cache = Cache()
db = SQLAlchemy()
cors = CORS()
