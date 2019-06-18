from agent import db, login_manager, app, admin, bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
import cgi, cgitb
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, current_user
from sqlalchemy.ext.hybrid import hybrid_property
import os

#create instance of field storage


@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))



class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(20), unique = True, nullable = False)
    lastName = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    phoneNumber = db.Column(db.String(15), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return '<uploader %r>' %(self.id)

    def get_reset_token(self, expires_sec = 1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return users.query.get(user_id)


class Uploader(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(20), nullable = False)
    plotname = db.Column(db.String(20), nullable = False)
    estate = db.Column(db.String(20), nullable = False)
    roomNumber = db.Column(db.String(10), nullable = False)
    price = db.Column(db.DECIMAL(5,2), nullable = False)
    description = db.Column(db.String(300), nullable = False)
    image = db.Column(db.String, nullable = False, default = 'default.jpg')
    images = db.relationship('Images',backref='uploader', lazy=True)

    def __repr__(self):
        return '<Uploader %r>' %(self.id)

class Images(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.String, nullable = False, default = 'default.jpg')
    uploader_id = db.Column(db.Integer, db.ForeignKey('uploader.id'), nullable = False)

    def __repr__(self):
        return '<Images %r>' %(self.id)

class Staff(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(20), unique = True, nullable = False)
    lastName = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    phoneNumber = db.Column(db.String(15), unique = True, nullable = False)
    _password = db.Column(db.Binary)
    _salt = db.Column(db.Binary, default=os.urandom(512))

class MicroBlogModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated
        
        # redirect to login page if user doesn't have access
   

class staffview(ModelView):
    form_columns = ['firstName','lastName','email','phoneNumber','_password']

    def __repr__(self):
        return '<Staff %r>' %(self.id)

admin.add_view(MicroBlogModelView(users, db.session))
admin.add_view(MicroBlogModelView(Uploader, db.session))
admin.add_view(staffview(Staff, db.session))
admin.add_view(MicroBlogModelView(Images, db.session))