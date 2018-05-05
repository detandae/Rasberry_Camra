import sys
sys.path.append("/usr/local/lib/python3.5/dist-packages")
sys.path.append("/usr/lib/python3/dist-packages")

import time
import threading
from _thread import get_ident
import io
import picamera
import numpy as np
import cv2
from picamera.array import PiRGBArray
from DetectMotion import MotionDetection
class CameraEvent(object):
    """An Event-like class that signals all active clients when a new frame is
    available.
    """
    def __init__(self):
        self.events = {}

    def wait(self):
        """Invoked from each client's thread to wait for the next frame."""
        ident = get_ident()
        if ident not in self.events.keys():
            # this is a new client
            # add an entry for it in the self.events dict
            # each entry has two elements, a threading.Event() and a timestamp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """Invoked by the camera thread when a new frame is available."""
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                # if this client's event is not set, then set it
                # also update the last set timestamp to now
                event[0].set()
                event[1] = now
            else:
                # if the client's event is already set, it means the client
                # did not process a previous frame
                # if the event stays set for more than 5 seconds, then assume
                # the client is gone and remove it
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """Invoked from each client's thread after a frame was processed."""
        self.events[get_ident()][0].clear()


class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    event = CameraEvent()

    def __init__(self):
        """Start the background camera thread if it isn't running yet."""
        if Camera.thread is None:
            Camera.last_access = time.time()

            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames are available
            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        """Return the current camera frame."""
        Camera.last_access = time.time()

        # wait for a signal from the camera thread
        Camera.event.wait()
        Camera.event.clear()

        return Camera.frame

   
    @staticmethod
    def frames():
        try:
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            video=cv2.VideoWriter('frame.avi',fourcc,9,(720,480))
            with picamera.PiCamera() as camera:
                camera.resolution = (720,480)
                camera.framerate=40
                rawCapture = PiRGBArray(camera, size=(720,480))
                time.sleep(2)
                MovDetection=MotionDetection()
                MovDetection.UpdateUsers()
                stream = io.BytesIO()
                
                for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

                    MovDetection.setFrame(f.array)
                    MovDetection.setTime()
                    currentframe,detect=MovDetection.detect()
                    if detect:
                        video.write(currentframe)
                    currentframe=cv2.imencode('.jpg', currentframe)[1].tobytes()
                    yield currentframe
                
                
                    rawCapture.truncate(0)
        finally:
            video.release()
        '''
        with picamera.PiCamera() as camera:

            # let camera warm up
            time.sleep(2)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()'''
    @classmethod
    def _thread(cls):
        """Camera background thread."""
        print('Starting camera thread.')
        frames_iterator = cls.frames()
        for frame in frames_iterator:
            Camera.frame = frame
            Camera.event.set()  # send signal to clients
            time.sleep(0)

            # if there hasn't been any clients asking for frames in
            # the last 10 seconds then stop the thread
            '''if time.time() - Camera.last_access > 10:
                frames_iterator.close()
                print('Stopping camera thread due to inactivity.')
                break'''
        Camera.thread = None