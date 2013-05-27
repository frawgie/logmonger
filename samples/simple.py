#!/usr/bin/env python

# Simple logging samples

import logging
import logmonger


def my_func(log):
    log.info('This will save the name of the method in the log record')


logger = logging.getLogger()
handler = logmonger.MongoHandler(dbname='my_logs', collection='log_records')
logger.addHandler(handler)

ex = OSError('This is an OS error')
logger.exception(ex)

logger.setLevel(logging.INFO)
logger.info('This is a message about %s' % ('a test',))

my_func(logger)
