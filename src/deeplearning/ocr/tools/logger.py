# -*- coding:utf-8 -*-
import logging
import logging.handlers
from .common import format_time, Singleton
import os


@Singleton
class Logger:

    FORMAT = "%(asctime)s - %(levelname)s: %(message)s"
    FILE_FORMAT = "%Y-%m-%d"
    LOG_SUF = ".log"
    DIR_NAME = "logs"

    def __init__(self, loc='../../'):
        if self.DIR_NAME not in loc:
            loc = os.path.join(loc, self.DIR_NAME)
            if not os.path.exists(loc):
                os.makedirs(loc)
        self.path = loc
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        file_handler = logging.handlers.TimedRotatingFileHandler(os.path.join(self.path, format_time(self.FILE_FORMAT) + self.LOG_SUF), when='D',
                                                                 interval=1, backupCount=40)
        file_handler.setLevel(logging.DEBUG)
        conslog = logging.StreamHandler()
        conslog.setLevel(logging.WARNING)
        fmt = logging.Formatter(self.FORMAT)

        file_handler.setFormatter(fmt)
        conslog.setFormatter(fmt)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(conslog)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def waring(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)



