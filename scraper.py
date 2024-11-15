import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_links(url):
    headers = {
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
        'User-Agent': 'PageRankAlgorthimParser/1.0'
    }

    try:
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for request errors

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <a> tags and extract href attributes
        links = [a['href'] for a in soup.find_all('a', href=True)]

        # Convert relative URLs to absolute URLs and remove GET parameters
        absolute_links = {
            urlparse(urljoin(url, link))._replace(query='').geturl() for link in links
        }

        return list(absolute_links)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return set()

def recurse(urls, current, max_depth):
    for url in urls:
        hrefs = []
        hrefs = get_links(url)
        print(f"{url}: {len(hrefs)} links found.")
        if current < max_depth:
            recurse(hrefs, current + 1, max_depth)

# Example usage
recurse(["https://akoolkev.github.io/Erika-Portfolio"], 0, 2)

