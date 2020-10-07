# PDF OCR Inspector

This one-off script is used to scan through a directory's .pdf files and search for bad OCR 
in these files.

All files and a few metrics are then listed in a log file.

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
> PDF OCR Inspector version 0.2
```

## Usage

To run this script, you must write the following command from the Terminal or PowerShell 
window inside the `pdf_ocr_inspector/` directory:

`$ python inspector.py path_to_directory [-v]`

- `path_to_directory` must be a valid path enclosed in quotes;
- `-v` is an optional parameter to increase verbosity in the Terminal output.

The script will go through each .pdf file, extracting text and will look for a particular pattern in the text. 
That pattern is considered as characters being "badly encoded". Metrics will be built with the files' OCR text:

- the total of characters;
- the total of bad characters;
- the percentage of bad characters.

At the end of the script, an Excel file is created containing all these metrics.

## To-do list:
- Add concurrency to speed up the scanning process.