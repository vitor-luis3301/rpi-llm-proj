import requests

headers = {
    'Content-Type': 'application/json',
}

json_data = {
    'model': 'medium',
    'language': 'auto',
    'file': 'recording.wav',
}

response = requests.get('http://localhost:5000/whisper/transcribe', json=json_data)
print(response.text)