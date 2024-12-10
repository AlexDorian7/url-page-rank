import numpy as np
from tqdm import tqdm  # For the progress bar

# The PageRank algorithm
# Expects an adjacency matrix (np array) of weights of links
def page_rank(M, d: float = 0.85, max_iter: int = 1000):
    """
    Compute PageRank scores.
    
    Parameters:
        M (np.ndarray): Adjacency matrix representing the link structure.
        d (float): Damping factor (default: 0.85).
        max_iter (int): Maximum number of iterations (default: 1000).
    
    Returns:
        np.ndarray: PageRank scores.
    """
    N = M.shape[1]
    w = np.ones(N) / N  # Initial rank vector
    M_hat = d * M       # Weighted adjacency matrix
    v = M_hat @ w + (1 - d)

    with tqdm(total=max_iter, desc="PageRank Progress", unit="iteration") as pbar:
        #pbar.update(0)
        for _ in range(max_iter):
            if np.linalg.norm(w - v) < 1e-10:  # Convergence check
                break
            w = v
            v = M_hat @ w + (1 - d)
            pbar.update(1)
    
    return v
