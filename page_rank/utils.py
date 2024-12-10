import numpy as np
from scipy.sparse import csc_matrix
from tqdm import tqdm  # For the progress bar

# Normalize columns of a sparse matrix
def fix_cols(M):
    """
    Normalize columns of a sparse matrix so that each column sums to 1.
    
    Parameters:
        M (scipy.sparse.csc_matrix): Sparse matrix to normalize.

    Returns:
        scipy.sparse.csc_matrix: Column-normalized sparse matrix.
    """
    if not isinstance(M, csc_matrix):
        M = csc_matrix(M)  # Convert to Compressed Sparse Column format for efficient column operations

    # Ensure the matrix data is float for division operations
    if M.dtype != np.float64:
        M = M.astype(np.float64)

    J = M.shape[1]  # Number of columns
    col_sums = np.array(M.sum(axis=0)).flatten()  # Compute column sums

    with tqdm(total=J, desc="ColFix Progress", unit="Cols") as pbar:
        for j in range(J):
            if col_sums[j] != 0:  # Avoid division by zero
                M.data[M.indptr[j]:M.indptr[j+1]] /= col_sums[j]  # Normalize column `j`
            pbar.update(1)
    
    return M

