from agent.models import users, Uploader, Images
from agent import app, db, bcrypt, APP_ROOT,destination, mail, login_manager
from flask import render_template,flash,redirect, url_for, request, send_file
from agent.forms import RegistrationForm, LoginForm, UploadForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug import secure_filename
from flask_wtf.file import FileAllowed
from flask_mail import Message
import os
import secrets
from PIL import Image



@app.route('/')
def index():
    return render_template('index.html') 

@login_required
@app.route('/admin/')
def admin_login():
    if not current_user.is_authenticated():
        return redirect('/login/')
        
@app.route('/about')
@login_required
def about():
    return render_template('about.html')

def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/photos', image_fn)
    output_size = (500, 500)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path) 
    return image_fn



@app.route('/home', methods = ['GET'])
@login_required
def home():
    form = UploadForm()
    session = db.session()
    result = session.query(Uploader).all()
    img = session.query(Images).all()
    #house = upload.query.get(6)
    #plot = house.plotname
    #images = url_for('static',filename = 'photos/'+result.images)
    return render_template('home.html',result = result, img = img, form = form)
    #pics = os.listdir(destination)
    #return render_template('home.html',pics=pics)

@app.route('/details', methods = ['GET'])
@login_required
def houseDetails():
    house_id = request.args.get('house_id',None)
    detail = Uploader.query.filter_by(id = house_id)
    return render_template('details.html', detail = detail)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = users(firstName = form.firstName.data, lastName = form.lastName.data,
                             email = form.email.data, phoneNumber = form.phoneNumber.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created for you please login!!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

@app.route('/login',methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = users.query.filter_by(email = form.email.data).first()
        if user is None:
            flash('The user does not exist!! register first', 'danger')
        elif user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember= form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('wrong password!', 'danger')
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
#@login_required
def profile():
    return render_template('profile.html')

@app.route('/update', methods = ['GET', 'POST'])
@login_required
def update():
    session = db.session()
    form = UploadForm()
    if form.validate_on_submit():
        if form.image.data:
            photo = save_image(form.image.data)
            plot = Uploader(category = form.category.data, plotname = form.plotname.data,
                                estate = form.estate.data, roomNumber = form.roomNumber.data,
                                 price = form.price.data,
                                description = form.description.data, image = photo)
            db.session.add(plot)
            db.session.commit()
        """ u = Uploader.query.all()
        upload = str(u[-1].id)
        p = form.image.data
        for pic in p:
            photo = save_image(p)
            foto = Images(image = photo, uploader_id = upload)
            db.session.add(foto)
            db.session.commit() """
        flash('data added successifilly', 'success')
        return redirect(url_for('update'))
    return render_template('upload.html', form = form)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Reset password request', sender='josehmahugu@gmail.com', recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link
{url_for('reset_token', token = token, _external = True)}
If you did nor request this email ignore and no changes will be made
'''
    mail.send(msg)

@app.route('/reset_password', methods = ['GET', 'POST'])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = users.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('A reset email has been sent to your email address', 'info')
        return redirect(url_for('login'))
    return render_template('request_reset.html', form = form)

@app.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = users.verify_reset_token(token)
    if user is None:
        flash('The token is invalid or has expired','warning')
        return redirect(url_for('request_reset'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been reset', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', form = form)