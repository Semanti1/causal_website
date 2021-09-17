from flask import Flask, render_template, request, jsonify, redirect, url_for
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
plan_object=None
display_object=[]
first_page = None
second_page = 0

@app.route("/")
def home():
    # image_path, img_json = furnitureloader.load()
    # global random_string
    # global encoding
    # random_string = ''.join(random.choice(letters) for i in range(10));
    # encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    #
    # rand_indx = random.randint(0, 1)
    # if rand_indx ==0 :
    #     return redirect(url_for("heat_based"))
    # else:
    #     return redirect(url_for("electric_based"))
    # causalgraph.reset();
    # return render_template("index.html", furniture_image=image_path, description=img_json);
    return render_template("tutorial.html")


@app.route("/tutorial")
def tutorial():
    global first_page
    global second_page
    first_page = None
    second_page  = 0
    return render_template("tutorial.html")

@app.route("/after_tutorial", methods=["GET", "POST"])
def after_tutorial():
    global first_page
    first_page = random.randint(0, 1)
    if first_page ==0 :
        return redirect(url_for("heat_based"))
    else:
        return redirect(url_for("electric_based"))

@app.route("/next_experiment", methods=["GET","POST"])
def next_experiment():
    global first_page
    global second_page
    if first_page == 0:
        if second_page == 0:
            second_page = 1
            return redirect(url_for("electric_based"))
        else:
            second_page = 2
            return redirect(url_for("light"))
    else:
        if second_page == 0:
            second_page = 1
            return redirect(url_for("heat_based"))
        else:
            second_page = 2
            return redirect(url_for("light"))
@app.route("/complete", methods=["GET", "POST"])
def complete():
    code = ''.join(random.choice(letters) for i in range(10));
    return render_template("complete.html", code=code)

@app.route("/lamp")
def lamp():
    global plan_object
    plan_object = "flashlight"
    furnitureloader.set_furniture(plan_object, index=1)
    plan_image_path, plan_json = furnitureloader.load()
    furnitureloader.set_furniture("lamp", index=1)
    image_path, img_json = furnitureloader.load()
    global random_string
    global encoding
    random_string = ''.join(random.choice(letters) for i in range(10));
    encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    causalgraph.reset();
    return render_template("index.html", furniture_image=image_path, description_list=img_json, plan_object=plan_object, plan_object_image=plan_image_path, plan_description=plan_json);

@app.route("/kerosene_lamp")
def kerosene_lamp():
    global plan_object
    plan_object = "candle"
    furnitureloader.set_furniture(plan_object, index=1)
    plan_image_path, plan_json = furnitureloader.load()
    furnitureloader.set_furniture("kerosene_lamp", index=1)
    image_path, img_json = furnitureloader.load()
    global random_string
    global encoding
    random_string = ''.join(random.choice(letters) for i in range(10));
    encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    causalgraph.reset();
    return render_template("index.html", furniture_image=image_path, description_list=img_json, plan_object=plan_object, plan_object_image=plan_image_path, plan_description=plan_json);

@app.route("/candle")
def candle():
    global plan_object
    plan_object = "kerosene_lamp"
    furnitureloader.set_furniture(plan_object, index=1)
    plan_image_path, plan_json = furnitureloader.load()
    furnitureloader.set_furniture("candle", index=1)
    image_path, img_json = furnitureloader.load()
    global random_string
    global encoding
    random_string = ''.join(random.choice(letters) for i in range(10));
    encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    causalgraph.reset();
    return render_template("index.html", furniture_image=image_path, description_list=img_json, plan_object="Kerosene lamp", plan_object_image=plan_image_path, plan_description=plan_json);

@app.route("/flashlight")
def flashlight():
    global plan_object
    plan_object = "lamp"
    furnitureloader.set_furniture(plan_object, index=1)
    plan_image_path, plan_json = furnitureloader.load()
    furnitureloader.set_furniture("flashlight", index=1)
    image_path, img_json = furnitureloader.load()
    global random_string
    global encoding
    random_string = ''.join(random.choice(letters) for i in range(10));
    encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    causalgraph.reset();
    return render_template("index.html", furniture_image=image_path, description_list=img_json, plan_object=plan_object, plan_object_image=plan_image_path, plan_description=plan_json);


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

@app.route("/heat_based")
def heat_based():
    global plan_object
    heat_based_list = ["kerosene_lamp", "candle", "oil_lamp"]
    rand_indx = random.randint(0, len(heat_based_list)-1)
    plan_object=heat_based_list[rand_indx]
    furnitureloader.set_furniture(plan_object, index=1)
    plan_image_path, plan_json = furnitureloader.load()
    global display_object
    display_object = [o for i, o in enumerate(heat_based_list) if i != rand_indx]
    image_path_list, json_file_list = furnitureloader.load_category(display_object);
    global random_string
    global encoding
    random_string = ''.join(random.choice(letters) for i in range(10));
    encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    causalgraph.reset();
    return render_template("index.html", furniture_image=image_path_list, description_list=json_file_list, plan_object=plan_object, plan_object_image=plan_image_path, plan_description=plan_json, second_page=second_page);


@app.route("/electric_based")
def electric_based():
    global plan_object
    electric_based_list = ["lamp", "flashlight", "wall_lamp"]
    rand_indx = random.randint(0, len(electric_based_list)-1)
    plan_object=electric_based_list[rand_indx]
    furnitureloader.set_furniture(plan_object, index=1)
    plan_image_path, plan_json = furnitureloader.load()
    global display_object
    display_object = [o for i, o in enumerate(electric_based_list) if i != rand_indx]
    image_path_list, json_file_list = furnitureloader.load_category(display_object);
    global random_string
    global encoding
    random_string = ''.join(random.choice(letters) for i in range(10));
    encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    causalgraph.reset();
    return render_template("index.html", furniture_image=image_path_list, description_list=json_file_list, plan_object=plan_object, plan_object_image=plan_image_path, plan_description=plan_json, second_page=second_page);


@app.route("/light")
# def light():
#     image_path_list, json_file_list = furnitureloader.load_all()
#     global random_string
#     global encoding
#     random_string = ''.join(random.choice(letters) for i in range(10));
#     encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
#     causalgraph.reset();
#     print(image_path_list, furnitureloader.furniture_path)
#     return render_template("index.html", furniture_image=image_path_list, description_list=json_file_list, plan_object="", plan_object_image=);
def light():
    image_path_list, json_file_list, plan_image_path_list, plan_json_file_list = furnitureloader.load_all2();
    print(image_path_list)
    global random_string
    global encoding
    global plan_object
    global second_page
    plan_object = "all"
    random_string = ''.join(random.choice(letters) for i in range(10));
    encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    causalgraph.reset();
    return render_template("index.html", furniture_image=image_path_list, description_list=json_file_list, plan_object="two objects", plan_object_image=plan_image_path_list, plan_description=plan_json_file_list, second_page=second_page);



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

@app.route("/recieve_plan_property", methods=["POST"])
def receive_plan_data():
    data = request.get_json()
    global encoding
    global plan_object
    # furnitureloader.set_furniture(plan_object, index=1)
    root = os.path.dirname(os.path.abspath(__file__))
    property_path = os.path.join(root,"static/causal_graph/", "object_property_" + plan_object+ "_" + encoding + ".json")
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
    causal_path = os.path.join(root,"static/causal_graph/", "causal_" + encoding + ".json")
    # causal_path = os.path.join(furnitureloader.furniture_path, "causal_" + encoding + ".json")
    content = request.get_json();
    success = causalinfo.create_causal_info(content, causal_path);
    code = "adkfjaqier";
    if success == 0 :
        return jsonify("successfully saved the causal model.");
    elif success ==1:
        return jsonify("There is an error on the server end to save the causal model. Please report this to the developer.")
    elif success == 2:
        return jsonify("All nodes must be connected to the goal node directly or indirectly")
    elif success == 3:
        return jsonify("There are syntax error in your causal rules")
    elif success == 4:
        return jsonify("Object property cannot be used as effect")
    elif success == 5:
        return jsonify("Effect nodes must be caused by at least one of the functions")
@app.route("/record_time", methods=["POST"])
def record_time():
    global encoding
    root = os.path.dirname(os.path.abspath(__file__))
    time_path = os.path.join(root,"static/causal_graph/" "submit_time_" + encoding + ".json");
    submit_time = request.get_json()
    with open(time_path, "w") as f:
        f.write(str(submit_time["time"]))
    print(submit_time)
    return "success";

@app.route("/plan_causal", methods=["POST"])
def plan_causal():
    global encoding
    root = os.path.dirname(os.path.abspath(__file__))
    causal_path = os.path.join(root,"static/causal_graph/")
    furniture_path = furnitureloader.furniture_path
    #print(causal_path, plan_object, furniture_path)
    global display_object
    return jsonify(website_plan(causal_path, causal_path, encoding, display_object, gen=False))


if __name__ == '__main__':
    app.run(debug=True)
    # socketio.run(app, debug=True, port=8000)
