import json, os
FILEPATH = 'data/library.json'

def charger_donnees():
    if not os.path.exists(FILEPATH): return {'livres': [], 'emprunts': []}
    with open(FILEPATH) as f: return json.load(f)

def sauvegarder_donnees(data):
    with open(FILEPATH, 'w') as f: json.dump(data, f, indent=2)

