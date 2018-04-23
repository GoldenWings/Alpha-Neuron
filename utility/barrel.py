import csv
import threading
from queue import Queue
from pathlib import Path
import cv2
import pandas as pd
from PIL import Image
import shutil
from .barrel_config import *
from .utility import *
from .singleton import Singleton


# noinspection PyTypeChecker

class BarrelWriter(metaclass=Singleton):
        def __init__(self, objects):
            """
            :param objects: contains all objects required for the class
            """
            self.status = objects.get('status')
            self.logger = objects.get('logger')
            self._start_saving = threading.Thread(name="Start saving image ",
                                                  target=self.save_images,
                                                  args=())
            self.file_path = DATA_PATH
            self.csv_name = None
            self.frames_to_save = Queue()

        # noinspection PyMethodMayBeStatic
        def get_record(self, throttle, angle, img_name):
            """
            :return: return a dictionary that represents a record of the input and outputs
            """

            record = {'angle': angle, 'throttle': throttle, 'image': img_name}
            return record

        def save_csv(self, start_time):
            """
            makes a new csv with a unique name of session_( timestamp of now).csv
            then write the header for the csv which are the keys for the record dict (angle, throttle, image)
            then for each image split its name and write the content of the name to a dictionary
            then write it to record
            """
            self.logger.log('Entered save_csv')
            start_time = datetime.strptime(start_time,  '%Y-%m-%d %H:%M:%S.%f')
            timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M')
            self.csv_name = 'session_' + timestamp + '.csv'
            self.logger.log('csv name {}'.format(self.csv_name))
            headers = {'angle', 'throttle', 'image'}
            with open(self.file_path + self.csv_name, 'a') as f:
                w = csv.DictWriter(f, headers)
                w.writeheader()
                IMAGE_PATH = self.file_path + 'Images/'
                image_files = os.listdir(IMAGE_PATH)
                counter = 0
                for name in image_files:
                    counter += 1
                    if os.path.isfile(os.path.join(IMAGE_PATH, name)):
                        if os.path.splitext(name)[1] == '.jpg':
                            full_name = name.split('_')
                            full_date = name.split(' ')
                            date = full_date[0].split('_')[1]
                            time = full_date[1].split('_')[0]
                            image_date = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S.%f')
                            throttle = full_name[3]
                            angle = full_name[5].split('.')[0]
                            record = self.get_record(throttle, angle, name)
                            if image_date >= start_time:
                                w.writerow(record)
                                self.logger.log('Processing image number {} of {}. '.format(str(counter),
                                                                                            str(len(image_files))))
                self.logger.log('Session has been done with all images!. ')
            self.logger.log('Session has been saved successfully!. ')

        # noinspection PyMethodMayBeStatic
        def abort_csv(self):
            """
            loop through all files ing IMG_PATH/ , check if its a file or direction
            if file split the date then compare date if it fall between the interval then remove image
            :return:
            """
            self.logger.log("removing {}".format(self.file_path))
            shutil.rmtree(self.file_path, ignore_errors=True)
            self.logger.log("The session has been aborted successfully")

        def start_saving(self):
            self._start_saving = threading.Thread(name="Start saving image ",
                                                  target=self.save_images,
                                                  args=())
            self._start_saving.start()

        def make_session_dir(self):
            count = sum(os.path.isdir('{}/{}'.format(DATA_PATH, i)) for i in os.listdir(DATA_PATH))
            self.file_path = '{}session_{}/'.format(DATA_PATH, str(count))
            Path(self.file_path).mkdir(exist_ok=True)
            Path(self.file_path + 'Images').mkdir(exist_ok=True)

        # noinspection PyMethodMayBeStatic
        def save_images(self):
            while self.status.is_recording:
                try:
                    frame_state = self.frames_to_save.get()
                    img = frame_state['img']
                    angle = frame_state['angle']
                    throttle = frame_state['throttle']
                    timestamp = frame_state['timestamp']
                    img_name = "img_%s_ttl_%.3f_agl_%.1f%s" % (timestamp, throttle, angle, ".jpg")
                    IMAGE_PATH = self.file_path + 'Images/'
                    full_name = os.path.expanduser(IMAGE_PATH + img_name)
                    cv2.imwrite(full_name, img)
                    self.frames_to_save.task_done()
                except Exception as e:
                    pass

        def put(self, image_frame):
            self.frames_to_save.put(image_frame)


class BarrelReader(metaclass=Singleton):
    def __init__(self, barrel_name=None):
        """
        Latest :  indicator if should use latest barrel (csv) or not
        df : pandas dataframe
        :param barrel_name: csv file name
        """
        self.latest = True if not barrel_name else False
        self.barrel_name = barrel_name
        self.file_path = None
        self.df = None

    # noinspection PyMethodMayBeStatic
    def get_image(self, img_path):
        image_path = self.file_path + 'Images/'
        img = Image.open(image_path + img_path)
        img_arr = np.array(img)
        return img_arr

    def get_record(self, record_dict):
        """
        Returns a record with image instead of image path
        :param record_dict:
        :return:
        """
        record = {}
        for key, value in record_dict.items():
            if key == 'image':
                value = self.get_image(value)
            record[key] = value
        return record

    def get_csv(self):
        """
        If it asks for latest barrel then get it
        else custom barrel_name provided (from _init_ parameter) then load it, raise exception if file not exist
        :return:
        """
        if self.latest:
            count = sum(os.path.isdir(i) for i in os.listdir(DATA_PATH))
            self.file_path = '{}session_{}/'.format(DATA_PATH, str(count))
            latest_csv_name = get_latest_csv(self.file_path)
            barrel_full_name = self.file_path + str(latest_csv_name)
            return barrel_full_name
        if os.path.isfile(os.path.join(DATA_PATH, self.barrel_name)):
            return DATA_PATH + self.barrel_name
        raise FileNotFoundError("Barrel path incorrect")

    def load_df(self):
        """
        Convert csv to pandas
        :return:
        """
        self.df = pd.read_csv(self.get_csv())

    def generate_record(self, df=None):
        """
        read csv records (with images instead of path) and shuffle it
        :param df: dataframe to use to extract records
        :return:
        """
        if df is None:
            df = self.df
        while True:
            for _ in df.iterrows():
                record_dict = df.sample(n=1).to_dict(orient='record')[0]
                normalized_angle = normalize(record_dict['angle'], -1, 1,
                                             SERVO_EFFECTIVE_ANGLE[0], SERVO_EFFECTIVE_ANGLE[1])
                record_dict['angle'] = linear_bin(normalized_angle)
                record_dict['throttle'] = linear_bin(record_dict['throttle'], N=4, offset=0, R=1)
                record_dict = self.get_record(record_dict)
                yield record_dict

    def change_barrel(self, name):
        """
        if needs to change barrel name anywhere in runtime
        :param name:
        :return:
        """
        self.barrel_name = name

    def generate_batch(self, batch_size=128, df=None):
        """
        Split dataframe into small chunks of data with the the provided size (For neural network training)
        :param batch_size: Chunk size
        :param df: data frame to use
        :return:
        """
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
        """
        Return data frame splited as X Y (X input, Y output) and split it to chunks.
        :param X_keys: input names
        :param Y_keys: output names
        :param batch_size: chunks size
        :param df: data frame to use
        :return:
        """
        batches = self.generate_batch(batch_size=batch_size, df=df)
        while True:
            batch = next(batches)
            X = [batch[k] for k in X_keys]
            Y = [batch[k] for k in Y_keys]
            yield X, Y

    def generate_training_validation(self, batch_size=128, train_frac=.8):
        """
        Acts as the start point for the entire class.
        split data into training validation sets and process the chunks and records
        :param batch_size: chunks size
        :param train_frac: specifies the number of samples to return in random order
        (.8 means 80% of the data returned in random order)
        :return:
        """
        self.load_df()
        X_keys = ['image']
        Y_keys = ['angle', 'throttle']
        train_df = self.df.sample(frac=train_frac, random_state=200)  # training set
        val_df = self.df.drop(train_df.index)  # drop the training set and the rest is validation

        train_gen = self.generate_training(X_keys=X_keys, Y_keys=Y_keys, batch_size=batch_size, df=train_df)

        val_gen = self.generate_training(X_keys=X_keys, Y_keys=Y_keys, batch_size=batch_size, df=val_df)

        return train_gen, val_gen
