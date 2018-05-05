import sys
sys.path.append("/usr/local/lib/python3.5/dist-packages")
sys.path.append("/usr/lib/python3/dist-packages")
sys.path.append("/home/pi/.local/lib/python2.7/site-packages")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
from werkzeug.urls import url_parse
from flask import Flask,url_for
from tables import User
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired
from app import db
from app import app
from flask_login import LoginManager, login_user, current_user, login_required, logout_user,UserMixin
from flask import flash, redirect
from flask import render_template

def create_form_class(number):
    form_fields = {}
    for i in range(number):
        field_id = 'submit'+str(i)
        form_fields[field_id] = SubmitField("Delete")
    return type('MySubmitForm', (FlaskForm,), form_fields)
number=db.session.query(User).count()
MySubmitForm=create_form_class(number)



list=[]
@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    if int(current_user.id) is 10:
        flash('You are not admin!')
        return redirect(url_for('page'))
    form=MySubmitForm()
    users=User.query.all()
    print(users)
    list.clear()
    for i,u in zip(range(number),users):
        list.append([u,i])
    print(list)    
    if form.validate_on_submit():
        for subfield,i in zip(form,range(number)):
            if subfield.data:
                     print(i)
                     print(list[i][1])
                     print(list[i][0])
                     db.session.delete(list[i][0])
                     db.session.commit()
                     del list[i]
                     flash('ID %d deleted'%(i+1))
                     return redirect(url_for('users'))
   
    return render_template('users.html',number=number,users=users,form=form)
