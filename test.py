import numpy as np

from page_rank import page_rank
from page_rank import fix_cols

from scraper import get_graph_and_index

"""
M = np.array([[0, 0, 0, 0],
              [0, 0, 0, 0],
              [1, 1, 0, 0],
              [0, 1, 1, 0]])
"""
"""
M = np.array([[0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0],
              [0, 0, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 1, 0]])
"""

M, index = get_graph_and_index(["https://versel.info"], 1)

N = fix_cols(M)
print(N)
v = page_rank(N, 0.85)

print(v)

print("Out:")
for url, i in index.items():
	print(f"{url}: {v[i]}")
