from .scraper import get_adjacency_matrix

def get_graph_and_index(links = ["https://example.com"], depth = 0):
	return get_adjacency_matrix(links, depth)
