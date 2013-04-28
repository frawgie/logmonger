#  "THE BEER-WARE LICENSE" (Revision 42):
# <jonas@agilefrog.se> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Jonas Ericsson.

"""
A logging handler for MongoDB in Python.

See samples on how to use it.
"""

import datetime
import logging
import pymongo

class MongoHandler(logging.Handler):
    """
    A class which sends records to a MongoDB.
    """

    def __init__(self, host="localhost", port=27017):
        """
        Initialize the connection pool and set the desired database.
        """
        logging.Handler.__init__(self)
        self.client = pymongo.MongoClient(host, port)
#        self.db = self.client.logs

    def emit(self, record):
        """
        Emit a record.

        Send the record to a mongo instance as a document.
        """
        try:
            message = None
            if isinstance(record.msg, Exception):
                message = self.transform_message(record)
            else:
                message = record.msg

            entry = {
                    'timestamp': datetime.datetime.now(),
                    'msg': message,
                    'level': record.levelname,
                    'module': record.module,
                    'lineno': record.lineno}
            # FIXME: Add threading info
            # FIXME: Add multiproc info
            print entry
            self.save(entry)
            #self.db.logs.save(entry)
        except Exception, e:
            print e
            self.handleError(record)

    def transform_message(self, message):
        exception_type = type(message.msg)
        log_message = str(message.msg)
        arguments = message.msg.args
        return "%s: %s, %s" % (exception_type, log_message, arguments) 

    def save(self, entry):
       self.client.logs.logs.save(entry)

