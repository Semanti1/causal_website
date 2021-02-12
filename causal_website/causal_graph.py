from graphviz import Digraph
import os
import shutil
import json

all_sentences = [
['property:production', 'keyword:AND', 'property:connection to power source', 'keyword:is/are neccesary for', 'latent:Light'],
['property:stability', 'keyword:AND', 'property:extension', 'keyword:is/are neccesary for', 'latent:Lamp structure'],
["latent:Lamp structure", "keyword:AND", 'latent:Light', 'keyword:is/are neccesary for', 'latent:Lamp'],
]
def check_correctness(sentence):
    #check for syntax error
    #rule1: AND/ OR between properties/latent
    try:
        for idx, field in enumerate(sentence[:-1]):
            name,value = field.split(":")
            # print(value)
            if name == "prop" or name =="lat":
                # print(sentence[idx+1], sentence[idx+1].find("key"))
                if (sentence[idx+1].find("key") == -1):
                    print("error")
                    raise Exception("key word missing")
    except:
        return False
    return True

def check_extend(sentence):
    try:
        for idx, field in enumerate(sentence):
            name,value = feild.split(":")
            if name == "key":
                if (value.find("preferrable") != -1):
                    return True
        return False
    except:
        return False

class CausalGraph():
    def __init__(self, furniture):
        self.x = 0;
        self.furniture = furniture
        self.APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    def process_causal(self, all_sentences):
        #static i = 0;
        dot = Digraph(format="png")
        image_filename = "static/images/output_" + self.furniture + str(self.x) + ".gv";
        image_file = os.path.join(self.APP_ROOT, image_filename)
        for sentence in all_sentences:
            children_list = []
            before_key = True
            optional = False;
            for idx, field in enumerate(sentence):
                name, value = field.split(':')
                if before_key and (name == "prop" or name== "lat" or name =="goal"):
                    children_list.append(value);
                else:
                    if name == "lat" or name =="goal":
                        dot.node(value, label=value, color='red');
                        if optional:
                            for child in children_list:
                                dot.edge(child, value, style="dashed");
                        else:
                            for child in children_list:
                                dot.edge(child, value);
                if name == "key" and value.find("is/are")!=-1:
                    before_key = False;
                if name == "key" and value.find("neccesary")!=-1:
                    optional = False;
                if name == "key" and value.find("preferrable")!=-1:
                    optional = True;


        #print(dot.source)
        dot.render(image_file, view=False)
        # if self.x >=1:
        #     old_image_file = "./static/images/output" + str(self.x-1) + ".gv"
        #     os.remove(old_image_file)
        #     os.remove(old_image_file+".png")
        self.x +=1;
        #dot.save(image_file)
        return image_filename

    def reset(self):
        path = os.path.join(self.APP_ROOT,"static/images/")
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))
        self.x = 0;


class CausalInfo():
    def __init__(self):
        self.graph = {}

    def create_causal_info(self, all_sentences, info_path):
        try:
            self.graph = {}
            for sentence in all_sentences:
                children_list = []
                before_key = True
                for idx, field in enumerate(sentence):
                    name, value = field.split(':')
                    if before_key and (name == "prop" or name== "lat"):
                        if (value not in self.graph):
                            self.graph[value] = []
                        children_list.append(value);
                    else:
                        if name == "lat" or name == "goal":
                            if value not in self.graph:
                                self.graph[value] = []
                            for child in children_list:
                                self.graph[child].append(value);
                    if name == "key" and value.find("is/are")!=-1:
                        before_key = False;

            with open(info_path, "w") as file:
                json.dump(self.graph, file)
            return True;
        except:
            return False;



# causalgraph = CausalGraph();
# causalgraph.process_causal(all_sentences);
