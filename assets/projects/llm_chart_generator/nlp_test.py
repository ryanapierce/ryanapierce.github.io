import spacy

nlp = spacy.load("en_core_web_sm")

def extract_query_intent(user_query):
    doc = nlp(user_query.lower())

    # Identify stats the user wants to compare
    metrics = ["points", "rebounds", "assists", "per", "ws", "bpm", "vorp", "fg%", "3p%", "ft%"]
    players = ["lebron james", "michael jordan"]

    extracted_metrics = [token.text for token in doc if token.text in metrics]
    extracted_players = [token.text.title() for token in doc if token.text in players]

    # Identify if user requests a visualization
    if "heatmap" in user_query:
        return {"visualization": "heatmap", "players": extracted_players}
    elif "bar chart" in user_query:
        return {"visualization": "bar", "players": extracted_players, "metrics": extracted_metrics}
    else:
        return {"compare": extracted_players, "metrics": extracted_metrics}

# Example Usage
query = "Who is better, Lebron James or Michael Jordan in points and rebounds?"
intent = extract_query_intent(query)
print(intent)
