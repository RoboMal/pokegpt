import pandas as pd
from parser import extract_query_components
from filter_data import filter_data

def parse_type_field(x):
    '''
    The type column in the dataset is a string that looks like a list.
    This function helps convert it into an actual Python list to assist with parsing.
    (Remember to move this function to a utility module (data_utils.py) later)
    '''
    if isinstance(x, str) and x.startswith("{") and x.endswith("}"):
        inner = x[1:-1]
        return [t.strip().lower() for t in inner.split(",") if t.strip()]
    return []

pokedex = pd.read_csv("data/pokedex.csv")
pokedex["type"] = pokedex["type"].apply(parse_type_field)

print(pokedex["type"].head(10))
query = "LIST ALL POSION TYPES WITH 50 OR LESS ATACK"
parsed = extract_query_components(query)
print(f"Parsed Query:\n{parsed}")

filtered = filter_data(pokedex, parsed)
print(f"Filtered Query:\n{filtered}")