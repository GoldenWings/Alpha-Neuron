import io
from threading import Thread

import numpy as np
import picamera
from PIL import Image
from picamera.array import PiRGBArray


class PiCamera(Thread):
    def __init__(self, objects, resolution=(160, 120), framerate=20):
        Thread.__init__(self)
        # initialize the camera and stream
        self.status = objects.get('status')
        self.agent = objects.get('driving_nn')
        self.barrel_writer = objects.get('barrel')
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
        """
        this method is responsible for initialize the camera sensor using Picamera class
        :return: it has no return type
        """
        if self.camera is not None:
            self._close()
        self.camera = picamera.PiCamera()
        self.camera.resolution = self.resolution
        self.camera.framerate = self.framerate
        self.rawCapture = PiRGBArray(self.camera, size=self.resolution)
        self.stream = io.BytesIO()
        self.continuous_stream = self.camera.capture_continuous(self.stream,
                                                     format="jpeg", use_video_port=True)

    def read(self):
        """
        return the frame most recently read
        :return: img_name
        """
        return self.img_name

    def run(self):
        """this method get image frame from camera and save it using barrel_writer"""
        # keep looping infinitely until the thread is stopped
        i = 0
        for f in self.continuous_stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.byte_frame = self.stream.getvalue()
            self.frame = np.array(Image.open(io.BytesIO(self.byte_frame)))
            if self.status.is_recording:
                self.barrel_writer.put(self.frame)
            if not self.status.sensor_started:
                self._close()
                return
            elif self.status.is_agent and self.agent is not None:
                self.agent.put(self.frame)

            self.stream.seek(0)
            self.stream.truncate()
#            self.rawCapture.truncate(0)

    def _close(self):
        """this method close all on going stream and will destroy the camera obj to avoid resources conflict"""
        self.stream.close()
        self.rawCapture.close()
        self.camera.close()
        self.status.stop_recording()