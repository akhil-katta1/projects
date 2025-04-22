import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import hashlib
from PyPDF2 import PdfReader

# Define target URL and folder to save PDFs in Lakehouse
target_url = "https://mcsc.state.mi.us/MCSCJobSpecifications/JobSpecMain.aspx"
lakehouse_target_folder = f"{secret_1}@onelake.dfs.fabric.microsoft.com/{secret_2}/Files/Market Data Files/State of Michigan/pdfs"

# Define a browser-like header
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36"
}

# Function to calculate a hash of a PDF file's content (for duplicate detection)
def calculate_pdf_hash(file_path):
    """Calculate SHA-256 hash of a PDF file's content."""
    try:
        with open(file_path, 'rb') as f:
            pdf_content = f.read()
            return hashlib.sha256(pdf_content).hexdigest()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

# Function to extract and normalize text from a PDF for duplicate checking
def extract_and_normalize_text(file_path):
    """Extract text from PDF and normalize (remove extra spaces, line breaks)."""
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

        # Normalize text by removing extra spaces and line breaks
        normalized_text = " ".join(text.split())
        return normalized_text
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

# Function to download a single PDF and save it
def download_single_pdf_to_lakehouse(pdf_url, lakehouse_folder, idx, downloaded_hashes):
    file_name = os.path.basename(pdf_url)
    file_path = os.path.join(lakehouse_folder, file_name)

    try:
        # Fetch the PDF file using browser headers
        response = requests.get(pdf_url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        # Save the PDF directly to Lakehouse
        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f"{idx}. Downloaded to Lakehouse: {file_name}")

        # After downloading, calculate the hash of the PDF
        pdf_hash = calculate_pdf_hash(file_path)
        if pdf_hash:
            if pdf_hash in downloaded_hashes:
                print(f"Duplicate found: {file_name}")
            else:
                downloaded_hashes.add(pdf_hash)

    except Exception as e:
        print(f"{idx}. Failed to download {pdf_url}: {e}")

# Main function to download multiple PDFs with threading
def download_pdfs_to_lakehouse(url, lakehouse_folder="/lakehouse/default/Files/PDF_Downloads", max_workers=8):
    os.makedirs(lakehouse_folder, exist_ok=True)

    try:
        # Get the webpage content using browser headers
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching webpage: {e}")
        return

    # Parse the page to find all PDF links
    soup = BeautifulSoup(response.text, "html.parser")
    pdf_links = [urljoin(url, link['href']) for link in soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))]

    print(f"Found {len(pdf_links)} PDF files. Starting downloads with {max_workers} threads...")

    # Set to store hashes of downloaded files (for duplicate detection)
    downloaded_hashes = set()

    # Download PDFs concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for idx, pdf_url in enumerate(pdf_links, start=1):
            executor.submit(download_single_pdf_to_lakehouse, pdf_url, lakehouse_folder, idx, downloaded_hashes)

# Run the function to download PDFs and detect duplicates
download_pdfs_to_lakehouse(target_url)
