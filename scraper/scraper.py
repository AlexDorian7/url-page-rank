import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
from scipy.sparse import lil_matrix
import numpy as np
from tqdm import tqdm  # Progress bar
import time  # Timer
import os
import platform

def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")  # For Windows
    else:
        os.system("clear")  # For macOS and Linux

def normalize_url(url):
    """
    Normalize a URL by:
    - Removing fragments (#...)
    - Removing trailing slashes
    - Ignoring query parameters
    """
    parsed = urlparse(url)
    # Remove fragment and query
    normalized = parsed._replace(fragment='', query='')
    # Rebuild the URL and strip trailing slashes
    return urlunparse(normalized).rstrip('/')

def get_links(url):
    """
    Fetch links from a webpage, normalize them, and return them as a list.
    """
    headers = {
        'User-Agent': 'PageRankAlgorithmParser/1.0'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]

        # Normalize and convert links to absolute URLs
        absolute_links = {
            normalize_url(urljoin(url, link)) for link in links
        }

        return list(absolute_links)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL {url}: {e}")
        print("Skipping Link. Continuing...")
        return []

def build_graph(start_url, max_depth, url_index, adj_matrix, visited, progress_bar):
    """
    Recursively build the graph by exploring links up to max_depth.
    """
    to_visit = [(start_url, 0)]  # Initialize with the start URL and depth 0

    while to_visit:
        current_url, depth = to_visit.pop(0)
        normalized_url = normalize_url(current_url)

        if normalized_url in visited:
            progress_bar.update(1)
            continue

        # Mark the page as visited
        visited.add(normalized_url)

        # Add URL to index if not already present
        if normalized_url not in url_index:
            url_index[normalized_url] = len(url_index)

        url_idx = url_index[normalized_url]
        links = get_links(normalized_url)

        for link in links:
            normalized_link = normalize_url(link)

            # Skip self-links
            if normalized_link == normalized_url:
                continue

            # Add link to index if not already present
            if normalized_link not in url_index:
                url_index[normalized_link] = len(url_index)

            link_idx = url_index[normalized_link]
            adj_matrix[link_idx, url_idx] = 1  # Mark the link from `url` to `link`

            # Add to the queue if within depth limit
            if normalized_link not in visited and depth + 1 <= max_depth:
                to_visit.append((normalized_link, depth + 1))
                progress_bar.total += 1

        clear_terminal()
        print(f"{normalized_url}: {len(links)} links found.")
        progress_bar.update(1)

def get_adjacency_matrix(start_urls, max_depth):
    """
    Create the adjacency matrix for the graph starting from the given URLs.
    """
    start_time = time.time()  # Start timer

    url_index = {}  # Map each URL to a unique index
    adj_matrix = lil_matrix((1000000, 1000000), dtype=int)  # Initialize a sparse matrix
    visited = set()  # Track visited pages

    with tqdm(total=1, desc="Progress", unit="site", dynamic_ncols=True) as progress_bar:
        for url in start_urls:
            normalized_url = normalize_url(url)
            if normalized_url not in visited:
                #visited.add(normalized_url)
                build_graph(url, max_depth, url_index, adj_matrix, visited, progress_bar)

    end_time = time.time()  # End timer
    elapsed_time = end_time - start_time

    # Resize the sparse matrix to fit the number of unique URLs
    size = len(url_index)
    adj_matrix = adj_matrix[:size, :size]

    print(f"\nTotal time taken: {elapsed_time:.2f} seconds")
    return adj_matrix, url_index

# Example usage
if __name__ == "__main__":
    start_urls = ["https://example.com"]
    max_depth = 2
    adj_matrix, url_index = get_adjacency_matrix(start_urls, max_depth)

    print("Adjacency Matrix (Sparse Format):")
    print(adj_matrix)

    print("\nURL Index:")
    for url, index in url_index.items():
        print(f"{index}: {url}")

