# inspector.py
#
# Copyright (C) 2020 Benoit Hamel, Bibliothèque, HEC Montréal
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# This script is used to go through a directory's .pdf files and search for bad OCR.

# Imports
import argparse
import numpy as np
import os
import pandas as pd
import re
from pdfminer.high_level import extract_text
from progress.bar import Bar

# Globals
BAD_OCR_LOG_FILE_NAME = 'bad_ocr.xlsx'
BAD_OCR_PATTERN = r'\(cid\:[0-9]+\)'
SCRIPT_NAME = 'PDF OCR Inspector'
SCRIPT_VERSION = '0.2.1'


# Classes
class InspectorParser(argparse.ArgumentParser):
    """A script-specific parser."""

    parser_description = "Scans through a directory's files looking for bad OCR."

    def __init__(self, script_name: str, script_version: str):
        """Class constructor

        :param script_name:     The name of this script
        :type script_name:      str
        :param script_version:  The version of this script
        :type script_version:   str
        """
        if not isinstance(script_name, str):
            raise TypeError("script_name must be a string.")
        if not isinstance(script_version, str):
            raise TypeError("script_version must be a string.")

        super(InspectorParser, self).__init__(description=self.parser_description)
        self.script_name = script_name
        self.script_version = script_version
        self.add_all_arguments()

    def add_all_arguments(self):
        """Adds all parser arguments in one call."""
        self.add_argument('-V', '--version', help='show script version and exit', action='version',
                          version=f"{self.script_name} version {self.script_version}")
        self.add_argument('path_to_dir', help='a valid directory path', type=get_path)
        self.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')


class PDFFileList:
    """List of a directory's .pdf files and their statistics concerning OCR quality."""

    def __init__(self, path_to_dir: str, verbose: bool = False):
        """Class constructor

        :param path_to_dir:     The directory path string
        :type path_to_dir:      str
        :param verbose:         The verbose flag for the command line
        :type verbose:          bool
        """

        if not isinstance(path_to_dir, str):
            raise TypeError("path_to_dir must be a string.")
        if not isinstance(verbose, bool):
            raise TypeError("verbose must be a boolean.")
        if not os.path.isdir(path_to_dir):
            raise FileNotFoundError("path_to_dir must be a valid path.")

        self.file_names = []
        self.total_characters = []
        self.total_bad_characters = []
        self.percentage_bad_characters = []
        self.directory = path_to_dir
        self.verbose = verbose
        self.get_pdf_files()

    def get_pdf_files(self) -> None:
        """ Retrieves all pdf files contained in self.directory and populates self.file_names with the file names. """

        file_list = os.listdir(self.directory)
        for file in file_list:
            path_to_file = os.path.join(self.directory, file)
            if os.path.isfile(path_to_file) and file.endswith('.pdf'):
                self.file_names.append(path_to_file)

    def scan_files(self) -> None:
        """ Scans all pdf files contained in self.file_names in search of bad OCR and fills the different
        statistics lists: self.total_characters, self.total_bad_characters and self.percentage_bad_characters.
        """
        if self.file_names:
            if self.verbose:
                print(f"Scanning files in {self.directory}...")

            bar = Bar('Scanning', max=len(self.file_names))

            for file in self.file_names:
                try:
                    text = extract_text(file)
                except RecursionError:
                    print(f" {file} scanning has failed due to a RecursionError. Continuing with next file...")
                    # TODO : convert the three appends into a single method
                    self.total_characters.append(np.nan)
                    self.total_bad_characters.append(np.nan)
                    self.percentage_bad_characters.append(np.nan)
                    continue
                except Exception as erreur:
                    # TODO : create log file with Traceback here
                    print(f" {file} scanning has failed due to '{erreur}'. Continuing with next file...")
                    self.total_characters.append(np.nan)
                    self.total_bad_characters.append(np.nan)
                    self.percentage_bad_characters.append(np.nan)
                    continue
                else:
                    self.total_characters.append(len(text))
                    stripped_text = re.subn(BAD_OCR_PATTERN, '', text)
                    self.total_bad_characters.append(stripped_text[1])
                    self.percentage_bad_characters.append((1 - (len(stripped_text[0]) / len(text))) * 100)
                    bar.next()

            bar.finish()
        else:
            if self.verbose:
                print("No .pdf file to scan.")

    def generate_dataframe(self) -> pd.DataFrame:
        """Generates a Pandas DataFrame from the statistics lists and returns it
        :returns:   A DataFrame containing all bad OCR statistics.
        :rtype:     pd.DataFrame
        """
        if self.verbose:
            print("Generating DataFrame...")

        data = {
            'file_names': self.file_names,
            'total_characters': self.total_characters,
            'total_bad_characters': self.total_bad_characters,
            'percentage_bad_characters': self.percentage_bad_characters
        }
        return pd.DataFrame(data)

    def generate_excel_report(self) -> None:
        """Generates an Excel file from a Pandas DataFrame."""

        df = self.generate_dataframe()
        excel_file = os.path.join(self.directory, BAD_OCR_LOG_FILE_NAME)

        if self.verbose:
            print(f"Generating Excel file in {self.directory}...")

        df.to_excel(excel_file, index=False)


# Script functions
def main():
    """The main function of the script."""

    parser = InspectorParser(SCRIPT_NAME, SCRIPT_VERSION)

    try:
        args = parser.parse_args()

        if args.verbose:
            print("Starting script...")

        pdf_list = PDFFileList(args.path_to_dir, args.verbose)
        pdf_list.scan_files()
        pdf_list.generate_excel_report()

        if args.verbose:
            print("End of script.")

    except (FileNotFoundError, TypeError) as erreur:
        print(erreur.strerror)
        return
    except Exception as erreur:
        print(erreur)
        return


def get_path(path_to_dir: str) -> str:
    """Returns the directory path string if it is a valid path. Raises an error otherwise.

        :param path_to_dir: A valid path to a directory.
        :type path_to_dir: str
        :returns: the directory path string
        :rtype: str
        """
    if not isinstance(path_to_dir, str):
        raise TypeError("path_to_dir must be a string.")
    if not os.path.isdir(path_to_dir):
        raise FileNotFoundError("path_to_dir must be a valid path.")

    return path_to_dir


if __name__ == '__main__':
    main()
