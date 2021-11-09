from graphviz import Digraph
import os
import shutil
import json

all_sentences = [
['prop:provide fuel',  'key:is/are neccesary for causing', 'prop:feul to heat'],
['prop:feul to heat',  'key:is/are neccesary for causing', 'goal:light'],
]

def check_optional(sentence):
    optional = False;
    extend_word = 0
    for idx, field in enumerate(sentence):
        name, value = field.split(":")
        if name == "key" and value.find("is/are") != -1:
            extend_word +=1
            if value.find("preferrable") != -1:
                optional = True

    return optional, extend_word

def check_correctness(sentence):
    #check for syntax error
    #rule1: AND/ OR between properties/latent
    #rule2: No necessary/preferrable
    try:
        #optional or not
        optional, extend_word = check_optional(sentence);
        if extend_word ==0:
            return "no necessary/preferrable is specified"

        if not optional:
            for idx, field in enumerate(sentence[:-1]):
                name,value = field.split(":")
                # print(value)
                if name == "prop" or name =="lat":
                    # print(sentence[idx+1], sentence[idx+1].find("key"))
                    if (sentence[idx+1].find("key") == -1):
                        return "missing AND/OR"
        else:
            for idx, field in enumerate(sentence[:-1]):
                name, value = field.split(":")
                if name =="prop" or name =="lat":
                    if(sentence[idx+1].find("score") != -1):
                        if(sentence[idx+2].find("key") ==-1):
                            return "missing AND/OR"
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
        all_causal_graph_path = []
        for idx, line in enumerate(all_sentences):
            image_path = self.process_causal_single(line, idx);
            all_causal_graph_path.append(image_path);
        return all_causal_graph_path;

    def process_causal_single(self, all_sentences, index):
        #static i = 0;
        dot = Digraph(format="png")
        image_filename = "static/images/output_" + self.furniture + str(index)+ "_" + str(self.x) + ".gv";
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
                    if name == "lat" or name =="goal" or name =="prop":
                        if name=="lat":
                            dot.node(value, label=value);
                        if name=="goal":
                            dot.node(value, label=value, color="red");
                        if name=="prop":
                            dot.node(value, label=value, color="blue")
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
        success_final = 0
        all_graph = []
        for model in all_sentences:
            reverse_graph = {}
            success = self.create_single_causal_info(model, reverse_graph)
            if success !=0:
                return success
            all_graph.append(reverse_graph)
        with open(info_path, "w") as file:
            json.dump(all_graph, file)
        return success_final;

    def create_single_causal_info(self, all_sentences, reverse_graph):
        try:
            self.graph = {}
            self.reverse_graph = {}
            syntax_error = False

            for sentence in all_sentences:
                children_list = []
                before_key = True
                syntax_error = check_correctness(sentence);
                if syntax_error != "success":
                    print(syntax_error)
                    return 3; #status code3: syntax error

                optional,_ = check_optional(sentence);
                for idx, field in enumerate(sentence):
                    name, value = field.split(':')
                    if before_key and (name == "prop" or name== "lat"):
                        if (value not in self.graph):
                            self.graph[value] = []
                            self.reverse_graph[(value, name)] = []
                        children_list.append((value, idx+1));
                    else:
                        if (name == "lat") or (name == "goal") or (name =="prop"):
                            if value not in self.graph:
                                self.graph[value] = []
                                reverse_graph[value] = []
                                self.reverse_graph[(value, name)] = []
                            for child in children_list:
                                self.graph[child[0]].append(value);
                                if optional:
                                    score = int(sentence[child[1]].split(":")[1]);
                                    reverse_graph[value].append((child[0], score))
                                    self.reverse_graph[(value,name)].append((child[0], score));
                                else:
                                    reverse_graph[value].append((child[0], -1));
                                    self.reverse_graph[(value, name)].append((child[0], -1));
                        # if(name == "prop"):
                        #     return 4; # status code 4: function is used as intermidate effect
                    if name == "key" and value.find("is/are")!=-1:
                        before_key = False;

            leaf_node_count = 0;
            for key, val in self.graph.items():
                print(key, val)
                if len(val) == 0:
                    leaf_node_count +=1
            if leaf_node_count !=1:
                return 2; #status code 2: more than 1 leaf node
            for key, val in self.reverse_graph.items():
                if len(val) == 0:
                    name = key[1]
                    if name == "lat":
                        return 5; #status code 5: effect node cannot be leaf node

            return 0; # status code 0: success
        except Exception as err:
            print("exception in create_single_causal_info: ", err)
            return 1; # status code 1: exception happened



causalgraph = CausalInfo();
val = causalgraph.create_single_causal_info(all_sentences, {});
print(val)
