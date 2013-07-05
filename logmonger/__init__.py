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

    def __init__(self, host="localhost", port=27017, dbname='logs', collection=None):
        """
        Initialize the connection pool and set the desired database.

        :param host: the IP address or hostname for the MongoDb (default: localhost)
        :param port: the port (default: 27017)
        :param dbname: the name of the DB to save log records to, will default to 'logs'
        :param collection: the logger name is used if it is None, otherwise the set value (default: None)
        """
        logging.Handler.__init__(self)
        self.client = pymongo.MongoClient(host, port)
        self.dbname = dbname
        self.collection = collection

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
                    'function': record.funcName,
                    'lineno': record.lineno,
                    'name': record.name
                }

            self.add_thread_info(entry, record)
            self.add_multiproc_info(entry, record)

            self.save(entry)
        except Exception, _:
            self.handleError(record)

    def transform_message(self, message):
        """
        Exceptions can't be serialized directly so we need to transform it
        to a string instead. We use the format: Type: message, arguments.
        """
        exception_type = type(message.msg)
        log_message = str(message.msg)
        arguments = message.msg.args
        return "%s: %s, %s" % (exception_type, log_message, arguments)

    def add_thread_info(self, entry, record):
        """
        Add thread information in its own key.
        """
        entry['thread'] = {
            'thread': record.thread,
            'thread_name': record.threadName,
        }

    def add_multiproc_info(self, entry, record):
        """
        Add process information in its own key.
        """
        entry['process'] = {
            'process_name': record.processName,
            'process_id': record.process,
        }

    def save(self, entry):
        """
        Save an entry to the collection. We want this in a separate method since
        it makes it easier to stub it with mox.
        """
        collection = self.collection if self.collection else entry['name']
        self.client[self.dbname][collection].save(entry)
