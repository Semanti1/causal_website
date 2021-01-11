from graphviz import Digraph
import os
import json

all_sentences = [
['property:production', 'keyword:AND', 'property:connection to power source', 'keyword:is/are neccesary for', 'latent:Light'],
['property:stability', 'keyword:AND', 'property:extension', 'keyword:is/are neccesary for', 'latent:Lamp structure'],
["latent:Lamp structure", "keyword:AND", 'latent:Light', 'keyword:is/are neccesary for', 'latent:Lamp'],
]

class CausalGraph():
    def __init__(self):
        self.x = 0;
    def process_causal(self, all_sentences):
        #static i = 0;
        dot = Digraph(format="png")
        image_file = "static/images/output" + str(self.x) + ".gv"
        for sentence in all_sentences:
            children_list = []
            before_key = True
            for idx, field in enumerate(sentence):
                name, value = field.split(':')
                if before_key and (name == "property" or name== "latent"):
                    children_list.append(value);
                else:
                    if name == "latent":
                        dot.node(value, value);
                        for child in children_list:
                            dot.edge(child, value);
                if name == "keyword" and value.find("is/are")!=-1:
                    before_key = False;


        #print(dot.source)
        dot.render(image_file, view=False)
        # if self.x >=1:
        #     old_image_file = "./static/images/output" + str(self.x-1) + ".gv"
        #     os.remove(old_image_file)
        #     os.remove(old_image_file+".png")
        self.x +=1;
        #dot.save(image_file)
        return image_file
#

class CausalInfo():
    def __init__(self):
        self.graph = {}

    def create_causal_info(self, all_sentences, info_path):
        for sentence in all_sentences:
            children_list = []
            before_key = True
            for idx, field in enumerate(sentence):
                name, value = field.split(':')
                if before_key and (name == "property" or name== "latent"):
                    if (value not in self.graph):
                        self.graph[value] = []
                    children_list.append(value);
                else:
                    if name == "latent":
                        if value not in self.graph:
                            self.graph[value] = []
                        for child in children_list:
                            self.graph[child].append(value);
                if name == "keyword" and value.find("is/are")!=-1:
                    before_key = False;

        with open(info_path, "w") as file:
            json.dump(self.graph, file)


causalgraph = CausalGraph();
causalgraph.process_causal(all_sentences);
