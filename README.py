import os
import hashlib
from PyPDF2 import PdfReader

# Function to extract text from PDF and normalize it
def extract_and_normalize_text(file_path):
    """Extract text from PDF and normalize (remove extra spaces, line breaks)."""
    try:
        with open(file_path, 'rb') as file:
            pdf = PdfReader(file)
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        # Normalize text by removing extra spaces and line breaks
        normalized_text = " ".join(text.split())
        return normalized_text
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

# Function to compare and find duplicate PDFs based on text content
def find_duplicates_by_text(folder_path="/tmp/pdfs/"):
    text_hash_to_files = {}

    # Scan through all PDFs
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".pdf"):
            full_path = os.path.join(folder_path, file_name)
            normalized_text = extract_and_normalize_text(full_path)

            if normalized_text:
                # Calculate a hash of the normalized text
                text_hash = hashlib.sha256(normalized_text.encode('utf-8')).hexdigest()

                # Group files by normalized text hash
                if text_hash not in text_hash_to_files:
                    text_hash_to_files[text_hash] = []
                text_hash_to_files[text_hash].append(file_name)

    # Find duplicates based on normalized text
    print("🔎 Checking for duplicate PDFs by normalized text...\n")
    duplicates = {h: f for h, f in text_hash_to_files.items() if len(f) > 1}
    if duplicates:
        for hash_val, files in duplicates.items():
            print(f"✅ Duplicate text found in files: {files}")
    else:
        print("❌ No text-based duplicate PDFs found.")

# Run it
find_duplicates_by_text("/path/to/your/pdf/folder")
