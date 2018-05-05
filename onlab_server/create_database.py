
import sys
sys.path.append("/usr/local/lib/python3.5/dist-packages")
sys.path.append("/usr/lib/python3/dist-packages")
sys.path.append("/home/pi/.local/lib/python2.7/site-packages")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
sys.path.append("/home/pi/Desktop/python/bejelentkezes")
from tables import User
from app import db


 
db.create_all()
u = User(username='admin', email='detariandras@gmail.com')
u.set_password('valami')
db.session.add(u)
u = User(username='laci', email='DjVajda@gmail.com')
u.set_password('laci')
db.session.add(u)
u = User(username='bela', email='john@example.com')
db.session.add(u)
u = User(username='viktor', email='viktor@example.com')
db.session.add(u)
db.session.commit()