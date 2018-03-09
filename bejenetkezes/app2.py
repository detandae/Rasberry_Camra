import sys
sys.path.append("/usr/local/lib/python3.5/dist-packages")
sys.path.append("/usr/lib/python3/dist-packages")
sys.path.append("/home/pi/.local/lib/python2.7/site-packages")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
from flask import Flask
from flask import session
from flask_session import Session
from flask import render_template
from flask import flash, redirect
from flask import request
from random import randint
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import redis
#from flask_login import LoginManager, login_user, current_user, login_required, logout_user,UserMixin

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class User:
    def __init__(self,ip,id):
        self.ip=ip
        self.id=id
        self.enabled=False
    def enable(self):
        self.enabled=True
    def disable(self):
        self.enabled=False


list=[]
app = Flask(__name__)
file = open('secretkey.txt', 'r')
app.config['SECRET_KEY'] =file.readline()
file.close()
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url('localhost:5000')
app.config.from_object(__name__)
#sess = Session()
#sess.init_app(app)
print(app.config['SECRET_KEY']) 



@app.route('/')
def index():
    return 'Hello world'
@app.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        ip=request.remote_addr
        list.append(User(ip,randint(0,1000000000)))
        flash('Login requested for user {}, remember_me={}'.format(
          ip, form.remember_me.data))

            
        if form.username.data== 'admin' and form.password.data=='jelszo1222':
            list[-1].enable()
            return redirect('/page')
        
      
    return render_template('login.html', title='Sign In', form=form)
@app.route('/page', methods=['GET', 'POST'])
def page():
        ip=request.remote_addr
        for x in list:
            if x.ip==ip and x.enabled==True:
               return render_template("page.html")
        return redirect('/')
       
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,threaded=True)
