import queue
from datetime import datetime

from utility.status import Status
from .singleton import Singleton


class Logger(metaclass=Singleton):
    LOG_PATH = '/home/pi/Development/Alpha-Neuron/utility/logs/'

    def __init__(self, which=None, everything=True):
        self._session_name = 'others.log'
        self.status = Status()
        if not everything:
            self.agent = which.get('agent') if which.get('agent') else False
            self.trainer = which.get('agent') if which.get('agent') else False
            self.everything = everything
            self.interface = which.get('agent') if which.get('agent') else False
            if not (self.agent and self.trainer and self.interface):
                raise ValueError("Not logging Every thing and you didn't specify what to log.")
        else:
            self.agent = True
            self.trainer = True
            self.everything = everything
            self._session_start_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M')
            self._session_name = self._session_start_time + '.log'
            self.interface_msgs = queue.LifoQueue()

    def log(self, msg, error_type=None):
        """
        :param msg: message to be logged
        :param error_type: type of log message __name__ of module happened
        :return:
        """
        if self.status.is_trainer is not self.trainer or self.status.is_agent is not self.agent:
            return
        msg_date = datetime.now().strftime('%H:%M')
        with open(Logger.LOG_PATH + self._session_name, 'a') as f:
            if error_type:
                formatted_msg = "@@{}\t{}\n{}".format(error_type, msg_date, msg)
                f.write(formatted_msg)
            else:
                formatted_msg = "##'\n'{}\t{}".format(msg_date, msg)
                f.write(formatted_msg)
            self.interface_msgs.put(bytes(formatted_msg, 'utf-8'))
