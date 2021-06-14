from flask import Flask, render_template, request, jsonify
from causal_website.causal_graph import CausalGraph, CausalInfo, check_correctness, check_extend
from causal_website.load_furniture import FurnitureLoader
import json
import os
from causal_website import app
import hashlib as hasher
import string
import random
from causal_website.planner.main import website_plan
# app = Flask(__name__)
#
# socketio = SocketIO(app)
furnitureloader = FurnitureLoader()
causalgraph = CausalGraph(furnitureloader.furniture)
causalinfo = CausalInfo()
letters = string.ascii_lowercase
random_string= 0;
encoding  = 0;

@app.route("/")
def home():
    image_path, img_json = furnitureloader.load()
    global random_string
    global encoding
    random_string = ''.join(random.choice(letters) for i in range(10));
    encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();

    causalgraph.reset();
    return render_template("index.html", furniture_image=image_path, description=img_json);

@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")
@app.route("/lamp")
def lamp():
    furnitureloader.set_furniture("lamp", index=3)
    image_path, img_json = furnitureloader.load()
    global random_string
    global encoding
    random_string = ''.join(random.choice(letters) for i in range(10));
    encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    causalgraph.reset();
    return render_template("index.html", furniture_image=image_path, description_list=img_json);

@app.route("/chair")
def chair():
    furnitureloader.set_furniture("chair", index=3)
    image_path, img_json = furnitureloader.load()
    global random_string
    global encoding
    random_string = ''.join(random.choice(letters) for i in range(10));
    encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    causalgraph.reset();
    return render_template("index.html", furniture_image=image_path, description_list=img_json);

@app.route("/light")
def light():
    image_path_list, json_file_list = furnitureloader.load_all()
    global random_string
    global encoding
    random_string = ''.join(random.choice(letters) for i in range(10));
    encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    causalgraph.reset();
    print(image_path_list)
    return render_template("index.html", furniture_image=image_path_list, description_list=json_file_list);



@app.route("/recieve_property", methods = ["POST"])
def receive_data():
    data = request.get_json()
    global encoding
    root = os.path.dirname(os.path.abspath(__file__))
    property_path = os.path.join(root,"static/causal_graph/" "object_property_" + encoding + ".json");
    #property_path = os.path.join(furnitureloader.furniture_path, "object_property_" + encoding + ".json")
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
    global encoding
    root = os.path.dirname(os.path.abspath(__file__))
    causal_path = os.path.join(root,"static/causal_graph/" "causal_" + encoding + ".json");
    content = request.get_json()
    success = causalinfo.create_causal_info(content, causal_path);
    code = "adkfjaqier";
    if success == 0 or success ==2:
        return jsonify("successfully saved the causal model.");
    elif success ==1:
        return jsonify("There is an error on the server end to save the causal model. Please report this to the developer.")
    # elif success == 2:
    #     return jsonify("All nodes must be connected to the goal node directly or indirectly")
    elif success == 3:
        return jsonify("Threr are syntax error in your causal rules")

@app.route("/plan_causal", methods=["POST"])
def plan_causal():
    global encoding
    root = os.path.dirname(os.path.abspath(__file__))
    causal_path = os.path.join(root,"static/causal_graph/")
    print(causal_path)
    return jsonify(website_plan(causal_path, encoding))

if __name__ == '__main__':
    app.run(debug=True)
    # socketio.run(app, debug=True, port=8000)
