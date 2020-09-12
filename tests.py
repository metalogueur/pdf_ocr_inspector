"""Unit tests for PDF OCR Inspector."""

# imports
import logging
import inspector
import os
import unittest


# Classes
class TestInspectorParser(unittest.TestCase):

    def setUp(self) -> None:
        self.script_name = 'Roger'
        self.script_version = 0.42
        self.parser = inspector.InspectorParser(self.script_name, self.script_version)

    def test_parser_instance(self):
        self.assertIsInstance(self.parser, inspector.InspectorParser)
        self.assertIsInstance(self.parser.script_name, str)
        self.assertIsInstance(self.parser.script_version, float)
        self.assertEqual(self.parser.script_name, self.script_name)
        self.assertEqual(self.parser.script_version, self.script_version)


class TestScriptFunctions(unittest.TestCase):

    def setUp(self) -> None:
        self.path = os.path.join(os.getcwd(), 'test_dir')
        self.file_list = ['one.txt',
                          'two.txt',
                          'three.txt',
                          'bad_files.txt']
        self.logger = logging.getLogger('test_logger')

    def test_file_list(self):
        file_list = inspector.get_file_list(self.path)
        self.assertIsInstance(file_list, tuple)
        for file in file_list[0]:
            self.assertIn(file, self.file_list)
        self.assertEqual(file_list[1], self.path)

    def test_scan_files(self):
        inspector.instantiate_logger(self.path)
        inspector.scan_files(self.file_list, self.path, False)
        file_list = inspector.get_file_list(self.path)
        self.assertIn('bad_files.txt', file_list[0])


if __name__ == '__main__':
    unittest.main()
