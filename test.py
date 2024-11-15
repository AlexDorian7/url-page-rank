import numpy as np

from page_rank import page_rank
from page_rank import fix_cols

M = np.array([[0, 0, 0, 0],
              [0, 0, 0, 0],
              [1, 1, 0, 0],
              [0, 1, 1, 0]])

"""
M = np.array([[0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0],
              [0, 0, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 1, 0]])
"""
N = fix_cols(M)
print(N)
v = page_rank(N, 0.85)

print(v)
