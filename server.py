from flask import Flask, render_template, request, jsonify
from script.causal_graph import CausalGraph
from script.load_furniture import FurnitureLoader
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)
furnitureloader = FurnitureLoader()
causalgraph = CausalGraph()

@app.route("/")
def home():
    image_path, img_json = furnitureloader.load()
    return render_template("index.html", furniture_image=image_path, description=img_json);

@app.route("/recieve_property", methods = ["POST"])
def receive_data():
    print(request.get_json())
    return "OK"
@app.route("/recieve_causal", methods=["POST"])
def receive_causal_data():
    content = request.get_json()
    print(content)
    file_name = causalgraph.process_causal(content)
    socketio.emit("causal graph", file_name);
    return "OK"

if __name__ == '__main__':
    #app.run(debug=True)
    socketio.run(app, debug=True)
