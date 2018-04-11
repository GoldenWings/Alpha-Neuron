from .singleton import Singleton
from datetime import datetime


class Logger(metaclass=Singleton):
    LOG_PATH = '/home/pi/Development/Alpha-Neuron/utility/logs/'

    def __init__(self, agent, trainer, training, everything=True, interface=True):
        self._session_name = 'others.log'
        if not everything:
            if agent is None or trainer is None or training is None:
                raise ValueError("Not logging Every thing and you didn't specify what to log.")
            self.agent = agent
            self.trainer = trainer
            self.training = training
            self.everything = everything
            self.interface = interface
        else:
            self.agent = True
            self.trainer = True
            self.training = True
            self.everything = everything
            self.interface = True
        if not (agent and trainer and training):
            self._session_start_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M')
            self._session_name = self._session_start_time + '.log'
        if interface:
            self.interface_msg = []

    def log(self, msg, log_type=0):
        """
        :param msg: message to be logged
        :param log_type: type of log message (normal: 0, warning: 1, error: 2)
        :return:
        """
        msg_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        with open(Logger.LOG_PATH + self._session_name, 'a') as f:
            if log_type == 0:
                f.write("{} {}\n".format(msg_date, msg))
            elif log_type == 1:
                f.write("##WARNING##")
                f.write("{} {}\n".format(msg_date, msg))
                f.write("##WARNING##")
