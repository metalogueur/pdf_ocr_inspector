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
import logging
import os
import re
from pdfminer.high_level import extract_text
from progress.bar import Bar

# Globals
BAD_OCR_LOG_FILE_NAME = 'bad_files.txt'
BAD_OCR_PATTERN = r'\(cid\:[0-9]+\)'
SCRIPT_NAME = 'PDF OCR Inspector'
SCRIPT_VERSION = 0.1

bad_ocr_logger = logging.getLogger('bad_ocr_files')


# Classes
class InspectorParser(argparse.ArgumentParser):
    """A script-specific parser."""

    parser_description = "Scans through a directory's files looking for bad OCR."

    def __init__(self, script_name: str, script_version: float):
        if not isinstance(script_name, str):
            raise TypeError("script_name must be a string.")
        if not isinstance(script_version, float):
            raise TypeError("script_version must be a float.")

        super(InspectorParser, self).__init__(description=self.parser_description)
        self.script_name = script_name
        self.script_version = script_version

    def add_all_arguments(self):
        """Adds all parser arguments in one call."""
        self.add_argument('-V', '--version', help='show script version and exit', action='version',
                          version=f"{self.script_name} version {self.script_version}")
        self.add_argument('path_to_dir', help='a valid directory path', type=get_file_list)
        self.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')


# Script functions
def main():
    """The main function of the script."""

    parser = InspectorParser(SCRIPT_NAME, SCRIPT_VERSION)
    parser.add_all_arguments()

    try:
        args = parser.parse_args()
        instantiate_logger(args.path_to_dir[1])

        if args.verbose:
            print("Starting script...")

        scan_files(args.path_to_dir[0], args.path_to_dir[1], args.verbose)

        if args.verbose:
            print("End of script.")

    except (FileNotFoundError, TypeError) as erreur:
        print(erreur.strerror)
        return
    except Exception as erreur:
        print(erreur)
        return


def get_file_list(path_to_dir: str) -> tuple:
    """Returns the contents of a directory as a list. Raises an error otherwise.

        :param path_to_dir: A valid path to a directory.
        :type path_to_dir: str
        :returns: a tuple containing the file list and the path string
        :rtype: tuple
        """
    if not isinstance(path_to_dir, str):
        raise TypeError("path_to_dir must be a string.")
    if not os.path.isdir(path_to_dir):
        raise FileNotFoundError("path_to_dir must be a valid path.")

    return os.listdir(path_to_dir), path_to_dir


def instantiate_logger(path_to_log_file_dir: str) -> None:
    """Creates a Logger instance, a log file and returns the Logger instance.

    :param path_to_log_file_dir: A valid path to a directory
    :type path_to_log_file_dir: str
    :returns: None
    :rtype: NoneType
    """
    if not isinstance(path_to_log_file_dir, str):
        raise TypeError("path_to_log_file must be a string.")
    if not os.path.isdir(path_to_log_file_dir):
        raise FileNotFoundError("path_to_log_file_dir must be a valid path.")

    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    log_file = logging.FileHandler(os.path.join(path_to_log_file_dir, BAD_OCR_LOG_FILE_NAME), encoding='utf-8')
    log_file.setFormatter(formatter)
    bad_ocr_logger.addHandler(log_file)
    bad_ocr_logger.setLevel('INFO')


def scan_files(file_list: list, path_to_dir: str, verbose: bool) -> None:
    """Extracts text from all pdf files and searches for bad OCR.

    :param file_list: The list of all files and directories in a single directory.
    :type file_list: list
    :param path_to_dir: The path to the directory.
    :type path_to_dir: str
    :param verbose: The verbose flag received from the command line prompt.
    :type verbose: bool
    :returns: None
    :rtype: NoneType
    """
    if not isinstance(file_list, list):
        raise TypeError("file_list must be a list.")
    if not isinstance(path_to_dir, str):
        raise TypeError("path_to_dir must be a string.")
    if verbose:
        bad_ocr_logger.info(f"Scanning files in {path_to_dir}...")

    bar = Bar('Scanning', max=len(file_list))

    for file in file_list:
        path_to_file = os.path.join(path_to_dir, file)
        if os.path.isfile(path_to_file) and file.endswith('.pdf'):
            text = extract_text(path_to_file, maxpages=2)
            if re.search(BAD_OCR_PATTERN, text):
                bad_ocr_logger.warning(f"bad file: {file}")
            elif verbose:
                bad_ocr_logger.info(f"good file: {file}")
        bar.next()

    bar.finish()

    if verbose:
        print(f"Bad OCR file list written in {os.path.join(path_to_dir, BAD_OCR_LOG_FILE_NAME)}")


if __name__ == '__main__':
    main()
