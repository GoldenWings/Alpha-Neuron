import tensorflow as tf
import os
import queue
import threading
import cv2
from utility.data_util import get_prev_epoch
import numpy as np
from utility.data_prep import apply_transformations


class DrivingNeuralNetwork:
    def __init__(self, objects, checkpoint_dir_path=''):
        self.__car = objects.get('car')
        if checkpoint_dir_path is not '':
            start_epoch = get_prev_epoch(checkpoint_dir_path)
            graph_name = 'model-' + str(start_epoch)
            checkpoint_file_path = os.path.join(checkpoint_dir_path, graph_name)
            saver = tf.train.import_meta_graph(checkpoint_dir_path + "/" + graph_name + ".meta")
            self.sess = tf.Session()
            saver.restore(self.sess, checkpoint_file_path)
            graph = tf.get_default_graph()
            self.x = graph.get_tensor_by_name("x:0")
            make_logits = graph.get_operation_by_name("logits")
            logits = make_logits.outputs[0]
            # A tensor representing the model's prediction
            self.prediction = tf.argmax(logits, 1)

        self.frame_queue = queue.LifoQueue()
        self.prediction_thread = threading.Thread(name="Prediction thread",
                                                  target=self.predict_from_queue,
                                                  args=())

    def put(self, frame):
        self.frame_queue.put(frame)

    def start(self):
        self.prediction_thread.start()

    def predict_from_queue(self):
        while self.__car.status.is_agent:
            frame = self.frame_queue.get()
            flipped_image = cv2.flip(frame, 1)
            normalized_images = [frame, flipped_image]
            normalized_images = np.array(normalized_images)
            # Normalize for contrast and pixel size
            normalized_images = apply_transformations(normalized_images)
            command = self.prediction.eval(feed_dict={self.x: normalized_images}, session=self.sess)[0]
            if command is "right":
                self.__car.turn_right()
            elif command is "left":
                self.__car.turn_left()
            elif command is "up":
                self.__car.move_forward()
            self.frame_queue.task_done()

    def obstacle_avoidance(self):
        pass
