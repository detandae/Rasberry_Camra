import sys
sys.path.append("/usr/local/lib/python3.5/dist-packages")
sys.path.append("/usr/lib/python3/dist-packages")
sys.path.append("/home/pi/.local/lib/python2.7/site-packages")
sys.path.append("/usr/local/lib/python2.7/dist-packages")

from app import app
from Login import LoginForm
from Login import login
from register import register
from users import users
from pycamera_stream import CameraPage
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,threaded=True)








