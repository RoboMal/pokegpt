from parser import extract_query_components
from filter_data import filter_data
from data_utils import load_and_clean_pokedex

pokedex = load_and_clean_pokedex("data/pokedex.csv")

query = "LIST ALL POSION TYPES WITH 50 OR LESS ATACK"
parsed = extract_query_components(query)
print(f"Parsed Query:\n{parsed}")

filtered = filter_data(pokedex, parsed)
print(f"Filtered Query:\n{filtered}")