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
    #rule2: No necessary/preferrable
    extend_word = 0;
    try:
        for idx, field in enumerate(sentence[:-1]):
            name,value = field.split(":")
            # print(value)
            if name == "prop" or name =="lat":
                # print(sentence[idx+1], sentence[idx+1].find("key"))
                if (sentence[idx+1].find("key") == -1):
                    return "missing keyword"
            if name == "key":
                if value.find("is/are") !=-1:
                    extend_word +=1;
        if extend_word ==0:
            return "no necessary/preferrable is specified"

    except:
        return "error"
    return "success"

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
                    if name=="prop":
                        dot.node(value, label=value, color='blue');
                else:
                    if name == "lat" or name =="goal":
                        if name=="lat":
                            dot.node(value, label=value, color='grey');
                        if name=="goal":
                            dot.node(value, label=value, color="red");
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
        self.reverse_graph = {}

    def create_causal_info(self, all_sentences, info_path):
        try:
            self.graph = {}
            self.reverse_graph = {}
            syntax_error = False

            for sentence in all_sentences:
                children_list = []
                before_key = True
                syntax_error = check_correctness(sentence);
                if syntax_error == False:
                    return 3; #status code3: syntax error
                for idx, field in enumerate(sentence):
                    name, value = field.split(':')
                    if before_key and (name == "prop" or name== "lat"):
                        if (value not in self.graph):
                            self.graph[value] = []
                        children_list.append(value);
                    else:
                        if (name == "lat") or (name == "goal"):
                            if value not in self.graph:
                                self.graph[value] = []
                                self.reverse_graph[value] = []
                            for child in children_list:
                                self.graph[child].append(value);
                                self.reverse_graph[value].append(child);
                    if name == "key" and value.find("is/are")!=-1:
                        before_key = False;

            leaf_node_count = 0;
            for key, val in self.graph.items():
                if len(val) == 0:
                    leaf_node_count +=1
            if leaf_node_count !=1:
                return 2; #status code 2: more than 1 leaf node
            else:
                with open(info_path, "w") as file:
                    json.dump(self.graph, file)
                return 0; # status code 0: success
        except:
            return 1; # status code 1: exception happened



# causalgraph = CausalGraph();
# causalgraph.process_causal(all_sentences);
