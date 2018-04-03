import os
from pathlib import Path
from threading import Thread
import cv2
import picamera
from picamera.array import PiRGBArray


class PiCamera(Thread):
    def __init__(self, objects, resolution=(640, 480), framerate=32):
        Thread.__init__(self)
        # initialize the camera and stream
        self.status = objects.get('status')
        self.agent = objects.get('agent')
        self.resolution = resolution
        self.framerate = framerate
        self.camera = None
        self.rawCapture = None
        self.stream = None
        self.initialize_sensor()
        # initialize the frame
        self.frame = None
        self.img_name = ''

    def initialize_sensor(self):
        if self.camera is not None:
            self.__close()
        self.camera = picamera.PiCamera()
        self.camera.resolution = self.resolution
        self.camera.framerate = self.framerate
        self.rawCapture = PiRGBArray(self.camera, size=self.resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
                                                     format="bgr", use_video_port=True)

    def read(self):
            # return the frame most recently read
            return self.img_name

    def run(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            if self.status.is_recording:
                i = 1
                dirpath = str(Path(os.path.abspath(os.path.dirname(__file__))).parent)
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

            self.rawCapture.truncate(0)

    def __close(self):
        self.stream.close()
        self.rawCapture.close()
        self.camera.close()
        self.status.stop_recording()
