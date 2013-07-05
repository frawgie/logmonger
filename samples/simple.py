#!/usr/bin/env python

# Simple logging samples

import logging
import logmonger


def my_func(log):
    log.info("This will save the name of the method in the log record's 'function' field")
    # We can temporarily enable debug logs:
    lvl = log.level
    log.setLevel(logging.DEBUG)
    log.debug('This is a low-level debug message')
    log.setLevel(lvl)


logger = logging.getLogger('my_logger')

# Connects by default to localhost:27017
handler = logmonger.MongoHandler(dbname='my_logs')
logger.addHandler(handler)

ex = OSError('This is an OS error')
logger.exception(ex)

logger.critical("My critical")
logger.error("My error")
logger.warning("My warning")

# By default, the logger will only log WARN level and above
logger.setLevel(logging.INFO)
logger.info('This is a message about %s' % ('a test',))

my_func(logger)
logger.debug('This will not appear in the logs db')
