import queue
import threading

import keras

from .model_architecture import build_model


class DrivingNeuralNetwork:
    def __init__(self, objects, model=None):
        self._car = objects.get('car')
        self._logger = objects.get('logger')
        self.model = model
        if model:
            self.model = model
        else:
            self.model = build_model()
        self.frame_queue = queue.LifoQueue()
        self.prediction_thread = threading.Thread(name="Prediction thread",
                                                  target=self.predict_from_queue,
                                                  args=())

    def load(self, model_path):
        self.model = keras.models.load_model(model_path)

    def put(self, frame):
        self.frame_queue.put(frame)

    def start(self):
        self.prediction_thread = threading.Thread(name="Prediction thread",
                                                      target=self.predict_from_queue,
                                                      args=())
        self.prediction_thread.start()

    def predict_from_queue(self):
        while self._car.status.is_agent:
            frame = self.frame_queue.get()
            img_arr = frame.reshape((1,) + frame.shape)
            angle, throttle = self.model.predict(img_arr)
            prediction = "steering angle = {} throttle = {}".format(angle, throttle)
            self._logger.log(prediction)
            self.frame_queue.task_done()

    def train(self, train_gen, val_gen,
              saved_model_path, epochs=100, steps=100, train_split=0.8,
              verbose=1, min_delta=.0005, patience=5, use_early_stop=True):

        """
        train_gen: generator that yields an array of images an array of

        """

        # checkpoint to save model after each epoch
        save_best = keras.callbacks.ModelCheckpoint(saved_model_path,
                                                    monitor='val_loss',
                                                    verbose=verbose,
                                                    save_best_only=True,
                                                    mode='min')

        # stop training if the validation error stops improving.
        early_stop = keras.callbacks.EarlyStopping(monitor='val_loss',
                                                   min_delta=min_delta,
                                                   patience=patience,
                                                   verbose=verbose,
                                                   mode='auto')

        callbacks_list = [save_best]

        if use_early_stop:
            callbacks_list.append(early_stop)

        hist = self.model.fit_generator(
            train_gen,
            steps_per_epoch=steps,
            epochs=epochs,
            verbose=1,
            validation_data=val_gen,
            callbacks=callbacks_list,
            validation_steps=steps * (1.0 - train_split) / train_split)
        return hist

    def obstacle_avoidance(self):
        pass
