import os

def compare_files(file1, file2):
    """Compare two PDF files byte by byte."""
    try:
        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
            file1_bytes = f1.read()
            file2_bytes = f2.read()
            return file1_bytes == file2_bytes  # Return True if identical, False otherwise
    except Exception as e:
        print(f"Error comparing {file1} and {file2}: {e}")
        return False

def find_duplicates_by_bytes(folder_path="/tmp/pdfs/"):
    files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
    duplicates = []

    # Compare each pair of files
    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            file1 = os.path.join(folder_path, files[i])
            file2 = os.path.join(folder_path, files[j])
            if compare_files(file1, file2):
                # If the files are identical, store them as duplicates
                duplicates.append((files[i], files[j]))

    if duplicates:
        print("✅ Duplicate files found:")
        for duplicate in duplicates:
            print(f"Duplicate pair: {duplicate[0]} and {duplicate[1]}")
    else:
        print("❌ No duplicate PDFs found.")

# Run it on the folder containing your 609 PDFs
find_duplicates_by_bytes("/path/to/your/pdf/folder")
