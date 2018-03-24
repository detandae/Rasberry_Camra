import sys
sys.path.append("/usr/local/lib/python3.5/dist-packages")
sys.path.append("/usr/lib/python3/dist-packages")
sys.path.append("/home/pi/.local/lib/python2.7/site-packages")
sys.path.append("/usr/local/lib/python2.7/dist-packages")

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
app.config.from_object(Config)
db = SQLAlchemy(app)



