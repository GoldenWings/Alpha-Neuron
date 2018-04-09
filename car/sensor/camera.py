import os
from pathlib import Path
from threading import Thread
import cv2
import picamera
from picamera.array import PiRGBArray, bytes_to_rgb
import io
import numpy as np
from PIL import Image


class PiCamera(Thread):
    def __init__(self, objects, resolution=(160, 120), framerate=20):
        Thread.__init__(self)
        # initialize the camera and stream
        self.status = objects.get('status')
        self.agent = objects.get('driving_nn')
        self.resolution = resolution
        self.framerate = framerate
        self.camera = None
        self.rawCapture = None
        self.continuous_stream = None
        self.stream = None
        self.initialize_sensor()
        # initialize the frame
        self.frame = None
        self.img_name = ''
        self.byte_frame = None

    def initialize_sensor(self):
        if self.camera is not None:
            self.__close()
        self.camera = picamera.PiCamera()
        self.camera.resolution = self.resolution
        self.camera.framerate = self.framerate
        self.rawCapture = PiRGBArray(self.camera, size=self.resolution)
        self.stream = io.BytesIO()
        self.continuous_stream = self.camera.capture_continuous(self.stream,
                                                     format="jpeg", use_video_port=True)

    def read(self):
            # return the frame most recently read
            return self.img_name

    def run(self):
        # keep looping infinitely until the thread is stopped
        i = 0
        for f in self.continuous_stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.byte_frame = self.stream.getvalue()
            self.frame = np.array(Image.open(io.BytesIO(self.byte_frame)))
            #            self.frame = bytes_to_rgb(self.stream.getvalue(), self.camera.resolution)
            if self.status.is_recording:
                i = 1
                dirpath = str(Path(os.path.abspath(os.path.dirname(__file__))).parent.parent)
                filepath = dirpath + '/Training Data/Images/'
                while os.path.exists(filepath + 'image_' + "%s.jpg" % i):
                    i += 1
                self.img_name = filepath + 'image_' + "%s.jpg" % i
                cv2.imwrite(self.img_name, self.frame)
                # if the thread indicator variable is set, stop the thread
                # and resource camera resources
                if not self.status.sensor_started:
                    self.__close()
                    return
            elif self.status.is_agent and self.agent is not None:
                self.agent.put(self.frame)

            self.stream.seek(0)
            self.stream.truncate()
#            self.rawCapture.truncate(0)

    def __close(self):
        self.stream.close()
        self.rawCapture.close()
        self.camera.close()
        self.status.stop_recording()
