import os
import hashlib

def calculate_file_hash(file_path):
    """Calculate SHA256 hash of the file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):  # read in chunks
            sha256.update(chunk)
    return sha256.hexdigest()

def find_duplicate_pdfs(folder_path="/tmp/pdfs/"):
    # Dictionary to hold hash → list of files
    hash_dict = {}

    # Loop through all PDFs in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".pdf"):
            full_path = os.path.join(folder_path, file_name)
            file_hash = calculate_file_hash(full_path)

            if file_hash in hash_dict:
                hash_dict[file_hash].append(file_name)
            else:
                hash_dict[file_hash] = [file_name]

    # Find duplicates
    duplicates = {hash_val: files for hash_val, files in hash_dict.items() if len(files) > 1}

    if duplicates:
        print("Duplicate PDFs found:")
        for hash_val, files in duplicates.items():
            print(f"Files with same content ({len(files)} copies): {files}")
    else:
        print("No duplicate PDFs found!")

# Run the function
find_duplicate_pdfs("/tmp/pdfs/")
