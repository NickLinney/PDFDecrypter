#!/usr/bin/env python3
import os
import glob
from PyPDF2 import PdfReader, PdfWriter

INPUT_DIR = "./data"
OUTPUT_DIR = "./processed"

def strip_owner_password(input_path: str, output_path: str) -> None:
    reader = PdfReader(input_path)
    if reader.is_encrypted:
        try:
            # Try to decrypt with an empty password
            reader.decrypt("")
        except Exception:
            print(f"ERROR: Could not decrypt (owner password needed): {input_path}")
            return

    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    # Write a new PDF with no encryption (permissions dropped)
    with open(output_path, "wb") as out_f:
        writer.write(out_f)

def main():
    # Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not os.path.isdir(INPUT_DIR):
        print(f"ERROR: Input directory not found: {INPUT_DIR}")
        return

    pattern = os.path.join(INPUT_DIR, "*.pdf")
    for fullpath in glob.glob(pattern):
        filename = os.path.basename(fullpath)
        output_path = os.path.join(OUTPUT_DIR, filename)

        if os.path.exists(output_path):
            print(f"Skipping (already processed): {filename}")
            continue

        print(f"Processing: {filename} → {os.path.join('processed', filename)}")
        strip_owner_password(fullpath, output_path)

if __name__ == "__main__":
    main()
