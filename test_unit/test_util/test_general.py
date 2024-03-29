import tempfile
import unittest

from discbase.enumeration.URLType import URLType
from discbase.util.general import get_file_extension, get_random_string, get_url_type


class TestGeneral(unittest.TestCase):
    def test_get_random_string(self):
        rand_str_5 = get_random_string(5)
        rand_str_3 = get_random_string(3)
        self.assertEqual(5, len(rand_str_5))
        self.assertEqual(3, len(rand_str_3))

        with self.assertRaises(Exception) as context:
            get_random_string(0)
        self.assertEqual("Length must be greater than or equal to 1.", str(context.exception))

        with self.assertRaises(Exception) as context:
            get_random_string(-1)
        self.assertEqual("Length must be greater than or equal to 1.", str(context.exception))

    def test_get_file_extension(self):
        ext_png_local = get_file_extension("foo/bar.png")
        ext_png_online = get_file_extension("http://foo/bar.png")
        self.assertEqual(".png", ext_png_local)
        self.assertEqual(".png", ext_png_online)

        with self.assertRaises(Exception) as context:
            get_file_extension("foo")
        self.assertEqual("No file extension found.", str(context.exception))

    def test_get_url_type(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            url_local = get_url_type(tmp_dir)
        url_online = get_url_type("http://foo/bar")
        url_unknown = get_url_type("")
        self.assertEqual(URLType.LOCAL, url_local)
        self.assertEqual(URLType.ONLINE, url_online)
        self.assertEqual(URLType.UNKNOWN, url_unknown)
