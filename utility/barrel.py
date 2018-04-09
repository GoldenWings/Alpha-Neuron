from .singleton import Singleton
import csv
from .barrel_config import *
import cv2


class BarrelWriter(metaclass=Singleton):
        def __init__(self, objects, current_session=False):
            '''
            :param objects: contains all objects required for the class
            :param current_session: weather or not to save on the latest csv (Current session is the latest csv)
            '''
            self._car = objects.get('car')
            self.current_session = current_session
            self.csv_name = None

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
            angle = self._car.current_angle
            throttle = self._car.current_speed
            img = self._car.camera.frame
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
            angle = self._car.current_angle
            throttle = self._car.current_speed
            full_name = "img_%d_ttl_%.3f_agl_%.1f%s" % (img_number, throttle, angle, ".jpg")
            # next line for production
            # full_name = IMAGE_PATH + '/img_' + str(img_number) + '.jpg'
            cv2.imwrite(full_name, img)
            return full_name


class BarrelReader(metaclass=Singleton):
    def __init__(self):
        pass

    def get_record(self):
        pass

    def get_image(self):
        pass

    def __convert_to_df(self):
        pass
