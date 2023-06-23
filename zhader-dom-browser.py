import tkinter as tk
from tkinter import filedialog
import requests
from bs4 import BeautifulSoup
import qrcode
import os
import subprocess

# Function to generate a QR code with coordinates
def generate_qr_code(tag_name, coordinates, url):
    counter = 1
    file_path = ""

    while True:
        qr_code_file_name = f"{coordinates[0]}_{coordinates[1]}_{tag_name}_{counter}.png"
        file_path = os.path.join("qrcodes", qr_code_file_name)

        if not os.path.exists(file_path):
            break

        counter += 1

    qr_code = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    unique_url = f"{url}#{'-'.join(map(str, coordinates))}"
    qr_code.add_data(f"[{', '.join(map(str, coordinates))}]\n{unique_url}")
    qr_code.make(fit=True)

    qr_image = qr_code.make_image(fill_color="black", back_color="white")
    qr_image.save(file_path)

    return file_path

# Function to resize the QR code image
def resize_qr_image(file_path, size):
    resized_path = os.path.splitext(file_path)[0] + "_resized.png"
    subprocess.run(["convert", file_path, "-resize", f"{size[0]}x{size[1]}", resized_path], check=True)
    return resized_path

# Function to render the DOM structure recursively
def render_dom(element, url, coordinate_tracker, text_output, qr_output, qr_window):
    if element.name:
        tag_name = element.name
        coordinates = coordinate_tracker.get_coordinates()

        text_output.insert(tk.END, f"<{tag_name}")
        for attr_name, attr_value in element.attrs.items():
            text_output.insert(tk.END, f" {attr_name}='{attr_value}'")
        text_output.insert(tk.END, '>\n')

        qr_code_path = generate_qr_code(tag_name, coordinates, url)
        qr_output.insert(tk.END, f"QR Code: {qr_code_path}\n")

        resized_path = resize_qr_image(qr_code_path, (50, 50))  # Adjust the size as per your requirement

        image = tk.PhotoImage(file=resized_path)
        qr_label = tk.Label(qr_window, image=image)
        qr_label.image = image

        # Compute grid row and column based on coordinates
        row, col = coordinates[0], coordinates[1]
        qr_label.grid(row=row, column=col, padx=5, pady=5)

        for child in element.children:
            if child.name:
                coordinate_tracker.update()
                render_dom(child, url, coordinate_tracker, text_output, qr_output, qr_window)

        text_output.insert(tk.END, f"</{tag_name}>\n")
        coordinate_tracker.update()

# Event handler for "Fetch" button
def fetch_page():
    url = url_entry.get()
    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    coordinate_tracker = CoordinateTracker()

    # Create a new window for displaying QR codes
    qr_window = tk.Toplevel(window)
    qr_window.title("QR Codes")

    render_dom(soup, url, coordinate_tracker, text_output, qr_output, qr_window)

# Event handler for "Export" button
def export_html():
    html = text_output.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html")])

    if file_path:
        with open(file_path, "w") as file:
            file.write(html)

# Coordinate tracker class
class CoordinateTracker:
    def __init__(self):
        self.coordinates = [0, 0]

    def get_coordinates(self):
        return self.coordinates.copy()

    def update(self):
        self.coordinates[1] += 1

    def __enter__(self):
        self.coordinates[0] += 1
        self.coordinates[1] = 0

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

# Create the main window
window = tk.Tk()
window.title("Dom Browser/Indexer")

# Create the URL input section
url_frame = tk.Frame(window)
url_frame.pack(pady=10)

url_label = tk.Label(url_frame, text="URL:")
url_label.pack(side=tk.LEFT)

url_entry = tk.Entry(url_frame, width=80)
url_entry.pack(side=tk.LEFT)

# Set the default URL value
url_entry.insert(0, "https://example.com")

fetch_button = tk.Button(window, text="Fetch", command=fetch_page)
fetch_button.pack(pady=10)

# Create the text output section
text_frame = tk.Frame(window)
text_frame.pack(padx=10, pady=10)

text_label = tk.Label(text_frame, text="DOM Structure:")
text_label.pack()

text_output = tk.Text(text_frame, width=80, height=25)
text_output.pack()

# Create the QR code output section
qr_frame = tk.Frame(window)
qr_frame.pack(padx=10, pady=10)

qr_label = tk.Label(qr_frame, text="QR Code DOM Index:")
qr_label.pack()

qr_output = tk.Text(qr_frame, width=80, height=5)
qr_output.pack()

# Create the export button
export_button = tk.Button(window, text="Export HTML", command=export_html)
export_button.pack(pady=10)

# Start the GUI event loop
window.mainloop()
