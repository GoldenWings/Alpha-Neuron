from .singleton import Singleton
import csv
from .barrel_config import *
import cv2


class BarrelWriter(metaclass=Singleton):
        def __init__(self, objects, current_session=True):
            self._car = objects.get('car')
            self.current_session = False
            self.csv_name = None
            if current_session:
                self.current_session = True

        def get_csv(self):
            csv_number = count_datasets()
            if not self.current_session or csv_number == 0:
                self.make_csv()
                self.current_session = True
            elif self.current_session:
                self.csv_name = 'session' + str(csv_number) + '.csv'
                if os.path.isfile(os.path.join(DATA_PATH, self.csv_name)):
                    return
                self.make_csv()
            else:
                self.make_csv()

        def get_record(self):
            angle = self._car.current_angle
            throttle = self._car.current_speed
            img = self._car.camera.frame
            img_name = self.save_image(img)
            record = {'angle': angle, 'throttle': throttle, 'image': img_name}
            return record

        def make_csv(self):
            csv_number = count_datasets() + 1
            self.csv_name = 'session_' + str(csv_number) + '.csv'
            record = self.get_record()
            with open(self.csv_name, 'a') as f:
                w = csv.DictWriter(f, record.keys())
                w.writeheader()
                w.writerow(record)

        def write_csv(self):
            if self.csv_name is None:
                self.get_csv()
            else:
                record = self.get_record()
                with open(self.csv_name, 'a') as f:
                    w = csv.DictWriter(f, record.keys())
                    w.writerow(record)

        # noinspection PyMethodMayBeStatic
        def save_image(self, img):
            img_number = count_images() + 1
            # for testing store throttle and angle in image name
            angle = self._car.current_angle
            throttle = self._car.current_speed
            full_name = "img_%d_ttl_%.3f_agl_%.1f%s" % (img_number, throttle, angle, ".jpg")
            #full_name = IMAGE_PATH + '/img_' + str(img_number) + '.jpg'
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
