import pandas as pd

#Map string operator to actual Python operation
def apply_operator(series, op, value):
    if op == ">=":
        return series >= value
    elif op == "<=":
        return series <= value
    elif op == ">":
        return series > value
    elif op == "<":
        return series < value
    elif op == "==":
        return series == value
    else:
        raise ValueError(f"Unsupported operator: {op}")
    
def filter_data(df, query):
    '''
    Filter dataframe based on parsed query components.

    Args:
        df: Pokedex dataframe
        query: The user's query broken down into a structured dict with the following keys
            - type: Should match to a Pokemon's type as listed in the dataset
            - stat: Should match to one of the stat columns in the dataset
            - op: Should match to one of the operators in the user's query
            - value: The value of stat

    Returns:
        Filtered dataframe
    '''
    type = query["type"]
    stat = query["stat"]
    op = query["op"]
    value = query["value"]

    #Check type membership from list
    type_filter = df["type"].apply(lambda t: type.lower() in [x.lower() for x in t])

    #Check stat value condition
    stat_filter = apply_operator(df[stat], op, value)

    #Combine filters
    result_df = df[type_filter & stat_filter]

    #return relevant columns
    return result_df[["name", "type", stat]]