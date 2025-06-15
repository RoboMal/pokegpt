import pandas as pd
from parser import extract_query_components
from filter_data import filter_data

pokedex = pd.read_csv("data/pokedex.csv")

query = "LIST ALL POSION TYPES WITH 50 OR LESS ATACK"
parsed = extract_query_components(query)

print(parsed)

filtered = filter_data(pokedex, parsed)
print(filtered)