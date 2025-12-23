import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF
import os

def select_files():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(initialdir='.', title='Select PDF files', filetypes=[("PDF Files", "*.pdf")])
    return list(file_paths)

def convert_pages_to_images(pdf_path, output_folder, dpi=200):
    os.makedirs(output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)
    for page_number in range(len(doc)):
        page = doc[page_number]        
        mat = fitz.Matrix(dpi / 72, dpi / 72)  # 72 is PDF native dpi
        pix = page.get_pixmap(matrix=mat)
        img_path = os.path.join(output_folder, f"page{page_number+1}.png")
        pix.save(img_path)
    return f"All {len(doc)} pages saved to {output_folder}"

# Select PDF files
selected_files = select_files()

for pdf_file_path in selected_files:
    output_dir = os.path.join("page_images", os.path.splitext(os.path.basename(pdf_file_path))[0])
    print(convert_pages_to_images(pdf_file_path, output_dir))
