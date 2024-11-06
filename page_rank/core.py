import numpy as np


# The page rank algorthim
# Is expecting an adjacency matrix (np array) of weights of links
def page_rank(M, d: float = 0.85):
	N = M.shape[1]
	w = np.ones(N) / N
	M_hat = d * M
	v = M_hat @ w + (1 - d)
	while (np.linalg.norm(w - v) >= 1e-10):
		w = v
		v = M_hat @ w + (1 - d)
	return v
