from src.utils.secret_storage import secrets

import requests
import json

def perspective(text):
    report = {'troll': 0.0, 'notes':[]}

    key = secrets["perspective_key"]

    data = {"comment": {"text": text}, "languages": ["en"], "requestedAttributes": {"TOXICITY": {}}}

    res = requests.post("https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="+key, json.dumps(data))

    out = res.json()

    # TODO: sometimes this gets error KeyError: 'attributeScores'
    report['troll'] = out['attributeScores']['TOXICITY']['summaryScore']['value']

    return report

if __name__ == "__main__":
    print(perspective("what kind of dumb name is quagmire anyway?"))
