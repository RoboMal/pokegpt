from parser import extract_query_components

query = "List all Fire types with 100 or more special attack"
parsed = extract_query_components(query)

print(parsed)