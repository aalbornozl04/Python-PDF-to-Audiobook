PDF to Audiobook Converter

A simple Python script that converts PDF files into audiobooks (.wav files) using text-to-speech (TTS).

This script reads a PDF, extracts its text, and uses the pyttsx3 library to generate an audio version, which is saved in the same directory.

Features

PDF Text Extraction: Uses PyPDF2 to open and read text from each page of a PDF.

Text-to-Speech: Employs pyttsx3 to convert the extracted text into spoken audio.

Smart Dependency Checking: Checks for required libraries on startup and provides installation instructions if they are missing.

Flexible Input: Run the script by passing a PDF file path as a command-line argument or by setting the default path in the script.

Backwards Compatibility: Automatically handles different versions of PyPDF2 (both modern PdfReader and legacy PdfFileReader).

User Feedback: Prints its progress as it extracts text and warns about image-only (scanned) pages.

Voice Configuration: Sets a sensible speaking rate and attempts to select a female voice for a better listening experience.

Automatic Naming: The output audio file is automatically named based on the input PDF (e.g., my_report.pdf becomes my_report_audio.wav).

Installation

This script requires Python 3 and the following Python libraries:

pyttsx3: A text-to-speech library.

PyPDF2: A PDF manipulation library.

You can install them using pip:

pip install pyttsx3 PyPDF2


Usage

You can run the script in two ways:

Option 1: As a Command-Line Argument (Recommended)

Pass the path to your PDF file as an argument to the script. Make sure to use quotes if your file path contains spaces.

python your_script_name.py "C:\Users\YourName\Documents\my_book.pdf"


Option 2: Edit the Script

You can hardcode the path to your PDF directly in the main() function of the script.

def main(pdf_path=None):
    if pdf_path is None:
        #
        # EDIT THIS LINE
        #
        pdf_path = r"C:\path\to\your\document.pdf"
    
    # ... rest of the script


After saving your change, you can run the script without any arguments:

python your_script_name.py


Output

The script will create a .wav file (e.g., my_book_audio.wav) in the same directory where you ran the script.

How It Works

Imports & Checks: Verifies that pyttsx3 and PyPDF2 are installed.

Get PDF Path: Checks for a command-line argument (sys.argv[1]). If one isn't found, it uses the hardcoded path.

Initialize PDF Reader: It tries the modern PdfReader class first. If that fails (due to an older PyPDF2 version), it falls back to the legacy PdfFileReader.

Initialize TTS Engine: It initializes pyttsx3, sets the speaking rate to 200 WPM, and attempts to select the second available voice (voices[1]).

Extract Text: It loops through all pages, extracts text, and stores it in a list.

Save to File: It joins all extracted text with newline separators and calls engine.save_to_file() to create the .wav file.

Run: engine.runAndWait() processes the entire audio generation task before the script exits.
