from graphviz import Digraph
import os

all_sentences = [
['property:production', 'keyword:AND', 'property:connection to power source', 'keyword:is/are neccesary for', 'latent:Light'],
['property:stability', 'keyword:AND', 'property:extension', 'keyword:is/are neccesary for', 'latent:Lamp structure']
]

class CausalGraph():
    def __init__(self):
        self.x = 0;
    def process_causal(self, all_sentences):
        #static i = 0;
        dot = Digraph(format="png")
        image_file = "static/images/output" + str(self.x) + ".gv"
        for sentence in all_sentences:
            property_list = []
            for field in sentence:
                name, value = field.split(':')
                if name == "property":
                    dot.node(value, value);
                    property_list.append(value);
                if name == "latent":
                    dot.node(value, value);
                    for property in property_list:
                        dot.edge(property, value);
        #print(dot.source)
        dot.render(image_file, view=False)
        if self.x >=1:
            old_image_file = "./static/images/output" + str(self.x-1) + ".gv"
            os.remove(old_image_file)
            os.remove(old_image_file+".png")
        self.x +=1;
        #dot.save(image_file)
        return image_file
#process_causal(all_sentences);
