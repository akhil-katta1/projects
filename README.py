# Import necessary libraries
import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor




target_url = "https://mcsc.state.mi.us/MCSCJobSpecifications/JobSpecMain.aspx"
    
    # Folder inside Lakehouse where PDFs will be saved
lakehouse_target_folder = f"{secret_1}@onelake.dfs.fabric.microsoft.com/{secret_2}/Files/Market Data Files/State of Michigan/pdfs"


# Define a browser-like header
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36"
}

# Function to download a single PDF and save directly into Lakehouse
def download_single_pdf_to_lakehouse(pdf_url, lakehouse_folder, idx):
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

    # Download PDFs concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for idx, pdf_url in enumerate(pdf_links, start=1):
            executor.submit(download_single_pdf_to_lakehouse, pdf_url, lakehouse_folder, idx)

# Main execution

download_pdfs_to_lakehouse(target_url, lakehouse_target_folder)



# Step 1: Download PDFs into /tmp/pdfs folder (local in Fabric Notebook)

# Folder inside temporary notebook filesystem
local_temp_folder = "/tmp/pdfs"

os.makedirs(local_temp_folder, exist_ok=True)

download_pdfs_to_lakehouse(target_url, local_temp_folder)



# Step 2: Move the downloaded files to Lakehouse
import shutil

lakehouse_folder_path = f"Files/Market Data Files/State of Michigan/pdfs"

# List files in /tmp/pdfs
for file_name in os.listdir(local_temp_folder):
    local_file_path = os.path.join(local_temp_folder, file_name)
    
    # Final destination inside Lakehouse
    lakehouse_full_path = os.path.join(lakehouse_folder_path, file_name)
    
    # Save file to Lakehouse using Fabric built-in APIs
    shutil.copy(local_file_path, f"/lakehouse/default/{lakehouse_full_path}")
    
    print(f"Uploaded {file_name} to Lakehouse: {lakehouse_full_path}")
