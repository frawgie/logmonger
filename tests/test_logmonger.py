import datetime
import logging
import mox
import unittest

import logmonger
import pymongo

class TestLogMonger(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_handler(self):
        handler = self.mox.CreateMock(logmonger.MongoHandler())
        logger = logging.getLogger()
        logger.addHandler(handler)

        handler.handle(mox.IsA(logging.LogRecord))

        self.mox.ReplayAll()
        logger.info("Log me.")
        self.mox.VerifyAll()


    def test_emit(self):
        fake_date = "2013 3 7"
        handler = logmonger.MongoHandler()
        logger = logging.getLogger()
        logger.addHandler(handler)

        self.mox.StubOutWithMock(handler, 'save')
        self.mox.StubOutWithMock(datetime, 'datetime')
        datetime.datetime.now().AndReturn(fake_date)

        handler.save({'timestamp': fake_date, # Ugly!
            'msg': "Log me too.", 'lineno': 44, 'module': 'test_logmonger', 'level': 'INFO'})

        self.mox.ReplayAll()

        logger.info("Log me too.")

        self.mox.VerifyAll()

    def test_emit_exception(self):
        fake_date = "2013 3 7"
        log_message = "This is my output!"

        handler = logmonger.MongoHandler()
        logger = logging.getLogger()
        logger.addHandler(handler)

        self.mox.StubOutWithMock(handler, 'save')
        self.mox.StubOutWithMock(handler, 'transform_message')
        self.mox.StubOutWithMock(datetime, 'datetime')

        handler.transform_message(mox.IgnoreArg()).AndReturn(log_message)
        datetime.datetime.now().AndReturn(fake_date)
        datetime.datetime.now().AndReturn(fake_date) # FIXME
        handler.save(mox.ContainsKeyValue("msg", log_message))

        self.mox.ReplayAll()

        my_exception = Exception(log_message)
        logger.exception(my_exception)

        self.mox.VerifyAll()
