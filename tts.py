import requests, sys

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer your_api_key_here',
}

json_data = {
    "input": sys.argv[1],
    "voice": sys.argv[2],
    "response_format": "mp3",
    "speed": 1.0
}

response = requests.post('http://localhost:5050/v1/audio/speech', headers=headers, json=json_data)

with open(sys.argv[3], 'wb') as f:
    f.write(response.content)