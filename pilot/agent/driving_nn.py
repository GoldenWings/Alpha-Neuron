import queue
import threading
from utility.utility import *
import keras
from car.hardware.config import SERVO_EFFECTIVE_ANGLE
from car.trainer_config import *
from .model_architecture import build_model
import tensorflow as tf


class DrivingNeuralNetwork:
    def __init__(self, objects, model_path=None):
        self._car = objects.get('car')
        self._logger = objects.get('logger')
        if model_path:
            self._logger.log('Model path is given...')
            self.load(model_path)
        elif count_models() > 0:
            self._logger.log('No path for model provided, will load latest model...')
            model_path = "{}model_{}.h5".format(MODEL_PATH, count_models())
            self.load(model_path)
        else:
            self._logger.log('No models exist in pilot/models ! \n Building model...')
            self.model = build_model()
            self._logger.log('Building model completed successfully')
        self.graph = tf.get_default_graph()
        self.frame_queue = queue.LifoQueue()
        self.prediction_thread = threading.Thread(name="Prediction thread",
                                                  target=self.predict_from_queue,
                                                  args=())

    def load(self, model_path):
        self._logger.log('Loading model...')
        self.model = keras.models.load_model(model_path)
        self._logger.log('Model successfully loaded!')

    def put(self, frame):
        self.frame_queue.put(frame)

    def start(self):
        self.prediction_thread = threading.Thread(name="Prediction thread",
                                                  target=self.predict_from_queue,
                                                  args=())
        self.prediction_thread.start()

    def predict_from_queue(self):
        while self._car.status.is_agent:
            with self.graph.as_default():
                frame = self.frame_queue.get()
                img_arr = frame.reshape((1,) + frame.shape)
                binned_angle, throttle = self.model.predict(img_arr)
                unbinned_angle = linear_unbin(binned_angle)
                angle = denormalize(unbinned_angle, SERVO_EFFECTIVE_ANGLE[0], SERVO_EFFECTIVE_ANGLE[1])
                N = len(throttle[0])

                if N > 0:
                    throttle = linear_unbin(throttle, N=N, offset=0.0, R=1)
                else:
                    throttle = throttle[0][0]
                prediction = "Unbinned steering angle {} " \
                             " final angle {} throttle = {}".format(unbinned_angle, angle, throttle)
                self._car.set_angle(angle)
                self._car.set_throttle(throttle)
                self._logger.log(prediction)
                self.frame_queue.task_done()

    def train(self, train_gen, val_gen,
              saved_model_path, epochs=100, steps=100, train_split=0.8,
              verbose=1, min_delta=.0005, patience=5, use_early_stop=True):

        """
        train_gen: generator that yields an array of images an array of

        """
        print('Save Best')
        # checkpoint to save model after each epoch
        save_best = keras.callbacks.ModelCheckpoint(saved_model_path,
                                                    monitor='val_loss',
                                                    verbose=verbose,
                                                    save_best_only=True,
                                                    mode='min')
        print('Save best finish')
        # stop training if the validation error stops improving.
        early_stop = keras.callbacks.EarlyStopping(monitor='val_loss',
                                                   min_delta=min_delta,
                                                   patience=patience,
                                                   verbose=verbose,
                                                   mode='auto')
        print('early stop finish')
        callbacks_list = [save_best]

        if use_early_stop:
            callbacks_list.append(early_stop)
        print('start fitting')
        print(steps, train_split)
        val_steps = steps * (1.0 - train_split) / train_split
        print(val_steps)
        hist = self.model.fit_generator(
            train_gen,
            steps_per_epoch=steps,
            epochs=epochs,
            verbose=1,
            validation_data=val_gen,
            callbacks=callbacks_list,
            validation_steps=val_steps)
        print('finish fiting')
        return hist

    def obstacle_avoidance(self):
        pass
