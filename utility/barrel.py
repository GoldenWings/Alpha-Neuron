from .singleton import Singleton
import csv
from .barrel_config import *
import cv2
import pandas as pd
from PIL import Image
import numpy as np


class BarrelWriter(metaclass=Singleton):
        def __init__(self, objects, current_session=False):
            """
            :param objects: contains all objects required for the class
            :param current_session: weather or not to save on the latest csv (Current session is the latest csv)
            """
            self.servo = objects.get('servo')
            self.motor = objects.get('motor')
            self.frame = None
            self.current_session = current_session
            self.csv_name = None

        def put_frame(self, frame):
            self.frame = frame

        def get_csv(self):
            """
            First check if its suppose to make new session or there is no csv files.
            If its set to not to store on the current session then make new csv and set the current session to true
                so next reading appended to the current csv.
            If there is no csv then make new csv
            if its suppose to store on the current session and there exist a csv then good to store.
            if its suppose to store on the current session but somehow no file then make new csv.
            """
            csv_number = count_datasets()
            if not self.current_session or csv_number == 0:
                self.make_csv()
                self.current_session = True
            elif self.current_session:
                self.csv_name = 'session' + str(csv_number) + '.csv'
                if os.path.isfile(os.path.join(DATA_PATH, self.csv_name)):
                    return
                self.make_csv()

        def get_record(self):
            """
            :return: a dictionary that represents a record of the input and outputs
            """
            angle = self.motor.throttle
            throttle = self.servo.angle
            img = self.frame
            img_name = self.save_image(img)
            record = {'angle': angle, 'throttle': throttle, 'image': img_name}
            return record

        def make_csv(self):
            """
            makes a new csv with a new name of csv_(number of csvs + 1)
            then write the header for the csv which are the keys for the record dict (angle, throttle, image)
            then write the content of dictionary
            """
            csv_number = count_datasets() + 1
            self.csv_name = 'session_' + str(csv_number) + '.csv'
            record = self.get_record()
            with open(self.csv_name, 'a') as f:
                w = csv.DictWriter(f, record.keys())
                w.writeheader()
                w.writerow(record)

        def write_csv(self):
            """
            is the starting point of the BarrelWriter class.
            first check if there exist a csv_name (Ready to start writing)
            or append to the latest csv.
            """
            if self.csv_name is None:
                self.get_csv()
            else:
                record = self.get_record()
                with open(self.csv_name, 'a') as f:
                    w = csv.DictWriter(f, record.keys())
                    w.writerow(record)

        # noinspection PyMethodMayBeStatic
        def save_image(self, img):
            """
            :param img: image to be stored
            :return: full name of the image
            """
            img_number = count_images() + 1
            # for testing store throttle and angle in image name for better visualization
            angle = self.servo.angle
            throttle = self.servo.throttle
            full_name = "img_%d_ttl_%.3f_agl_%.1f%s" % (img_number, throttle, angle, ".jpg")
            # next line for production
            # full_name = IMAGE_PATH + '/img_' + str(img_number) + '.jpg'
            cv2.imwrite(full_name, img)
            return full_name


class BarrelReader(metaclass=Singleton):
    def __init__(self, barrel_name=None):
        self.latest = True if not barrel_name else False
        self.barrel_name = barrel_name
        self.df = None

    # noinspection PyMethodMayBeStatic
    def get_image(self, img_path):
        img = Image.open(img_path)
        img_arr = np.array(img)
        return img_arr

    def get_record(self, record_dict):
        record = {}
        for key, value in record_dict.items():
            if key is 'image':
                value = self.get_image(value)
            record[value] = key
        return record

    def get_csv(self):
        if self.latest:
            latest_number = count_datasets() + 1
            barrel_full_name = DATA_PATH + '/' + str(latest_number) + '.csv'
            return barrel_full_name
        if os.path.isfile(os.path.join(DATA_PATH, self.barrel_name + '.csv')):
            return DATA_PATH + '/' + self.barrel_name + '.csv'
        raise FileNotFoundError("Barrel path incorrect")

    def load_df(self):
        self.df = pd.read_csv(self.get_csv())

    def generate_record(self, df=None):
        if not df:
            df = self.df
        while True:
            for _ in df.iterrows():
                record_dict = df.sample(n=1).to_dict(orient='record')[0]

                record_dict = self.get_record(record_dict)
                yield record_dict

    def change_barrel(self, name):
        self.barrel_name = name

    def generate_batch(self, batch_size=128, df=None):
        records = self.generate_record(df)
        keys = list(self.df.columns)

        while True:
            record_list = []

            for _ in range(batch_size):
                record_list.append(next(records))
            batch_arrays = {}

            for i, k in enumerate(keys):
                arr = np.array([r[k] for r in record_list])
                batch_arrays[k] = arr

            yield batch_arrays

    def generate_training(self, X_keys, Y_keys, batch_size=128, df=None):
        batches = self.generate_batch(batch_size=batch_size, df=df)
        while True:
            batch = next(batches)
            X = [batch[k] for k in X_keys]
            Y = [batch[k] for k in Y_keys]
            yield X, Y

    def generate_training_validation(self, batch_size=128, train_frac=.8):
        self.load_df()
        X_keys = ['image']
        Y_keys = ['angle', 'throttle']
        train_df  = self.df.sample(frac=train_frac, random_state=200)
        val_df = self.df.drop(train_df.index)

        train_gen = self.generate_training(X_keys=X_keys, Y_keys=Y_keys, batch_size=batch_size, df=train_df)

        val_gen = self.generate_training(X_keys=X_keys, Y_keys=Y_keys, batch_size=batch_size, df=val_df)

        return train_gen, val_gen
