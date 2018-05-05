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
from wtforms.validators import InputRequired, Email
from wtforms.fields.html5 import EmailField  
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, current_user, login_required, logout_user,UserMixin

class RegisterForm(FlaskForm):
    username = StringField("Name", validators=[InputRequired('Please enter your name.')])
    #username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = EmailField("Email",  validators=[InputRequired("Please enter your email address."), Email("Please enter your email address.")])
#  email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Add User')

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegisterForm()
    if form.validate_on_submit(): 
        if len(form.username.data)>4 and len(form.password.data)>8 and '@' in form.email.data :    
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Register Succsesfull')
            return redirect(url_for('register'))
        else:
            flash('Something went wrong! :( ')
            
        
        
    return render_template('register.html', form=form)
    
    
    
    