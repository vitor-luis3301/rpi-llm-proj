import json
import requests

def translation_to_en(text, tgt):
    url = "http://127.0.0.1:5000/translate"
    payload = {
        "q": text,
        "source": tgt,
        "target": "en"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    response = json.loads(requests.post(url, json=payload, headers=headers).text)
    
    return str(response["translatedText"])

def translation_to_tgt(text, tgt):
    url = "http://127.0.0.1:5000/translate"
    payload = {
        "q": text,
        "source": "en",
        "target": tgt
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    response = json.loads(requests.post(url, json=payload, headers=headers).text)
    
    return str(response["translatedText"])