"""Unit tests for PDF OCR Inspector."""

# imports
import inspector
import os
import pandas as pd
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


class TestPDFFileList(unittest.TestCase):

    def setUp(self) -> None:
        self.test_dir = os.path.join(os.getcwd(), 'test_dir')
        self.pdf_file_list = inspector.PDFFileList(self.test_dir)

    def tearDown(self) -> None:
        self.pdf_file_list = None

    def test_file_list_instance(self):
        self.assertIsInstance(self.pdf_file_list, inspector.PDFFileList)
        self.assertIsInstance(self.pdf_file_list.file_names, list)
        self.assertIsInstance(self.pdf_file_list.total_characters, list)
        self.assertIsInstance(self.pdf_file_list.total_bad_characters, list)
        self.assertIsInstance(self.pdf_file_list.percentage_bad_characters, list)
        self.assertIsInstance(self.pdf_file_list.directory, str)
        self.assertIsInstance(self.pdf_file_list.verbose, bool)

    def test_file_names(self):
        self.assertEqual(len(self.pdf_file_list.file_names), 3)
        self.assertIn(os.path.join(self.test_dir, 'one.pdf'), self.pdf_file_list.file_names)
        self.assertIn(os.path.join(self.test_dir, 'two.pdf'), self.pdf_file_list.file_names)
        self.assertIn(os.path.join(self.test_dir, 'three.pdf'), self.pdf_file_list.file_names)
        self.assertNotIn(os.path.join(self.test_dir, 'one.txt'), self.pdf_file_list.file_names)
        self.assertNotIn(os.path.join(self.test_dir, 'two.txt'), self.pdf_file_list.file_names)
        self.assertNotIn(os.path.join(self.test_dir, 'three.txt'), self.pdf_file_list.file_names)
        self.assertNotIn(os.path.join(self.test_dir, 'bad_files.txt'), self.pdf_file_list.file_names)

    def test_scan_files(self):
        self.pdf_file_list.scan_files()
        self.assertEqual(len(self.pdf_file_list.file_names), 3)
        self.assertEqual(len(self.pdf_file_list.total_characters), 3)
        self.assertEqual(len(self.pdf_file_list.total_bad_characters), 3)
        self.assertEqual(len(self.pdf_file_list.percentage_bad_characters), 3)

    def test_generate_dataframe(self):
        self.pdf_file_list.scan_files()
        self.assertIsInstance(self.pdf_file_list.generate_dataframe(), pd.DataFrame)


class TestScriptFunctions(unittest.TestCase):

    def setUp(self) -> None:
        self.path = os.path.join(os.getcwd(), 'test_dir')

    def test_get_path(self):
        path = inspector.get_path(self.path)
        self.assertTrue(os.path.isdir(path))


if __name__ == '__main__':
    unittest.main()
