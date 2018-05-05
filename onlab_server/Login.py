import sys
sys.path.append("/usr/local/lib/python3.5/dist-packages")
sys.path.append("/usr/lib/python3/dist-packages")
sys.path.append("/home/pi/.local/lib/python2.7/site-packages")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
from flask import request
from werkzeug.urls import url_parse
from flask import Flask,url_for
from flask import render_template
from flask import flash, redirect
from app import app
from app import db
from tables import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, current_user, login_required, logout_user,UserMixin
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

login = LoginManager(app)
login.login_view = 'login'
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
@app.route('/login', methods=['GET', 'POST'])
def login():
    """  if current_user.is_authenticated:
        return redirect(url_for('page'))"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('page')
        return redirect(next_page)
        
        
    return render_template('login.html', title='Sign In', form=form)


@app.route('/page', methods=['GET', 'POST'])
@login_required
def page():
    return render_template("page.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))






