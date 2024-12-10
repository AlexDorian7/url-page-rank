import numpy as np

from page_rank import page_rank
from page_rank import fix_cols

from scraper import get_graph_and_index

from visualize import save_to_file

def prompt_positive_integer():
	while True:
		try:
			# Prompt the user for input
			user_input = int(input("Enter a depth amount: "))

			# Check if the input is positive
			if user_input >= 0:
				return user_input
			else:
				print("The number must be a positive integer. Please try again.")
		except ValueError:
			# Handle cases where the input is not an integer
			print("Invalid input. Please enter a valid integer.")



M, index = get_graph_and_index([input("Please enter the starting URL (e.g. https://example.com): ")], prompt_positive_integer())
print("Calculating Page Rank...")

N = fix_cols(M)
# print(N)
v = page_rank(N, 0.85)

# print(v)

print("")
print("Out:")
for url, i in index.items():
	print(f"{url}: {v[i]}")
print("")

save = input("Would you like to save this data to a csv file? (Y/N): ")
if save == "Y" or save == "y":
	save_to_file(index,v)
