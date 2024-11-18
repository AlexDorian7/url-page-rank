import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
from scipy.sparse import lil_matrix
import numpy as np

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
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]

        # Normalize and convert links to absolute URLs
        absolute_links = {
            normalize_url(urljoin(url, link)) for link in links
        }

        return list(absolute_links)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

def build_graph(urls, current, max_depth, url_index, adj_matrix, visited):
    """
    Recursively build the graph by exploring links up to max_depth.
    """
    for url in urls:
        normalized_url = normalize_url(url)

        # Skip already visited pages
        if normalized_url in visited:
            continue

        # Mark this page as visited
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
            adj_matrix[link_idx, url_idx] = 1  # Mark the link from `link` to `url`

        print(f"{normalized_url}: {len(links)} links found.")

        # Recurse deeper if the depth limit hasn't been reached
        if current < max_depth:
            build_graph(links, current + 1, max_depth, url_index, adj_matrix, visited)

def get_adjacency_matrix(start_urls, max_depth):
    """
    Create the adjacency matrix for the graph starting from the given URLs.
    """
    url_index = {}  # Map each URL to a unique index
    adj_matrix = lil_matrix((100000, 100000), dtype=int)  # Initialize a sparse matrix
    visited = set()  # Track visited pages

    build_graph(start_urls, 0, max_depth, url_index, adj_matrix, visited)

    # Resize the sparse matrix to fit the number of unique URLs
    size = len(url_index)
    adj_matrix = adj_matrix[:size, :size]

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

