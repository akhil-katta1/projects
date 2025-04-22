# Import necessary libraries
import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Function to download a single PDF and save directly into Lakehouse
def download_single_pdf_to_lakehouse(pdf_url, lakehouse_folder, idx):
    # Get the file name from the URL
    file_name = os.path.basename(pdf_url)
    file_path = os.path.join(lakehouse_folder, file_name)

    try:
        # Fetch the PDF file
        response = requests.get(pdf_url, timeout=10)
        response.raise_for_status()

        # Save the PDF directly to Lakehouse
        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f"{idx}. Downloaded to Lakehouse: {file_name}")
    except Exception as e:
        print(f"{idx}. Failed to download {pdf_url}: {e}")

# Main function to download multiple PDFs with threading
def download_pdfs_to_lakehouse(url, lakehouse_folder="/lakehouse/default/Files/PDF_Downloads", max_workers=8):
    # Ensure the Lakehouse folder exists
    os.makedirs(lakehouse_folder, exist_ok=True)

    try:
        # Get the webpage content
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching webpage: {e}")
        return

    # Parse the page to find all PDF links
    soup = BeautifulSoup(response.text, "html.parser")
    pdf_links = [urljoin(url, link['href']) for link in soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))]

    print(f"Found {len(pdf_links)} PDF files. Starting downloads with {max_workers} threads...")

    # Use ThreadPoolExecutor for fast downloading
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for idx, pdf_url in enumerate(pdf_links, start=1):
            executor.submit(download_single_pdf_to_lakehouse, pdf_url, lakehouse_folder, idx)

# Main execution
if _name_ == "_main_":
    # Set the target webpage URL here
    target_url = "https://www.icai.org/post.html?post_id=17843"
    
    # Folder inside Lakehouse where PDFs will be saved
    lakehouse_target_folder = "/lakehouse/default/Files/PDF_Downloads"

    # Start the download process
    download_pdfs_to_lakehouse(target_url, lakehouse_target_folder)
