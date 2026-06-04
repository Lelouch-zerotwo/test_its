import json

#primo esercizio
raw_data = '{"server": "Amazon", "config": {"port": 80, "active": true}}'

data = json.loads(raw_data)

print(data["config"]["port"])


#secondo esercizio
json_social = '[{"id": 1, "tag": "python"}, {"id": 2, "tag": "gaming"}, {"id": 3, "tag": "python"}, {"id": 4, "tag": "webdev"}, {"id": 5, "tag": "python"}, {"id": 6, "tag": "gaming"}]'

conteggio = json.loads(json_social)

#conteggia quanti e quali tag ci sono nel "json" -->"risultato=  python: 3, gaming: 2, webdev: 1"

for i in conteggio:
    