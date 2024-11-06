import numpy as np

# replace cols with values that sum to 1
import numpy as np

def fix_cols(M):
	I, J = M.shape  # Get dimensions of the matrix

	for j in range(J):  # Iterate over each column
		total = np.sum(M[:, j])  # Sum of the current column
		print(total)
		if total != 0:  # Avoid division by zero
			print(M[:, j])
			M[:, j] = M[:, j] / total  # Normalize each element in the column
			print(M[:, j])
	return M
