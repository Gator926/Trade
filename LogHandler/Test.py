from unittest import TestCase
from LogHandler.LogHandler import LogHandler


class TestLogHandler(TestCase):
    def setUp(self):
        self.log_handler = LogHandler()

    def test_info(self):
        self.log_handler.info("hello")

    def test_debug(self):
        self.log_handler.debug("hello")

    def test_warning(self):
        self.log_handler.warning("hello")

    def test_error(self):
        self.log_handler.error("hello")
