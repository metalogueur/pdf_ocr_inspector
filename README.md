# PDF OCR Inspector

This one-off script is used to scan through a directory's .pdf files and search for bad OCR 
in these files.

All bad files are then listed in a log file.

## Installation
Python 3.8 and over is required to run this script. It has not been tested with older
distributions.

Once Python is installed, simply download the `master.zip` archive and extract its contents
in a working directory.

Open a Terminal of PowerShell window in the `pdf_ocr_inspector/` directory and run the
following command to install the script's dependencies:

`$ pip install -r requirements.txt`

To make sure everything is installed properly, run the following command. You should see
this output:

```
$ python inspector.py -V
> PDF OCR Inspector version 0.1
```

## Usage

To run this script, you must write the following command from the Terminal or PowerShell 
window inside the `pdf_ocr_inspector/` directory:

`$ python inspector.py path_to_directory [-v]`

- `path_to_directory` must be a valid path enclosed in quotes;
- `-v` is an optional parameter to increase verbosity in the Terminal output and
the log file.

The script will go through each .pdf file, extracting text from the first few pages, and
will look for a particular pattern in the text. If that pattern shows up, the .pdf file
will be flagged as bad and its name will be logged in the `bad_files.txt` log stored in
`path_to_directory`.

## To-do list:
- Add concurrency to speed up the scanning process;
- Publish to PyPI.