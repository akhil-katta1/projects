#!/usr/bin/env python
# coding: utf-8

# Import required libraries
import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from azure.storage.filedatalake import DataLakeServiceClient
from io import BytesIO

# Function to download and upload a single PDF to Azure Data Lake (Lakehouse)
def download_and_upload_single_pdf(pdf_url, download_folder, idx, file_system_client, directory_name):
    file_name = os.path.basename(pdf_url)
    file_path = os.path.join(download_folder, file_name)

    try:
        # Download the PDF file
        response = requests.get(pdf_url, timeout=10)
        response.raise_for_status()

        # Upload PDF directly to Azure Data Lake (Lakehouse)
        file_client = file_system_client.get_file_client(f"{directory_name}/{file_name}")
        file_client.append_data(data=response.content, offset=0, length=len(response.content))
        file_client.flush_data(len(response.content))

        print(f"{idx}. Uploaded to Data Lake: {file_name}")
    except Exception as e:
        print(f"{idx}. Failed to download and upload {pdf_url}: {e}")

# Main function to find and download multiple PDFs using threads, then upload to Data Lake
def download_pdfs_with_threads_and_upload_to_datalake(url, download_folder="PDF_Downloads", max_workers=8, directory_name="pdfcontainer", connection_string="YOUR_AZURE_CONNECTION_STRING"):
    # Create download folder if it doesn't exist (for temporary storage)
    os.makedirs(download_folder, exist_ok=True)

    # Initialize the DataLakeServiceClient
    service_client = DataLakeServiceClient.from_connection_string(connection_string)
    file_system_client = service_client.get_file_system_client(file_system="YOUR_FILE_SYSTEM_NAME")

    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching the page: {e}")
        return

    # Parse the webpage HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all <a> links ending with .pdf
    pdf_links = [urljoin(url, link['href']) for link in soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))]

    print(f"Found {len(pdf_links)} PDF files. Starting downloads with {max_workers} threads...")

    # Use ThreadPoolExecutor to download PDFs concurrently and upload to Data Lake
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for idx, pdf_url in enumerate(pdf_links, start=1):
            executor.submit(download_and_upload_single_pdf, pdf_url, download_folder, idx, file_system_client, directory_name)

# Main execution starts here
if _name_ == "_main_":
    target_url = "https://www.icai.org/post.html?post_id=17843"  # Change the URL as needed
    download_pdfs_with_threads_and_upload_to_datalake(target_url, directory_name="pdfcontainer", connection_string="YOUR_AZURE_CONNECTION_STRING")
