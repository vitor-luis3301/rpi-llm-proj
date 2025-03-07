import requests

url = 'http://localhost:6050/whisper'

result = ''
def transcribe_audio(audio_pth):
    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'file': audio_pth,
        'task': 'transcribe',
    }
    
    response = requests.get(f'{url}/manual', json=json_data, headers=headers)
    
    print(response.text)
    return response.text

def translate_audio(audio_pth):
    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'file': audio_pth,
        'task': 'translate',
    }
    
    response = requests.get(f'{url}/manual', json=json_data, headers=headers)
    print(response.text[0])
    return response.text    

def transcribe_and_translate(audio_pth, **kwargs):
    language = kwargs.get("language", None)
    
    headers = {
        'Content-Type': 'application/json',
    }

    if language:
        json_data = {
            'file': audio_pth,
            'language': language,
        }
    else:
        json_data = {
            'file': audio_pth,
            'language': 'Auto',
        }
    
    response = requests.get(f'{url}/auto', json=json_data, headers=headers)
    print(response.text)
    return response.text