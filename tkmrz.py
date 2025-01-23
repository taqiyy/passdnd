import json
import pyperclip
from datetime import datetime
from fastmrz import FastMRZ
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD

# Function to calculate age from birth date
def calculate_age(birth_date):
    birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
    today = datetime.now()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

# Function to convert gender to Indonesian format
def convert_gender(gender):
    return "P" if gender == "F" else "L"

# Function to format date to dd-mm-yyyy
def format_date(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return date.strftime("%d-%m-%Y")

# Function to handle drag-and-drop event
def on_drop(event):
    file_path = event.data.strip()
    if file_path.startswith("{") and file_path.endswith("}"):
        file_path = file_path[1:-1]
    process_file(file_path)

# Function to process the dropped file
def process_file(file_path):
    fast_mrz = FastMRZ()

    # Extract MRZ details and format them as JSON
    passport_mrz_json = fast_mrz.get_details(file_path, include_checkdigit=False)

    # Extract necessary fields
    full_name = f"{passport_mrz_json['given_name']} {passport_mrz_json['surname']}"
    sex = convert_gender(passport_mrz_json['sex'])
    birth_date = format_date(passport_mrz_json['birth_date'])
    age = calculate_age(passport_mrz_json['birth_date'])
    passport_number = passport_mrz_json['document_number']
    expiry_date = format_date(passport_mrz_json['expiry_date'])
    issuer_code = passport_mrz_json['issuer_code']  # negara
    # maybe I need a trained OCR model (;_;)
    issuing_office = "kantor imigrasi" # MRZ data typically doesn't include this; update if you know
    issue_date = "tanggal terbit"  # MRZ data typically doesn't include this; update if you know
    place_of_birth = "tempat lahir"  # MRZ data typically doesn't include this; update if you know

    # Format the output
    formatted_output = (
        f"{full_name}\t{sex}\t{place_of_birth}\t{birth_date}\t{age}\t"
        f"{passport_number}\t{issue_date}\t{expiry_date}\t{issuing_office}"
    )

    # Copy formatted result to clipboard
    pyperclip.copy(formatted_output)
    print("Formatted Output:")
    print(formatted_output)
    print("\nCopied formatted output to clipboard.\n")

# Set up GUI for drag-and-drop
root = TkinterDnD.Tk()
root.title("Drag and Drop Passport Image")
root.geometry("600x200")

label = tk.Label(root, text="Drag and drop a passport image file here.", font=("Arial", 14))
label.pack(pady=50)

# Enable drag-and-drop functionality
root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", on_drop)

# Run the Tkinter event loop
root.mainloop()
