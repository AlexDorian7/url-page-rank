import numpy as np

# replace cols with values that sum to 1
def fix_cols(M):

	# Ensure M is a float array to avoid integer division
	M = M.astype(float)

	I,J = M.shape  # Get dimensions of the matrix

	"""
	print('Initial Adj matrix:')
	for i in range(I):
		print('[', end='')
		for j in range(J):
			print(M[i][j], " ", end="");
		print(']');
	print()
	"""


	for j in range(J):  # Iterate over each column
		total = np.sum(M[:, j])  # Sum of the current column
		# print("total 1's in col: ", total)

		if total != 0:  # Avoid division by zero
			M[:, j] = M[:, j]/ total # Normalize each element in the column
			# print out modify matrix
			"""
			print("After normalization")
			for row in range(I):
				print('[', end='')
				for col in range(J):
					print(M[row][col], " ", end='');
				print(']');
			"""
		# print()
	return M
