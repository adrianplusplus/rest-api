"""Module which imports all the basic utility functions."""
from __future__ import absolute_import

import logging
import os
from logging import handlers


class LogFormatter(logging.Formatter):
    """."""

    datefmt = '%Y-%m-%d %H:%M:%S'

    def format(self, record):
        """."""
        error_location = "%s.%s" % (record.name, record.funcName)
        line_number = "%s" % (record.lineno)
        location_line = error_location[:32] + ":" + line_number
        s = "%.19s [%-8s] [%-36s] %s" % (self.formatTime(record, self.datefmt),
                                         record.levelname, location_line,
                                         record.getMessage())
        return s


def setup_logger(logging_location, logging_level):
    """Set up the global logging settings."""
    ALL_LOG_FILENAME = '{0}/all.log'.format(logging_location)
    ERROR_LOG_FILENAME = '{0}/error.log'.format(logging_location)
    if not os.path.exists(logging_location):
        os.makedirs(logging_location)

    logger = logging.getLogger()
    logger.setLevel(logging_level)

    # create console handler and set custom level
    handler = logging.StreamHandler()
    handler.setLevel(logging_level)
    handler.setFormatter(LogFormatter())
    logger.addHandler(handler)

    # create error file handler and set level to error
    handler = logging.handlers.RotatingFileHandler(ERROR_LOG_FILENAME,
                                                   maxBytes=1000000,
                                                   backupCount=100)
    handler.setLevel(logging.ERROR)
    handler.setFormatter(LogFormatter())
    logger.addHandler(handler)

    # create debug file handler and set level to debug
    handler = logging.handlers.RotatingFileHandler(ALL_LOG_FILENAME,
                                                   maxBytes=1000000,
                                                   backupCount=100)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(LogFormatter())
    logger.addHandler(handler)
