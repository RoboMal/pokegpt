def generate_response(parsed_query: dict, filtered_df) -> str:
    """
    Generates a natural language response based on the query and results.
    
    Args:
        parsed_query: dict with keys "type", "stat", "op", "value"
        filtered_df: pandas DataFrame containing filtered Pokémon
        
    Returns:
        A human-readable chatbot response string
    """
    if "error" in parsed_query:
        return "Sorry, I couldn't understand your request. Please try rephrasing it."

    poke_type = parsed_query["type"]
    stat = parsed_query["stat"]
    op = parsed_query["op"]
    value = parsed_query["value"]

    count = len(filtered_df)
    
    # No matches
    if count == 0:
        return f"I couldn't find any {poke_type.capitalize()}-type Pokémon with {stat} {op} {value}."

    # Format Pokémon names
    names = filtered_df["name"].tolist()
    formatted_names = ", ".join(names[:-1]) + f", and {names[-1]}" if count > 1 else names[0]

    # Pick template based on count
    if count == 1:
        return f"I found one {poke_type.capitalize()}-type Pokémon with {stat} {op} {value}: {formatted_names}."
    elif count <= 5:
        return f"Here are the {poke_type.capitalize()}-type Pokémon with {stat} {op} {value}: {formatted_names}."
    else:
        return f"There are {count} {poke_type.capitalize()}-type Pokémon matching your query ({stat} {op} {value}). Some examples include: {formatted_names}."
