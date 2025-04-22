import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Function to download a PDF
def download_pdf(url, folder):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        filename = os.path.join(folder, url.split('/')[-1])

        # Save the PDF to the specified folder
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")

# Function to scrape and find all PDF links on a webpage
def get_pdf_links(url):
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links with the 'href' attribute containing '.pdf'
    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.lower().endswith('.pdf'):
            # Handle relative URLs by converting them to absolute URLs
            if href.startswith('http'):
                pdf_links.append(href)
            else:
                pdf_links.append(url + href)
    
    return pdf_links

# Main function to scrape and download PDFs
def download_all_pdfs(webpage_url, folder='downloads'):
    # Create a folder to save PDFs if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Get all PDF links from the webpage
    pdf_links = get_pdf_links(webpage_url)
    print(f"Found {len(pdf_links)} PDF links.")

    # Use ThreadPoolExecutor to download PDFs concurrently
    with ThreadPoolExecutor() as executor:
        for pdf_url in pdf_links:
            executor.submit(download_pdf, pdf_url, folder)

# Example usage
webpage_url = 'http://example.com'  # Replace with the webpage URL
download_all_pdfs(webpage_url)
