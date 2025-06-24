import pandas as pd

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

def load_and_clean_pokedex(filepath):
    '''
    Loads the Pokedex CSV and applies preprocessing
    '''
    df = pd.read_csv("data/pokedex.csv")
    df["type"] = df["type"].apply(parse_type_field)
    return df