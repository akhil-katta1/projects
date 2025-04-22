import os
import hashlib
import fitz  # PyMuPDF

def calculate_text_hash(file_path):
    """Extract text from PDF and calculate a hash."""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text()
        text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        return text_hash
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def find_duplicates_by_text(folder_path="/tmp/pdfs/"):
    text_hash_to_files = {}
    name_to_text_hash = {}

    # Scan through all PDFs
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".pdf"):
            full_path = os.path.join(folder_path, file_name)
            text_hash = calculate_text_hash(full_path)

            if text_hash:
                # Group files by extracted text hash
                if text_hash not in text_hash_to_files:
                    text_hash_to_files[text_hash] = []
                text_hash_to_files[text_hash].append(file_name)

                # Track if files with the same name have different text
                if file_name not in name_to_text_hash:
                    name_to_text_hash[file_name] = []
                name_to_text_hash[file_name].append(text_hash)

    # Find duplicates based on text
    print("🔎 Checking for duplicate PDFs by extracted text...\n")
    duplicates = {h: f for h, f in text_hash_to_files.items() if len(f) > 1}
    if duplicates:
        for hash_val, files in duplicates.items():
            print(f"✅ Duplicate text found in files: {files}")
    else:
        print("❌ No text-based duplicate PDFs found.")

    # Find same-name but different text
    print("\n🔎 Checking for files with same name but different text...\n")
    same_name_diff_text = {n: h for n, h in name_to_text_hash.items() if len(set(h)) > 1}
    if same_name_diff_text:
        for name, hashes in same_name_diff_text.items():
            print(f"⚠ File name '{name}' has different textual contents!")
    else:
        print("✅ No files with the same name and different text.")

# Run it
find_duplicates_by_text("/tmp/pdfs/")
