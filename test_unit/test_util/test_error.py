import logging
import unittest

from discbase.util.error import log_and_raise


class TestError(unittest.TestCase):
    def test_log_and_raise_happy_path(self):
        logger = logging.getLogger("test")
        with self.assertRaises(Exception) as context:
            log_and_raise(logger, "dummy msg")
        self.assertEqual("dummy msg", str(context.exception))

    def test_log_and_raise_with_exception(self):
        logger = logging.getLogger("test")
        with self.assertRaises(FileNotFoundError) as context:
            log_and_raise(logger, "dummy msg", exception=FileNotFoundError)
        self.assertEqual("dummy msg", str(context.exception))
