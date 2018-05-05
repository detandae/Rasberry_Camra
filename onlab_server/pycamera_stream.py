import sys
sys.path.append("/usr/local/lib/python3.5/dist-packages")
sys.path.append("/usr/lib/python3/dist-packages")
sys.path.append("/home/pi/Desktop/python/webapp6")

from importlib import import_module
import os
from flask import Flask, render_template, Response
from werkzeug.urls import url_parse
from flask import Flask,url_for
from tables import User
from flask_wtf import FlaskForm
from app import db
from app import app
from flask_login import LoginManager, login_user, current_user, login_required, logout_user,UserMixin
from flask import flash, redirect
from flask import render_template
# import camera driver
"""
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera
"""
# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera



cam=Camera()

@app.route('/SecurityCamera')
@login_required
def CameraPage():
    """Video streaming home page."""
    return render_template('camera.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
@login_required
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(cam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


