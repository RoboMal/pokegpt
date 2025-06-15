import spacy as sp
import re
from rapidfuzz import process

nlp = sp.load("en_core_web_sm")

# <potential user inputs> : <actual column name>
POKE_STATS = {
    "hp": "hp",
    "attack": "attack",
    "defense": "defense",
    "sp. atk": "s_attack",
    "sp atk": "s_attack",
    "special attack": "s_attack",
    "sp. def": "s_defense",
    "sp def": "s_defense",
    "special defense": "s_defense",
    "speed": "speed"
}

POKE_TYPES = {
    "normal", "fire", "water", "electric", "grass", "ice",
    "fighting", "poison", "ground", "flying", "psychic",
    "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"
}

# Map of comparisons and their operators
OPERATOR_MAP = {
    "more than": ">",
    "greater than": ">",
    "or more": ">=",
    "over": ">",
    "less than": "<",
    "under": "<",
    "below": "<",
    "or less": "<=",
    "equal to": "==",
    "equals": "==",
    "=": "==",
    "==": "==",
    ">=": ">=",
    "<=": "<=",
    ">": ">",
    "<": "<"  
}

#Uses rapidfuzz to allow typo lenience in user query
def match(query, choices, threshold=80):
    match, score, _ = process.extractOne(query, choices)
    return match if score >= threshold else None

def extract_query_components(text):
    text = text.lower() #Lowercase all text to match the dataset
    doc = nlp(text) #Processes user query as a list of tokens

    tokens = [token.text for token in doc]

    #Step 1: Type detection in user query
    type = None
    for word in tokens:
        possible_type = match(word, POKE_TYPES)
        if possible_type:
            type = possible_type
            break
    
    #Step 2: Stat detection in user query by matching against POKE_STATS keys
    stat = None
    for word in tokens:
        possible_stat = match(word, POKE_STATS.keys())
        if possible_stat:
            stat = POKE_STATS[possible_stat]
            break
    
    #Step 3: Look for comparison/operator using keyword matching
    op = None
    for phrase, symbol in OPERATOR_MAP.items():
        if phrase in text:
            op = symbol
            break
    
    #Step 4: Look for stat value using regex
    value_match = re.search(r"\b\d+\b", text)
    value = int(value_match.group()) if value_match else None

    if type and stat and op and value is not None:
        return {
            "type": type,
            "stat": stat,
            "op": op,
            "value": value            
        }
    else:
        return {"Error": "Could not fully parse query"}
