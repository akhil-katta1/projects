# Install required libraries in Fabric Notebook first (only once)
# Fabric usually has requests and bs4 preinstalled
# If not, you can use:
# %pip install requests beautifulsoup4

import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Fabric specific: Mount Lakehouse Files path
lakehouse_files_path = "/lakehouse/default/Files/pdfs/"  # Save PDFs inside this path

# Create directory if not exists
dbutils.fs.mkdirs(lakehouse_files_path)  # dbutils is available in Fabric notebooks

# Function to download and save a single PDF into Lakehouse
def download_single_pdf_to_lakehouse(pdf_url, idx):
    file_name = os.path.basename(pdf_url)
    lakehouse_full_path = lakehouse_files_path + file_name

    try:
        # Download the PDF
        response = requests.get(pdf_url, timeout=10)
        response.raise_for_status()

        # Upload directly into Lakehouse Files
        with open(f"/tmp/{file_name}", "wb") as f:
            f.write(response.content)
        
        dbutils.fs.cp(f"file:/tmp/{file_name}", f"abfss:{lakehouse_full_path}")

        print(f"{idx}. Uploaded: {file_name}")
    except Exception as e:
        print(f"{idx}. Failed to download {pdf_url}: {e}")

# Main function to parse the webpage and download multiple PDFs
def download_pdfs_from_webpage_to_lakehouse(url, max_workers=8):
    try:
        # Fetch the webpage
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching webpage: {e}")
        return

    # Parse HTML to find PDF links
    soup = BeautifulSoup(response.text, "html.parser")
    pdf_links = [urljoin(url, link['href']) for link in soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))]

    print(f"Found {len(pdf_links)} PDFs. Downloading with {max_workers} threads...")

    # Use multithreading for faster downloads
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for idx, pdf_url in enumerate(pdf_links, start=1):
            executor.submit(download_single_pdf_to_lakehouse, pdf_url, idx)

# MAIN execution
if _name_ == "_main_":
    target_url = "https://www.icai.org/post.html?post_id=17843"  # Change this URL if needed
    download_pdfs_from_webpage_to_lakehouse(target_url, max_workers=8)
