# zhader-dom-browser
DOM Browser/Indexer that fetches a site's DOM and indexes it with QR codes.

# Dom Browser/Indexer with QR Codes

This Python script fetches the Document Object Model (DOM) of a webpage, indexes each HTML element with a QR code and allows you to export the HTML. It also provides a view of the fetched webpage. 

## Dependencies

To run this script, you will need to have the following Python packages installed:

- `tkinter`
- `requests`
- `beautifulsoup4`
- `qrcode`
- `PyQt5`
- `PyQtWebEngine`
- `ImageMagick`

The `tkinter`, `requests`, `beautifulsoup4`, and `qrcode` packages are used for GUI operations, making HTTP requests, parsing HTML, and generating QR codes respectively. `PyQt5` and `PyQtWebEngine` are used to display the fetched webpage. `ImageMagick` is used for image operations, specifically resizing the generated QR code images.

## Installation Instructions

First, ensure that you have Python and pip (Python's package manager) installed. 

Next, install the required Python packages with the following commands:

```shell
pip install requests beautifulsoup4 qrcode pyqt5 PyQtWebEngine

The tkinter package is included with Python, so you do not need to install it separately.

**Note: Depending on your Python setup, you might need to use pip3 instead of pip, or python -m pip.**

You will also need to install ImageMagick, a software suite for creating, editing, and composing bitmap images. On Linux, use your distribution's package manager. For example, on Ubuntu or Debian, you can use the command sudo apt-get install imagemagick.

Usage Instructions:

0. Create a folder in the same directory as the script named 'qrcodes'.

1. Run the Python script. A window titled "Dom Browser/Indexer" will open.

2. Enter the URL of the webpage you want to fetch in the URL field.

3. Click the "Fetch" button. The DOM structure of the webpage will be displayed in the "DOM Structure" text box and a new window will open showing the webpage. The "QR Code DOM Index" text box will display the file paths of the generated QR codes. A grid of QR codes will also be displayed in a separate window.

4.(Optional) Click the "Export HTML" button to save the HTML content to a file.

5. You can close the program by closing the main window.

![Image alt text](https://github.com/txtatech/zhader-dom-browser/blob/main/zhader-dom-browser.png)
