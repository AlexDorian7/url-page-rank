def save_to_file(index, v):
	# Prompt the user for the file name
	file_name = input("Enter the file name to save to (e.g., output.csv): ")

	try:
		# Open the file in write mode ('w')
		with open(file_name, 'w') as file:
			file.write('"URL","Rank"\n')
			for url, i in index.items():
				safe = url.replace('"', '\\"')
				file.write(f'"{safe}","{v[i]}"\n')
		print(f"Data successfully saved to {file_name}")
	except Exception as e:
		print(f"An error occurred while saving the file: {e}")
