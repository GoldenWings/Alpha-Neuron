from evdev import InputDevice, list_devices


class F710:
    f710 = None
    _f710_name = ["Logitech Logitech Cordless RumblePad 2", "Logitech Gamepad F710"]
    _f710_path = ''

    @property
    def _find_f710(self):
        """
        This method search for a Logitech f710 gamepad and if founded it gets it path and set it to _f710_path
        :return: return a boolean ex:True if gamepad founded
        """
        devices = [InputDevice(fn) for fn in list_devices()]
        for device in devices:
            if device.name in self._f710_name:
                self._f710_path = str(device.fn)
                return True

    def _set_f710(self):
        """
        This method initialize the gamepad if founded
        :return: it has no return type
        """
        if self._find_f710:
            self.f710 = InputDevice(self._f710_path)
        else:
            raise Exception('Please check the USB dongle, no F710 found !!')

    def __init__(self):
        self._set_f710()

    def __del__(self):
        self.f710 = None
