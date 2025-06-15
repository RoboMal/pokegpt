import spacy as sp
import re

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
    "Normal", "Fire", "Water", "Electric", "Grass", "Ice",
    "Fighting", "Poison", "Ground", "Flying", "Psychic",
    "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"
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

def extract_query_components(text):
    doc = nlp(text.lower())

    #Step 1: Look for types in user query
    type = None
    for token in doc:
        #Crude guess: Checks if token is a proper noun or known Pokemon type
        if token.text.capitalize() in POKE_TYPES:
            type = token.text.capitalize()
            break
    
    #Step 2: Look for mention of stats by matching against POKE_STATS keys
    stat = None
    for key in POKE_STATS:
        if key in text.lower():
            stat = POKE_STATS[key]
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
        return {"Error": "Could not parse"}
    
