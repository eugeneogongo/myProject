from agent import db, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
import cgi, cgitb
from flask_admin.contrib.sqla import ModelView


#create instance of field storage


@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))



class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(20), unique = True, nullable = False)
    lastName = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(20), unique = True, nullable = False)
    phoneNumber = db.Column(db.String(15), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return f"user('{self.username}','{self.email}','{self.image_file}',)"

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


class uploader(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(20), nullable = False)
    plotname = db.Column(db.String(20), nullable = False)
    estate = db.Column(db.String(20), nullable = False)
    roomNumber = db.Column(db.String(10), nullable = False)
    price = db.Column(db.DECIMAL(5,2), nullable = False)
    images = db.Column(db.String, nullable = False, default = 'default.jpg')
    description = db.Column(db.String(300), nullable = False)

    def __repr__(self):
        return f"('{self.plotname}','{self.images}',)"