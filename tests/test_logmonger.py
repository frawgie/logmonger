import datetime
import logging
import mox
import unittest

import logmonger
import pymongo

class TestLogMonger(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()
        self.handler = logmonger.MongoHandler()
        self.logger = logging.getLogger()
        self.logger.addHandler(self.handler)


    def tearDown(self):
        self.mox.UnsetStubs()

    def test_handler(self):
        self.mox.StubOutWithMock(self.handler, 'handle')
        self.handler.handle(mox.IsA(logging.LogRecord))

        self.mox.ReplayAll()
        self.logger.info("Log me.")
        self.mox.VerifyAll()


    def test_emit(self):
        fake_date = "2013 3 7"
        log_message = "Log me too."

        self.mox.StubOutWithMock(self.handler, 'save')
        self.mox.StubOutWithMock(datetime, 'datetime')
        datetime.datetime.now().AndReturn(fake_date)

        self.handler.save(mox.And(
            mox.ContainsKeyValue("msg", log_message),
            mox.ContainsKeyValue("level", "INFO"),
            mox.ContainsKeyValue("timestamp", fake_date)))

        self.mox.ReplayAll()

        self.logger.info(log_message)

        self.mox.VerifyAll()

    def test_emit_exception(self):
        fake_date = "2013 3 7"
        log_message = "This is my output!"

        self.mox.StubOutWithMock(self.handler, 'save')
        self.mox.StubOutWithMock(self.handler, 'transform_message')
        self.mox.StubOutWithMock(datetime, 'datetime')

        self.handler.transform_message(mox.IgnoreArg()).AndReturn(log_message)
        datetime.datetime.now().AndReturn(fake_date)
        datetime.datetime.now().AndReturn(fake_date) # FIXME
        self.handler.save(mox.ContainsKeyValue("msg", log_message))

        self.mox.ReplayAll()

        my_exception = Exception(log_message)
        self.logger.exception(my_exception)

        self.mox.VerifyAll()
