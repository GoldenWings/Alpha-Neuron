from evdev import InputDevice, list_devices


class F710:
    f710 = None
    _f710_name = ["Logitech Logitech Cordless RumblePad 2", "Logitech Gamepad F710"]
    _f710_path = ''

    @property
    def _find_f710(self):

        devices = [InputDevice(fn) for fn in list_devices()]
        for device in devices:
            if device.name in self._f710_name:
                self._f710_path = str(device.fn)
                return True

    def _set_f710(self):
        # Open the device
        if self._find_f710:
            self.f710 = InputDevice(self._f710_path)
        else:
            raise Exception('Please check the USB dongle, no F710 found !!')

    def __init__(self):
        self.__set_f710()

    def __del__(self):
        self.f710 = None
