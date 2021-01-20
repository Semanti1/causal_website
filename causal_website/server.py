from flask import Flask, render_template, request, jsonify
from causal_website.causal_graph import CausalGraph, CausalInfo, check_correctness, check_extend
from causal_website.load_furniture import FurnitureLoader
import json
import os
from causal_website import app
# app = Flask(__name__)
#
# socketio = SocketIO(app)
furnitureloader = FurnitureLoader()
causalgraph = CausalGraph(furnitureloader.furniture)
causalinfo = CausalInfo()

@app.route("/")
def home():
    image_path, img_json = furnitureloader.load()
    causalgraph.reset();
    return render_template("index.html", furniture_image=image_path, description=img_json);

@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")
@app.route("/lamp")
def lamp():
    furnitureloader.set_furniture("lamp")
    image_path, img_json = furnitureloader.load()
    return render_template("index.html", furniture_image=image_path, description=img_json);
@app.route("/chair")
def chair():
    furnitureloader.set_furniture("chair")
    image_path, img_json = furnitureloader.load()
    return render_template("index.html", furniture_image=image_path, description=img_json);

@app.route("/recieve_property", methods = ["POST"])
def receive_data():
    data = request.get_json()
    property_path = os.path.join(furnitureloader.furniture_path, "object_property.json")
    with open(property_path, "w") as file:
        json.dump(data, file);
    return "OK"

@app.route("/check_correct", methods=["POST"])
def check_correct():
    content = request.get_json()
    value = check_correctness(content);
    return jsonify(value)

@app.route("/recieve_causal", methods=["POST"])
def receive_causal_data():
    content = request.get_json()
    print(content)
    file_name = causalgraph.process_causal(content)
    return jsonify(file_name)

@app.route("/submit_causal", methods=["POST"])
def submit_causal_data():
    causal_path = os.path.join(furnitureloader.furniture_path, "causal.json");
    content = request.get_json()
    success = causalinfo.create_causal_info(content, causal_path);
    if success:
        return jsonify("successfully saved the causal model");
    else:
        return jsonify("There is an error on the server end to save the causal model. Please report this to the developer.")


if __name__ == '__main__':
    app.run(debug=True)
    # socketio.run(app, debug=True, port=8000)
