
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from werkzeug.utils import secure_filename
import os
from flask_admin import Admin
from flask_mail import Mail
from flask_googlemaps import GoogleMaps 

app = Flask(__name__)

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "8JZ7i18MjFuM35dJHq70n3Hx4"

# Initialize the extension
googleMaps = GoogleMaps(app)
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='Master Agent', template_mode='bootstrap3')
# Add administrative views here

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
destination = os.path.join(APP_ROOT, 'static/photos/')

app.config['SECRET_KEY'] = 'cb60c2ec45f896e9429cdb525cccdfbb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'josehmahugu@gmail.com'
app.config['MAIL_PASSWORD'] = 'josey7022'


mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from agent import routes