from flask import Flask, request, send_file, jsonify
from gevent.pywsgi import WSGIServer
import time, os

app = Flask(__name__)

hostName = "localhost"
serverPort = 8080

passwords = ["123", "321", "999", "666", "3301"]


@app.route('/', methods=['GET'])
def index():
    data = request.json
    if data.get("Search") in ["Hello, World", "Hello, World!", "Hello World", "hello, world!", "hello, world", "hello world"]:
        return jsonify("Answer", "Hello there! How can I help you today")
    else:
        return jsonify("Answer", "I'm sorry, I couldn't understand. Could you repeat that?")

@app.route("/secret", methods=['GET', 'POST'])
def secrets():
    data = request.json
    if data.get("Search") in ["Passwords", "passwords"]:
        return jsonify("Passwords", passwords)
        
    elif data.get("Add-password"):
        passwords.append(data.get("Add-password"))
        return f'Password added: {data.get("Add-password")}'



if __name__ == "__main__":        
    webServer = WSGIServer((hostName, serverPort), app)
    print("Server started http://%s:%s" % (hostName, serverPort))
    
    webServer.serve_forever()
