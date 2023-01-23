from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import flask_session
from flask_session import Session
from causal_website.causal_graph import CausalGraph, CausalInfo, check_correctness_new, check_extend
from causal_website.load_furniture import FurnitureLoader
import json
import os
from causal_website import app
import hashlib as hasher
import string
import random
from causal_website.planner.main import website_plan

# app = Flask(__name__)
# app = Flask(__name__)
# app.secret_key = "hdjhnmn"
# Check Configuration section for more details
# SESSION_TYPE = 'filesystem'
# app.config.from_object(__name__)
# Session(app)
# app = Flask(__name__)
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)
# session["submit_causal_1"] = 0
# session["submit_causal_2"] = 0
# session["submit_causal_3"] = 0
# app = Flask(__name__)
#
# socketio = SocketIO(app)
'''furnitureloader = FurnitureLoader()
causalgraph = CausalGraph(furnitureloader.furniture)
causalinfo = CausalInfo()
letters = string.ascii_lowercase
random_string = 0;
encoding = 0;
plan_object = None
display_object = []
first_page = None
step = 0'''
'''session["furnitureloader"] = FurnitureLoader()
session["causalgraph"] = CausalGraph(session["furnitureloader"].furniture)
session["causalinfo"] = CausalInfo()
session["letters"] = string.ascii_lowercase
session["random_string"] = 0
session["encoding"] = 0
session["plan_object"] = None
session["display_object"] = []
session["first_page"] = None
session["second_page"] = 0
session["step"]=0'''
# submit_causal_1 = 0
# submit_causal_2 = 0
# submit_causal_3 = 0

@app.route("/")
def home():
    # image_path, img_json = furnitureloader.load()
    session["submit_causal_0"] = 0
    session["submit_causal_1"] = 0
    session["submit_causal_2"] = 0
    session["submit_causal_3"] = 0

    session["furnitureloader"] = FurnitureLoader()
    session["causalgraph"] = CausalGraph(session["furnitureloader"].furniture)
    session["causalinfo"] = CausalInfo()
    session["letters"] = string.ascii_lowercase
    session["random_string"] = 0
    session["encoding"] = 0
    session["plan_object"] = None
    session["display_object"] = []
    session["first_page"] = None
    session["second_page"] = 0
    session["step"] = 1
    session["obj_prop_no0"] = 0
    session["obj_prop_no1"]=0
    session["obj_prop_no2"] = 0
    session["obj_prop_no3"] = 0
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
    '''global first_page
    global second_page
    first_page = None
    second_page = 0'''
    return render_template("tutorial.html")


@app.route("/after_tutorial", methods=["GET", "POST"])
def after_tutorial():
    #global first_page
    #global["first_page"] = random.randint(0, 1)
    session["first_page"] = random.randint(0, 1)
    session["step"]=1
    session["encoding"]=request.form.get("pid")
    session.modified = True

    '''global step
    step = 1
    global random_string
    global encoding

    # random_string = ''.join(random.choice(letters) for i in range(10));
    # encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    encoding = request.form.get("pid");
    global plan_object
    global display_object'''
    # global submit_causal_1
    # #submit_causal_1 = 0
    # global submit_causal_2
    # #submit_causal_2 = 0
    # global submit_causal_3
    # #submit_causal_3 = 0

    if session["first_page"] == 0:
        heat_based_list = ["kerosene_lamp", "candle", "oil_lamp"]
        rand_indx = random.randint(0, len(heat_based_list) - 1)
        session["plan_object"] = heat_based_list[rand_indx]
        session["display_object"] = [o for i, o in enumerate(heat_based_list) if i != rand_indx]
        session.modified = True
        return redirect(url_for(session["display_object"][0]))
        # return redirect(url_for("light_h"))
    else:
        electric_based_list = ["lamp", "flashlight", "wall_lamp"]
        rand_indx = random.randint(0, len(electric_based_list) - 1)
        session["plan_object"] = electric_based_list[rand_indx]
        session["display_object"]  = [o for i, o in enumerate(electric_based_list) if i != rand_indx]
        session.modified = True
        return redirect(url_for(session["display_object"][0]))
        # return redirect(url_for("light_e"))

@app.route("/after_tutorial_pract", methods=["GET", "POST"])
def after_tutorial_pract():
    #global first_page
    #global["first_page"] = random.randint(0, 1)
    #session["first_page"] = random.randint(0, 1)
    #session["step"]=1
    session["encoding"]=request.form.get("pid")
    session.modified = True
    session["furnitureloader"].set_furniture("recorder", index=1)
    session.modified = True
    plan_image_path, plan_json = session["furnitureloader"].load()

    plan_image_path_list = [plan_image_path[0]]
    print(plan_image_path_list)
    plan_json_file_list = [plan_json[0]]
    plan_object_list = list(["lamp"])

    # display_object = [o for i, o in enumerate(heat_based_list) if i != rand_indx]
    image_path_list, json_file_list = session["furnitureloader"].load_category(list(["recorder"]));
    # global random_string
    # global encoding
    # random_string = ''.join(random.choice(letters) for i in range(10));
    # encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    session["causalgraph"].reset()
    session.modified = True
    return render_template("index_gen_exp_tutorial.html", furniture_image=image_path_list, description_list=json_file_list,
                           plan_object=plan_object_list, plan_object_image=plan_image_path_list,
                           plan_description=plan_json_file_list, end_exp=False)






@app.route("/next_experiment", methods=["GET", "POST"])
def next_experiment():
    #global step
    session["step"] += 1
    session.modified = True
    if session["step"] == 1:
        return redirect(url_for("after_tutorial"))
    if session["step"] == 2:
        return redirect(url_for(session["display_object"][1]))
    if session["step"] == 3:
        if session["first_page"] == 0:
            return redirect(url_for("light_h"))
        else:
            return redirect(url_for("light_e"))
    if session["step"] == 4:
        return redirect(url_for("light"))
    # global first_page
    # global second_page
    # if first_page == 0:
    #     if second_page == 0:
    #         second_page = 1
    #         return redirect(url_for("electric_based"))
    #     else:
    #         second_page = 2
    #         return redirect(url_for("light"))
    # else:
    #     if second_page == 0:
    #         second_page = 1
    #         return redirect(url_for("heat_based"))
    #     else:
    #         second_page = 2
    #         return redirect(url_for("light"))

@app.route("/enter_prolific", methods=["GET", "POST"])
def enter_prolific():
    return render_template("prolific_id.html")

@app.route("/complete", methods=["GET", "POST"])
def complete():
    # code = ''.join(random.choice(session["letters"]) for i in range(10));
    # code='https://brown.co1.qualtrics.com/jfe/form/SV_blpZWbfUxXyxOyW'
    code = 'https://brown.co1.qualtrics.com/jfe/form/SV_9nvi8YUeJUjXkhM'
    return render_template("complete.html", code=code)


@app.route("/lamp")
def lamp():
    # global plan_object
    # plan_object = "flashlight"
    # furnitureloader.set_furniture(plan_object, index=1)
    # plan_image_path, plan_json = furnitureloader.load()
    '''furnitureloader.set_furniture("lamp", index=1)
    image_path, img_json = furnitureloader.load()
    # global random_string
    # global encoding
    # random_string = ''.join(random.choice(letters) for i in range(10));
    # encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    causalgraph.reset();
    # return render_template("index.html", furniture_image=image_path, description_list=img_json, plan_object=plan_object, plan_object_image=plan_image_path, plan_description=plan_json);
    return render_template("index.html", furniture_image=image_path, description_list=img_json, plan_object=None, end_exp=False);'''

    #furnitureloader.set_furniture("lamp", index=1)
    session["furnitureloader"].set_furniture("lamp", index=1)
    session.modified = True
    plan_image_path, plan_json = session["furnitureloader"].load()

    plan_image_path_list = [plan_image_path[0]]
    print(plan_image_path_list)
    plan_json_file_list = [plan_json[0]]
    plan_object_list = list(["lamp"])

    # display_object = [o for i, o in enumerate(heat_based_list) if i != rand_indx]
    image_path_list, json_file_list = session["furnitureloader"].load_category(list(["lamp"]));
    # global random_string
    # global encoding
    # random_string = ''.join(random.choice(letters) for i in range(10));
    # encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    session["causalgraph"].reset()
    session.modified = True
    return render_template("index_gen_exp1and2.html", furniture_image=image_path_list, description_list=json_file_list,
                           plan_object=plan_object_list, plan_object_image=plan_image_path_list,
                           plan_description=plan_json_file_list, end_exp=False)


@app.route("/kerosene_lamp")
def kerosene_lamp():
    # global plan_object
    # plan_object = "candle"
    # furnitureloader.set_furniture(plan_object, index=1)
    # plan_image_path, plan_json = furnitureloader.load()
    '''furnitureloader.set_furniture("kerosene lamp", index=1)
    image_path, img_json = furnitureloader.load()
    # global random_string
    # global encoding
    # random_string = ''.join(random.choice(letters) for i in range(10));
    # encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    causalgraph.reset();
    # return render_template("index.html", furniture_image=image_path, description_list=img_json, plan_object=plan_object, plan_object_image=plan_image_path, plan_description=plan_json);
    return render_template("index.html", furniture_image=image_path, description_list=img_json, plan_object=None, end_exp=False);'''
    session["furnitureloader"].set_furniture("kerosene_lamp", index=1)
    session.modified = True
    plan_image_path, plan_json = session["furnitureloader"].load()

    plan_image_path_list = [plan_image_path[0]]
    print(plan_image_path_list)
    plan_json_file_list = [plan_json[0]]
    plan_object_list = list(["kerosene_lamp"])

    # display_object = [o for i, o in enumerate(heat_based_list) if i != rand_indx]
    image_path_list, json_file_list = session["furnitureloader"].load_category(list(["kerosene_lamp"]));
    # global random_string
    # global encoding
    # random_string = ''.join(random.choice(letters) for i in range(10));
    # encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    session["causalgraph"].reset()
    session.modified = True
    return render_template("index_gen_exp1and2.html", furniture_image=image_path_list, description_list=json_file_list,
                           plan_object=plan_object_list, plan_object_image=plan_image_path_list,
                           plan_description=plan_json_file_list, end_exp=False)


@app.route("/candle")
def candle():
    # global plan_object
    # plan_object = "kerosene lamp"
    # furnitureloader.set_furniture(plan_object, index=1)
    # plan_image_path, plan_json = furnitureloader.load()
    '''furnitureloader.set_furniture("candle", index=1)
    image_path, img_json = furnitureloader.load()
    # global random_string
    # global encoding
    # random_string = ''.join(random.choice(letters) for i in range(10));
    # encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    causalgraph.reset();
    # return render_template("index.html", furniture_image=image_path, description_list=img_json, plan_object="Kerosene lamp", plan_object_image=plan_image_path, plan_description=plan_json);
    return render_template("index.html", furniture_image=image_path, description_list=img_json, plan_object=None, end_exp=False);'''

    # electric_based_list = ["lamp", "flashlight", "wall_lamp"]
    # rand_indx = random.randint(0, len(electric_based_list)-1)
    # far_obj =electric_based_list[rand_indx]
    session["furnitureloader"].set_furniture("candle", index=1)
    session.modified = True
    plan_image_path, plan_json = session["furnitureloader"].load()

    plan_image_path_list = [plan_image_path[0]]
    print(plan_image_path_list)
    plan_json_file_list = [plan_json[0]]
    plan_object_list = list(["candle"])

    # display_object = [o for i, o in enumerate(heat_based_list) if i != rand_indx]
    image_path_list, json_file_list = session["furnitureloader"].load_category(list(["candle"]));
    # global random_string
    # global encoding
    # random_string = ''.join(random.choice(letters) for i in range(10));
    # encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    session["causalgraph"].reset()
    session.modified = True
    return render_template("index_gen_exp1and2.html", furniture_image=image_path_list, description_list=json_file_list,
                           plan_object=plan_object_list, plan_object_image=plan_image_path_list,
                           plan_description=plan_json_file_list, end_exp=False)


@app.route("/flashlight")
def flashlight():
    # global plan_object
    # plan_object = "lamp"
    # furnitureloader.set_furniture(plan_object, index=1)
    # plan_image_path, plan_json = furnitureloader.load()
    '''furnitureloader.set_furniture("flashlight", index=1)
    image_path, img_json = furnitureloader.load()
    # global random_string
    # global encoding
    # random_string = ''.join(random.choice(letters) for i in range(10));
    # encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    causalgraph.reset();
    # return render_template("index.html", furniture_image=image_path, description_list=img_json, plan_object=plan_object, plan_object_image=plan_image_path, plan_description=plan_json);
    return render_template("index.html", furniture_image=image_path, description_list=img_json, plan_object="flashlight", end_exp=False);'''
    session["furnitureloader"].set_furniture("flashlight", index=1)
    session.modified = True
    plan_image_path, plan_json = session["furnitureloader"].load()

    plan_image_path_list = [plan_image_path[0]]
    print(plan_image_path_list)
    plan_json_file_list = [plan_json[0]]
    plan_object_list = list(["flashlight"])

    # display_object = [o for i, o in enumerate(heat_based_list) if i != rand_indx]
    image_path_list, json_file_list = session["furnitureloader"].load_category(list(["flashlight"]));
    # global random_string
    # global encoding
    # random_string = ''.join(random.choice(letters) for i in range(10));
    # encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    session["causalgraph"].reset()
    session.modified = True
    return render_template("index_gen_exp1and2.html", furniture_image=image_path_list, description_list=json_file_list,
                           plan_object=plan_object_list, plan_object_image=plan_image_path_list,
                           plan_description=plan_json_file_list, end_exp=False)


@app.route("/wall_lamp")
def wall_lamp():
    '''furnitureloader.set_furniture("wall_lamp", index=1)
    image_path, img_json = furnitureloader.load()
    causalgraph.reset();
    return render_template("index.html", furniture_image=image_path, description_list=img_json, plan_object=None, end_exp=False);'''
    session["furnitureloader"].set_furniture("wall_lamp", index=1)
    session.modified = True
    plan_image_path, plan_json = session["furnitureloader"].load()

    plan_image_path_list = [plan_image_path[0]]
    print(plan_image_path_list)
    plan_json_file_list = [plan_json[0]]
    plan_object_list = list(["wall_lamp"])

    # display_object = [o for i, o in enumerate(heat_based_list) if i != rand_indx]
    image_path_list, json_file_list = session["furnitureloader"].load_category(list(["wall_lamp"]));
    # global random_string
    # global encoding
    # random_string = ''.join(random.choice(letters) for i in range(10));
    # encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    session["causalgraph"].reset()
    session.modified = True
    return render_template("index_gen_exp1and2.html", furniture_image=image_path_list, description_list=json_file_list,
                           plan_object=plan_object_list, plan_object_image=plan_image_path_list,
                           plan_description=plan_json_file_list, end_exp=False)


@app.route("/oil_lamp")
def oil_lamp():
    '''furnitureloader.set_furniture("oil_lamp", index=1)
    image_path, img_json = furnitureloader.load()
    causalgraph.reset();
    return render_template("index.html", furniture_image=image_path, description_list=img_json, plan_object=None, end_exp=False);'''
    session["furnitureloader"].set_furniture("oil_lamp", index=1)
    session.modified = True
    plan_image_path, plan_json = session["furnitureloader"].load()

    plan_image_path_list = [plan_image_path[0]]
    print(plan_image_path_list)
    plan_json_file_list = [plan_json[0]]
    plan_object_list = list(["oil_lamp"])

    # display_object = [o for i, o in enumerate(heat_based_list) if i != rand_indx]
    image_path_list, json_file_list = session["furnitureloader"].load_category(list(["oil_lamp"]));
    # global random_string
    # global encoding
    # random_string = ''.join(random.choice(letters) for i in range(10));
    # encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    session["causalgraph"].reset()
    session.modified = True
    return render_template("index_gen_exp1and2.html", furniture_image=image_path_list, description_list=json_file_list,
                           plan_object=plan_object_list, plan_object_image=plan_image_path_list,
                           plan_description=plan_json_file_list, end_exp=False)


@app.route("/chair")
def chair():
    session["furnitureloader"].set_furniture("chair", index=3)
    image_path, img_json = session["furnitureloader"].load()
    #global random_string
    #global encoding
    session["random_string"] = ''.join(random.choice(session["letters"]) for i in range(10));
    session["encoding"] = hasher.sha256(session["random_string"].encode('utf-8')).hexdigest();
    session["causalgraph"].reset();
    return render_template("index.html", furniture_image=image_path, description_list=img_json);


@app.route("/light_h")
def light_h():
    #global plan_object
    #global display_object

    electric_based_list = ["lamp", "flashlight", "wall_lamp"]
    rand_indx = random.randint(0, len(electric_based_list) - 1)
    far_obj = electric_based_list[rand_indx]
    session["furnitureloader"].set_furniture(session["plan_object"], index=1)
    session.modified = True
    plan_image_path, plan_json = session["furnitureloader"].load()
    session["furnitureloader"].set_furniture(far_obj, index=1)
    session.modified = True
    plan_image_path_2, plan_json_2 = session["furnitureloader"].load()
    plan_image_path_list = [plan_image_path[0], plan_image_path_2[0]]
    print(plan_image_path_list)
    plan_json_file_list = [plan_json[0], plan_json_2[0]]
    plan_object_list = list([session["plan_object"], far_obj])

    # display_object = [o for i, o in enumerate(heat_based_list) if i != rand_indx]
    image_path_list, json_file_list = session["furnitureloader"].load_category(session["display_object"]);
    # global random_string
    # global encoding
    # random_string = ''.join(random.choice(letters) for i in range(10));
    # encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    session["causalgraph"].reset();
    session.modified = True
    return render_template("index_gen_nearfar.html", furniture_image=image_path_list, description_list=json_file_list,
                           plan_object=plan_object_list, plan_object_image=plan_image_path_list,
                           plan_description=plan_json_file_list, end_exp=True);


@app.route("/light_e")
def light_e():
    #global plan_object
    #global display_object

    heat_based_list = ["kerosene_lamp", "candle", "oil_lamp"]
    rand_indx = random.randint(0, len(heat_based_list) - 1)
    far_obj = heat_based_list[rand_indx]
    session["furnitureloader"].set_furniture(session["plan_object"], index=1)
    session.modified = True
    plan_image_path, plan_json = session["furnitureloader"].load()
    session["furnitureloader"].set_furniture(far_obj, index=1)
    session.modified = True
    plan_image_path_2, plan_json_2 = session["furnitureloader"].load()
    plan_image_path_list = [plan_image_path[0], plan_image_path_2[0]]
    plan_json_file_list = [plan_json[0], plan_json_2[0]]
    plan_object_list = list([session["plan_object"], far_obj])
    print(plan_image_path_list)

    # display_object = [o for i, o in enumerate(electric_based_list) if i != rand_indx]
    image_path_list, json_file_list = session["furnitureloader"].load_category(session["display_object"]);
    # global random_string
    # global encoding
    # random_string = ''.join(random.choice(letters) for i in range(10));
    # encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    session["causalgraph"].reset();
    session.modified = True
    return render_template("index_gen_nearfar.html", furniture_image=image_path_list, description_list=json_file_list,
                           plan_object=plan_object_list, plan_object_image=plan_image_path_list,
                           plan_description=plan_json_file_list, end_exp=True);


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
    image_path_list, json_file_list, plan_image_path_list, plan_json_file_list, plan_object_list = session["furnitureloader"].load_all2();
    print(image_path_list)
    # global random_string
    # global encoding
    #global plan_object
    #global second_page
    session["plan_object"] = "far"
    # random_string = ''.join(random.choice(letters) for i in range(10));
    # encoding = hasher.sha256(random_string.encode('utf-8')).hexdigest();
    session["causalgraph"].reset();
    return render_template("index_gen.html", furniture_image=image_path_list, description_list=json_file_list,
                           plan_object=plan_object_list, plan_object_image=plan_image_path_list,
                           plan_description=plan_json_file_list, end_exp=True);


@app.route("/recieve_property", methods=["POST"])
def receive_data():
    data = request.get_json()
    print("receive property ", data)
    #global encoding
    root = os.path.dirname(os.path.abspath(__file__))
    property_path = os.path.join(root, "static/causal_graph/",session["encoding"])
    if not os.path.exists(property_path):
        os.makedirs(property_path)
    file_name = "object_property_"
    #global step
    #global display_object
    if session["step"] == 0:
        file_name = "object_property_specific_obj0_" + session["display_object"][session["step"] - 1] + "_"+str(session.get("obj_prop_no0"))
    elif session["step"] == 1:
        file_name = "object_property_specific_obj1_" + session["display_object"][session["step"] - 1] + "_"+str(session.get("obj_prop_no1"))
        # session["obj_prop_no"]=data["time"]
        # session.modified = True
        # file_name = "object_property_specific_"
    elif session["step"] == 2:
        file_name = "object_property_specific_obj2_" + session["display_object"][session["step"] - 1] + "_"+str(session.get("obj_prop_no2"))
    elif session["step"] == 3:
        file_name = "object_property_near_"+"_"+str(session.get("obj_prop_no3"))
        # session["obj_prop_no"] = data["time"]
        # session.modified = True
    elif session["step"] == 4:
        file_name = "object_property_far_"+"_"+str(session.get("obj_prop_no"))
        # session["obj_prop_no"] = data["time"]
        # session.modified = True
    #property_path = os.path.join(root, "static/causal_graph/", file_name + "_"+session["encoding"] + ".json");
    property_path_new = os.path.join(property_path, file_name + "_" + session["encoding"] + ".json");
    # property_path = os.path.join(furnitureloader.furniture_path, "object_property_" + encoding + ".json")

    with open(property_path_new, "w") as file:
        json.dump(data, file);
    return "OK"


@app.route("/recieve_plan_property", methods=["POST"])
def receive_plan_data():
    data = request.get_json()
    #global encoding
    #global step
    # furnitureloader.set_furniture(plan_object, index=1)
    #root = os.path.dirname(os.path.abspath(__file__))
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)),"static/causal_graph/",session["encoding"])
    if not os.path.exists(root):
        os.makedirs(root)
    obj = data[-1]["obj_name"]
    #property_path = os.path.join(root, "static/causal_graph/", "object_property_" + obj + "_" + session["encoding"] + ".json")
    if session["step"] == 0:
        # property_path = os.path.join(root, "static/causal_graph/",
        #                              "object_property_specific_test_" + obj + "_" + session["encoding"] + ".json")
        property_path = os.path.join(root, "object_property_specific_test_" + obj + "_" + session["encoding"] + ".json")
    if session["step"] == 1 or session["step"] == 2:
        # property_path = os.path.join(root, "static/causal_graph/",
        #                              "object_property_specific_test_" + obj + "_" + session["encoding"] + ".json")
        property_path = os.path.join(root, "object_property_specific_test_" + obj + "_" + session["encoding"] + ".json")
    if session["step"] == 3:
        # property_path = os.path.join(root, "static/causal_graph/",
        #                              "object_property_near_test_" + obj + "_" + session["encoding"] + ".json")
        # property_path = os.path.join(root, "object_property_near_test_" + obj + "_" + session["encoding"] + ".json")
        property_path = os.path.join(root, "object_property_test_" + obj + "_" + session["encoding"] + ".json")
    if session["step"] == 4:
        # property_path = os.path.join(root, "static/causal_graph/",
        #                              "object_property_far_test_" + obj + "_" + session["encoding"] + ".json")
        property_path = os.path.join(root, "object_property_far_test_" + obj + "_" + session["encoding"] + ".json")

    with open(property_path, "w") as file:
        json.dump(data[:-1], file);
    return "OK"


@app.route("/check_correct", methods=["POST"])
def check_correct():
    content = request.get_json()
    value = check_correctness_new(content);
    return jsonify(value)


@app.route("/recieve_causal", methods=["POST"])
def receive_causal_data():
    content = request.get_json()
    print(content)
    file_name = session["causalgraph"].process_causal(content)
    return jsonify(file_name)


@app.route("/submit_causal", methods=["POST"])
def submit_causal_data():
    #global encoding
    # global submit_causal_1
    # global submit_causal_2
    # global submit_causal_3
    #global step
    # root = os.path.dirname(os.path.abspath(__file__))
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/causal_graph/", session["encoding"])
    if not os.path.exists(root):
        os.makedirs(root)
    # recording time

    submit_time = request.get_json()
    if session["step"] == 0:
        file_name = "causal_specific_tutorial_obj0_recorder_"
        session["submit_causal_0"] = submit_time["time"]

        session.modified = True
    elif session["step"] == 1:
        file_name = "causal_specific_obj1_" + session["display_object"][session["step"] - 1] + "_"
        session["submit_causal_1"] = submit_time["time"]

        session.modified = True

    elif session["step"] == 2:
        file_name = "causal_specific_obj2_" + session["display_object"][session["step"] - 1] + "_"
        session["submit_causal_2"] = submit_time["time"]
        session.modified = True
        # file_name = "causal_specific_"
    elif session["step"] == 3:
        file_name = "causal_near_"
        session["submit_causal_3"] = submit_time["time"]
        session.modified = True
    # elif step ==4:
    #     file_name = "causal_far_"
    #     submit_causal_3 = submit_time["time"] - submit_causal_1 - submit_causal_2
    # time_path = os.path.join(root, "static/causal_graph/", "submit_time_" + file_name + session["encoding"] + ".json")
    time_path = os.path.join(root, "submit_time_" + file_name + session["encoding"] + ".json")
    with open(time_path, "w") as f:
        if session["step"] == 0:
            f.write(str(session.get("submit_causal_0")))
        elif session["step"] == 1:
            f.write(str(session.get("submit_causal_1")))
        elif session["step"] == 2:
            f.write(str(session.get("submit_causal_2")))
        elif session["step"] == 3:
            f.write(str(session.get("submit_causal_3")))
    # if step <=2:
    #     file_name = "causal_specific_" + display_object[step-1] + "_"
    #     #file_name = "causal_specific_"
    # elif step == 3:
    #     file_name = "causal_near_"
    # elif step ==4:
    #     file_name = "causal_far_"
    if session["step"] == 0:
        # global submit_causal_1
        file_name = "causal_specific_tutorial_obj0_recorder_" + str(session["submit_causal_0"]) + "_"
    elif session["step"] == 1:
        # global submit_causal_1
        file_name = "causal_specific_obj1_" + session["display_object"][session["step"] - 1] + "_" + str(session["submit_causal_1"]) + "_"
    elif session["step"] == 2:
        # global submit_causal_2
        file_name = "causal_specific_obj2_" + session["display_object"][session["step"] - 1] + "_" + str(session.get("submit_causal_2")) + "_"
        # file_name = "causal_specific_"
    elif session["step"] == 3:
        # global submit_causal_3
        file_name = "causal_near_" + str(session.get("submit_causal_3")) + "_"
    elif session["step"] == 4:
        file_name = "causal_far_"
    # causal_path = os.path.join(root, "static/causal_graph/", file_name + session["encoding"] + ".json")
    causal_path = os.path.join(root,  file_name + session["encoding"] + ".json")
    # causal_path = os.path.join(furnitureloader.furniture_path, "causal_" + encoding + ".json")
    content = submit_time["as"];  # request.get_json();

    if session["step"] == 0:
        # global submit_causal_1
        file_name_cr = "causal_rules_tutorial_obj0_recorder_" + str(session["submit_causal_0"]) + "_"
    if session["step"] == 1:
        # global submit_causal_1
        file_name_cr = "causal_rules_specific_obj1_" + session["display_object"][session["step"] - 1] + "_" + str(session["submit_causal_1"]) + "_"
    elif session["step"] == 2:
        # global submit_causal_2
        file_name_cr = "causal_rules_specific_obj2_" + session["display_object"][session["step"] - 1] + "_" + str(session.get("submit_causal_2")) + "_"
        # file_name = "causal_specific_"
    elif session["step"] == 3:
        # global submit_causal_3
        file_name_cr = "causal_rules_near_" + str(session.get("submit_causal_3")) + "_"
    elif session["step"] == 4:
        file_name_cr = "causal_rules_far_"
    # causal_path = os.path.join(root, "static/causal_graph/", file_name + session["encoding"] + ".json")
    causalrules_path = os.path.join(root,  file_name_cr + session["encoding"] + ".json")

    with open(causalrules_path, "w") as file:
        json.dump(content, file)

    success = session["causalinfo"].create_causal_info(content, causal_path);
    return jsonify(success)
    #return json.dump(success)
    code = "adkfjaqier";
    # if success == 0:
    #     return jsonify("successfully saved the causal model.");
    # elif success == 1:
    #     # return jsonify(
    #     #     "There is an error on the server end to save the causal model. Please report this to the developer.")
    #     return jsonify("Some of your causal rules have errors.")
    # elif success == 2:
    #     return jsonify("All nodes must be connected to the goal node directly or indirectly")
    # elif success == 8:
    #     return jsonify("There are syntax error in your causal rules")
    # elif success == 7:
    #     return jsonify("missing AND")
    # elif success == 3:
    #     return jsonify("no necessary/preferrable is specified")
    # elif success == 4:
    #     return jsonify("Object property cannot be used as effect")
    # elif success == 5:
    #     return jsonify("Effect nodes must be caused by at least one of the functions")
    # elif success == 6:
    #     return jsonify("Goal node not present")


# @app.route("/record_time", methods=["POST"])
# def record_time():
#     global encoding
#     # global submit_causal_1
#     # global submit_causal_2
#     # global submit_causal_3
#     global step
#     root = os.path.dirname(os.path.abspath(__file__))
#     submit_time = request.get_json()
#     if step ==1:
#         file_name = "causal_specific_" + display_object[step-1] + "_"
#         session["submit_causal_1"] = submit_time["time"]
#
#         session.modified = True
#
#     elif step == 2:
#         file_name = "causal_specific_" + display_object[step - 1] + "_"
#         session["submit_causal_2"] = submit_time["time"]
#         session.modified = True
#         #file_name = "causal_specific_"
#     elif step == 3:
#         file_name = "causal_near_"
#         session["submit_causal_3"] = submit_time["time"]
#         session.modified = True
#     # elif step ==4:
#     #     file_name = "causal_far_"
#     #     submit_causal_3 = submit_time["time"] - submit_causal_1 - submit_causal_2
#     time_path = os.path.join(root, "static/causal_graph/", "submit_time_"+file_name + encoding + ".json")
#     with open(time_path, "w") as f:
#         if step ==1:
#             f.write(str(session.get("submit_causal_1")))
#         elif step==2:
#             f.write(str(session.get("submit_causal_2")))
#         elif step == 3:
#             f.write(str(session.get("submit_causal_3")))
#
#     #experimentalll
#
#
#     print(submit_time)
#     return "success";

@app.route("/record_time_step1", methods=["POST"])
def record_time_step1():
    #global encoding
    # global submit_causal_1
    # global submit_causal_2
    # global submit_causal_3
    #global step

    # root = os.path.dirname(os.path.abspath(__file__))
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/causal_graph/", session["encoding"])
    if not os.path.exists(root):
        os.makedirs(root)
    submit_time = request.get_json()
    #session["obj_prop_no"] = submit_time["time"]

    #session.modified = True
    #print("obj prop num", session["obj_prop_no"])
    if session["step"] == 0:
        file_name = "causal_specific_tutorial_obj0_recorder_"
        submit_step0_0 = submit_time["time"]
        session["obj_prop_no0"] = submit_time["time"]
        session.modified = True
    elif session["step"] == 1:
        file_name = "causal_specific_obj1_" + session["display_object"][session["step"] - 1] + "_"
        submit_step1_1 = submit_time["time"]
        session["obj_prop_no1"] = submit_time["time"]
        session.modified = True
    elif session["step"] == 2:
        file_name = "causal_specific_obj2_" + session["display_object"][session["step"] - 1] + "_"
        submit_step2_2 = submit_time["time"]
        session["obj_prop_no2"] = submit_time["time"]
        session.modified = True
        # file_name = "causal_specific_"
    elif session["step"] == 3:
        file_name = "causal_near_"
        submit_step3_3 = submit_time["time"]
        session["obj_prop_no3"] = submit_time["time"]
        session.modified = True
    # elif step ==4:
    #     file_name = "causal_far_"
    #     submit_causal_3 = submit_time["time"] - submit_causal_1 - submit_causal_2
    #time_path = os.path.join(root, "static/causal_graph/", "submit_time_step1_" + file_name + session["encoding"] + ".json")
    time_path = os.path.join(root, "submit_time_step1_" + file_name + session["encoding"] + ".json")
    with open(time_path, "w") as f:
        if session["step"] == 0:
            f.write(str(submit_step0_0))
        elif session["step"] == 1:
            f.write(str(submit_step1_1))
        elif session["step"] == 2:
            f.write(str(submit_step2_2))
        elif session["step"] == 3:
            f.write(str(submit_step3_3))
    print("all CONTT",submit_time)

    #root = os.path.dirname(os.path.abspath(__file__))
    file_name = "object_property_"
    # global step
    # global display_object
    if session["step"] == 0:
        file_name = "object_property_specific_tutorial_obj0_recorder_" +  str(
            session.get("obj_prop_no0"))
    elif session["step"] == 1:
        file_name = "object_property_specific_obj1_" + session["display_object"][session["step"] - 1] + "_" + str(
            session.get("obj_prop_no1"))
        # session["obj_prop_no"]=data["time"]
        # session.modified = True
        # file_name = "object_property_specific_"
    elif session["step"] == 2:
        file_name = "object_property_specific_obj2_" + session["display_object"][session["step"] - 1] + "_" + str(
            session.get("obj_prop_no2"))
    elif session["step"] == 3:
        file_name = "object_property_near_" + str(session.get("obj_prop_no3"))
        # session["obj_prop_no"] = data["time"]
        # session.modified = True
    elif session["step"] == 4:
        file_name = "object_property_far_" + str(session.get("obj_prop_no"))
        # session["obj_prop_no"] = data["time"]
        # session.modified = True
    #property_path = os.path.join(root, "static/causal_graph/", file_name + "_" + session["encoding"] + ".json");
    property_path = os.path.join(root, file_name + "_" + session["encoding"] + ".json");
    # property_path = os.path.join(furnitureloader.furniture_path, "object_property_" + encoding + ".json")

    with open(property_path, "w") as file:
        json.dump(submit_time["cont"], file);

    return "success";
    '''time_path = os.path.join(root,"static/causal_graph/" ,  "submit_time_" + encoding + ".json");
    submit_time = request.get_json()
    with open(time_path, "w") as f:
        f.write(str(submit_time["time"]))
    print(submit_time)
    return "success";'''


@app.route("/record_time_plan", methods=["POST"])
def record_time_plan():
    #global encoding
    #global step
    # global submit_causal_1
    # global submit_causal_2
    # global submit_causal_3
    submit_plan = 0
    # root = os.path.dirname(os.path.abspath(__file__))
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/causal_graph/", session["encoding"])
    if not os.path.exists(root):
        os.makedirs(root)
    submit_time_plan = request.get_json()
    if session["step"] == 0:
        file_name = "causal_specific_tutorial_obj0_recorder_"
        submit_plan = submit_time_plan["time"]
    elif session["step"] == 1:
        file_name = "causal_specific_obj1_" + session["display_object"][session["step"] - 1] + "_"
        submit_plan = submit_time_plan["time"]
    elif session["step"] == 2:
        file_name = "causal_specific_obj2_" + session["display_object"][session["step"] - 1] + "_"
        submit_plan = submit_time_plan["time"]
        # file_name = "causal_specific_"
    elif session["step"] == 3:
        file_name = "causal_near_"
        submit_plan = submit_time_plan["time"]
    # elif step ==4:
    #     file_name = "causal_far_"
    #     submit_causal_3 = submit_time["time"] - submit_causal_1 - submit_causal_2
    time_path = os.path.join(root,  "submit_time_planning_" + file_name + session["encoding"] + ".json")
    with open(time_path, "w") as f:
        f.write(str(submit_plan))
        # if step ==1:
        #     f.write(str(submit_causal_1))
        # elif step==2:
        #     f.write(str(submit_causal_2))
        # elif step == 3:
        #     f.write(str(submit_causal_3))
    print(submit_time_plan)
    return "success";


@app.route("/plan_causal", methods=["POST"])
def plan_causal():
    #global encoding
    # global submit_causal_1
    # global submit_causal_2
    # global submit_causal_3
    #global step
    # root = os.path.dirname(os.path.abspath(__file__))
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/causal_graph/", session["encoding"])
    if not os.path.exists(root):
        os.makedirs(root)
    causal_path = root #os.path.join(root, "static/causal_graph/")
    furniture_path = session["furnitureloader"].furniture_path
    # print(causal_path, plan_object, furniture_path)
    if session["step"] == 0:
        # global submit_causal_1
        plan_name = "plan_specific_tutorial_obj0_recorder" + "_" + str(session["submit_causal_0"]) + "_"
    elif session["step"] == 1:
        # global submit_causal_1
        plan_name = "plan_specific_obj1_" + session["display_object"][session["step"] - 1] + "_" + str(session["submit_causal_1"]) + "_"
    elif session["step"] == 2:
        # global submit_causal_2
        plan_name = "plan_specific_obj2_" + session["display_object"][session["step"] - 1] + "_" + str(session.get("submit_causal_2")) + "_"
        # file_name = "causal_specific_"
    elif session["step"] == 3:
        # global submit_causal_3
        plan_name = "plan_near_" + str(session.get("submit_causal_3")) + "_"
    elif session["step"] == 4:
        plan_name = "plan_far_"
    # plan_path = os.path.join(root, "static/causal_graph/", plan_name + session["encoding"] + ".json")
    plan_path = os.path.join(root, plan_name + session["encoding"] + ".json")
    print("checking session",session["obj_prop_no1"] )

    if session["step"] == 0:
        # global submit_causal_1
        feed_name = "plan_feedback_specific_tutorial_obj0_recorder" + "_" + str(session["submit_causal_0"]) + "_"
    elif session["step"] == 1:
        # global submit_causal_1
        feed_name = "plan_feedback_specific_obj1_" + session["display_object"][session["step"] - 1] + "_" + str(session["submit_causal_1"]) + "_"
    elif session["step"] == 2:
        # global submit_causal_2
        feed_name = "plan_feedback_specific_obj2_" + session["display_object"][session["step"] - 1] + "_" + str(session.get("submit_causal_2")) + "_"
        # file_name = "causal_specific_"
    elif session["step"] == 3:
        # global submit_causal_3
        feed_name = "plan_feedback_near_" + str(session.get("submit_causal_3")) + "_"
    elif session["step"] == 4:
        feed_name = "plan_feedback_far_"
    # plan_path = os.path.join(root, "static/causal_graph/", plan_name + session["encoding"] + ".json")
    feedback_path = os.path.join(root, feed_name + session["encoding"] + ".json")

    #global display_object
    if session["step"] == 0:
        a,f = website_plan(causal_path, causal_path, session["encoding"], "recorder",0,
                         num=session.get("submit_causal_0"),obj_prop_num= session.get("obj_prop_no0"),gen="specific_tutorial")
        with open(plan_path, "w") as file:
            json.dump(a, file)
        print("PRINTING PLAN CAUSAL STUFF ", a)
        with open(feedback_path, "w") as filew:
            json.dump(f, filew)
        return jsonify(
            f)  # jsonify(website_plan(causal_path, causal_path, encoding, display_object[step-1], gen="specific"))
    if session["step"] == 1:
        a,f = website_plan(causal_path, causal_path, session["encoding"], session["display_object"][session["step"] - 1],1,
                         num=session.get("submit_causal_1"),obj_prop_num= session.get("obj_prop_no1"),gen="specific")
        with open(plan_path, "w") as file:
            json.dump(a, file)
        print("PRINTING PLAN CAUSAL STUFF ", a)
        with open(feedback_path, "w") as filew:
            json.dump(f, filew)
        return jsonify(
            f)  # jsonify(website_plan(causal_path, causal_path, encoding, display_object[step-1], gen="specific"))
    if session["step"] == 2:
        a,f = website_plan(causal_path, causal_path, session["encoding"],session["display_object"][session["step"] - 1],2,
                         num=session.get("submit_causal_2"),obj_prop_num= session.get("obj_prop_no2"), gen="specific")
        print("PRINTING PLAN CAUSAL STUFF ", a)
        with open(plan_path, "w") as file:
            json.dump(a, file)
        with open(feedback_path, "w") as filew:
            json.dump(f, filew)
        return jsonify(f)
    if session["step"] == 3:
        b,f = website_plan(causal_path, causal_path, session["encoding"],session["display_object"], 3, num=session.get("submit_causal_3"),obj_prop_num= session.get("obj_prop_no3"),
                         gen="near")
        print("PRINTING PLAN CAUSAL STUFF ", b)
        with open(plan_path, "w") as file:
            json.dump(b, file)
        with open(feedback_path, "w") as filew:
            json.dump(f, filew)
        return jsonify(f)
        # return jsonify(website_plan(causal_path, causal_path, encoding, display_object, gen="near"))
    elif session["step"] == 4:
        c,f = website_plan(causal_path, causal_path, session["encoding"], session["display_object"], num=0,obj_prop_num= 0, gen="far")
        print("PRINTING PLAN CAUSAL STUFF ", c)
        with open(plan_path, "w") as file:
            json.dump(c, file)
        with open(feedback_path, "w") as filew:
            json.dump(f, filew)
        return jsonify(f)
        # return jsonify(website_plan(causal_path, causal_path, encoding, display_object, gen="far"))


if __name__ == '__main__':
    app.run(debug=True)
    # socketio.run(app, debug=True, port=8000)
