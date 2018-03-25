from evdev import InputDevice, list_devices


class F710:
    f710 = None
    __f710_name = ["Logitech Logitech Cordless RumblePad 2", "Logitech Gamepad F710"]
    __f710_path = ''
    ___f710_founded = False

    @property
    def __find_f710(self):

        devices = [InputDevice(fn) for fn in list_devices()]
        for device in devices:
            if device.name in self.__f710_name:
                self.__f710_path = str(device.fn)
                return True

    def __set_f710(self):
        # Open the device
        if self.__find_f710:
            self.f710 = InputDevice(self.__f710_path)
        else:
            raise Exception('Please check the USB dongle, no F710 found !!')

    def __init__(self):
        self.__set_f710()
