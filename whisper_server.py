import whisper, sys, torch
from time import gmtime, strftime
from flask import Flask, request, send_file, jsonify
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

hostName = "localhost"
serverPort = 6050


torch.cuda.init()
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Device: ", device)

model_name = "tiny"
model = whisper.load_model(model_name).to(device)
if model:
    print("Model loaded: ", model_name)
else:
    print("ERROR. Something went wrong")


@app.route("/whisper/manual", methods=['GET'])
def stt_transcribe():
    data = request.json
    audio_pth = data.get("file")
    audio_task = data.get("task")
    
    audio = whisper.load_audio(audio_pth)
    result = model.transcribe(audio, task=audio_task)
    
    input_log = strftime("%H:%M:%S", gmtime()) + ' User: ' + result["text"]
    print(input_log)
    return result["text"]

@app.route("/whisper/auto", methods=['GET'])
def stt_auto():
    data = request.json
    
    audio_pth = data.get("file")
    lang = ''
    
    audio = whisper.load_audio(audio_pth)
    
    if data.get("language") == "Auto":
        # load audio and pad/trim it to fit 30 seconds
        audio = whisper.pad_or_trim(audio)

        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

        # detect the spoken language
        _, probs = model.detect_language(mel)
        print(f"Detected language: {max(probs, key=probs.get)}")
        del mel
        lang = max(probs, key=probs.get)
    else:
        lang = data.get("language")
        print("Selected Language: ", lang)
        
    result = model.transcribe(audio)
    
    input_log = strftime("%H:%M:%S", gmtime()) + ' User: ' + result["text"]
    print(input_log)

    if lang != "en":
        result = model.transcribe(audio, task='translate')

    return (lang, result["text"])



if __name__ == "__main__":        
    webServer = WSGIServer((hostName, serverPort), app)
    print("Server started http://%s:%s" % (hostName, serverPort))
    
    webServer.serve_forever()