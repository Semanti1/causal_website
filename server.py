from flask import Flask, render_template, request, jsonify
from causal_graph import process_causal
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recieve_property", methods = ["POST"])
def receive_data():
    print(request.get_json())
    return "OK"
@app.route("/recieve_causal", methods=["POST"])
def receive_causal_data():
    content = request.get_json()
    print(content)
    file_name = process_causal(content)
    socketio.emit("causal graph", file_name);
    return "OK"

if __name__ == '__main__':
    #app.run(debug=True)
    socketio.run(app, debug=True)
