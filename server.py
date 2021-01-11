from flask import Flask, render_template, request, jsonify
from script.causal_graph import CausalGraph, CausalInfo
from script.load_furniture import FurnitureLoader
from flask_socketio import SocketIO
import json
import os

app = Flask(__name__)
socketio = SocketIO(app)
furnitureloader = FurnitureLoader()
causalgraph = CausalGraph()
causalinfo = CausalInfo()

@app.route("/")
def home():
    image_path, img_json = furnitureloader.load()
    return render_template("index.html", furniture_image=image_path, description=img_json);

@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")

@app.route("/recieve_property", methods = ["POST"])
def receive_data():
    data = request.get_json()
    property_path = os.path.join(furnitureloader.furniture_path, "object_property.json")
    with open(property_path, "w") as file:
        json.dump(data, file);
    return "OK"
@app.route("/recieve_causal", methods=["POST"])
def receive_causal_data():
    content = request.get_json()
    print(content)
    file_name = causalgraph.process_causal(content)
    socketio.emit("causal graph", file_name);
    return "OK"

@app.route("/submit_causal", methods=["POST"])
def submit_causal_data():
    causal_path = os.path.join(furnitureloader.furniture_path, "causal.json");
    content = request.get_json()
    causalinfo.create_causal_info(content, causal_path);
    return "OK"

if __name__ == '__main__':
    #app.run(debug=True)
    socketio.run(app, debug=True)
