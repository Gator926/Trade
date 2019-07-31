from unittest import TestCase
from IO.File import FileReadAndWrite


class TestFileReadAndWrite(TestCase):
    def test_file_write_and_read(self):
        FileReadAndWrite.write("/root/test/btc.txt", "9852.35")
        self.assertEqual(FileReadAndWrite.read("/root/test/btc.txt"), "9852.35")