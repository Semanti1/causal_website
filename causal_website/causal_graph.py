from graphviz import Digraph
from time import sleep
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
                        return "missing AND"
        else:
            for idx, field in enumerate(sentence[:-1]):
                name, value = field.split(":")
                if name =="prop" or name =="lat":
                    if(sentence[idx+1].find("score") != -1):
                        if(sentence[idx+2].find("key") ==-1):
                            return "missing AND"
    except:
        return "error"
    return "success"

def check_optional_new(sentence):
    valid = 0;
    extend_word = 0
    print("HELLO")
    mult = False
    dict = {}
    firstid=-1
    for idx, field in enumerate(sentence):
        name, value = field.split(":")
        if name == "key" and value.find("is/are") != -1:
            if firstid==-1:
                firstid = idx
            extend_word +=1
            if idx!=len(sentence)-2:
                if idx<(len(sentence)-1):
                    valid = 1
                if idx==(len(sentence)-1):
                    valid = 2
        if name=="prop":
            if value in dict:
                dict[value] += 1
                mult = True
            else:
                dict[value] = 1
    return valid, extend_word, mult,firstid

def check_correctness_new(sentence):
    #check for syntax error
    #rule1: AND/ OR between properties/latent
    #rule2: No necessary/preferrable
    try:
        #optional or not
        errors=[]
        print("SENTENCE", sentence)
        valid, extend_word, mult, firstid = check_optional_new(sentence)
        print(valid, extend_word, mult)
        if extend_word ==0:
            errors.append("All causal rules must include one “is/are necessary for causing” element. No \"is/are necessary for causing” found")
        if extend_word>1:
            errors.append("Only one “is/are necessary for causing” element can exist in a single causal rule.Multiple \"is/are necessary for causing” found")
        goalct = 0
        for idx, field in enumerate(sentence[:-1]):
        #for idx, field in enumerate(sentence):
            name, value = field.split(":")
            # print(value)
            if name == "prop" or name == "lat":
                # print(sentence[idx+1], sentence[idx+1].find("key"))
                if (sentence[idx + 1].find("key") == -1):
                    if idx<firstid:
                        errors.append(
                            "Multiple terms on the left-hand side of “is/are necessary for causing” must be connected by “AND”. Missing \"AND\"")
            if name == "key":
                # print(sentence[idx+1], sentence[idx+1].find("key"))
                if (sentence[idx + 1].find("key") != -1):
                    errors.append("Two keywords cannot exist side-by-side. \"AND\" should be used between two object functions.The keyword “is/are necessary for causing” can be used between two object functions or between an object function and the goal. Two adjacent keywords have been detected")

            if name== "goal":
                goalct +=1
        keyg, valg = (sentence[-1]).split(':')
        if keyg == "goal":
            goalct+=1
        if goalct>0:
            if goalct>1:
                errors.append("The goal node can be used only once in a causal rule. Multiple goal nodes detected")
            # keyg, valg = (sentence[-1]).split(':')
            if keyg!="goal":
                errors.append("The goal specified is not at the end of the causal rule")
        print("GOAL CT",goalct)

        if valid==1:
            errors.append("Each causal rule can only have one term on the right side of “is/are necessary for causing” element. More than one element to the right of “is/are necessary for causing” has been detected")
        if valid==2:
            errors.append("Each causal rule should have one term on the right side of “is/are necessary for causing” element. No element to the right of “is/are necessary for causing” has been detected")
        if mult:
            errors.append("Each function can appear atmost once in a causal rule. A function cannot cause itself or be ANDed to itself. Please check for repeated elements")
        print(errors)
        if len(errors)>0:
            return errors
    except Exception as err:
        print(err)
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
        print("ALL SENTENCESsssssss  ", all_sentences)
        for model in all_sentences:
            print("MODELLLLLLLLLLL  ", model)
            reverse_graph = {}
            success_code = self.create_single_causal_info(model, reverse_graph)
            print("SUCCESS CODE", success_code)
            if len(success_code)==1 and success_code[0]==6:
                if len(model)>1:
                    err= ["Goal node not present at the end of the last causal rule"];
                else:
                    err= ["Goal node not present at the end of the causal rule"];
                with open(info_path, "w") as file:
                    #json.dump(syntax_error, file)
                    json.dump(err,file)
                return err#success
            all_errors=[]
            sum_all=sum(sum(l) if isinstance(l,list) else l for l in success_code)
            if sum_all!=0:
                for rulenum,successes in enumerate(success_code):

                    syntax_error=""
                    if isinstance(successes,list):
                        for success in list(set(successes)):
                            if success !=0:
                                if success == 1:
                                    # syntax_error="There is an error on the server end to save the causal model. Please report this to the developer."
                                    syntax_error = "Some of your causal rules have errors."
                                elif success == 2:
                                    syntax_error="All nodes must be connected to the goal node directly or indirectly"
                                elif success == 8:
                                    syntax_error="There are syntax error in your causal rules #"+str(rulenum+1)
                                elif success == 7:
                                    syntax_error="Multiple terms on the left-hand side of “is/are necessary for causing” must be connected by “AND”. Missing \"AND\" in causal rule# "+str(rulenum+1)
                                elif success == 3:
                                    syntax_error= "All causal rules must include one “is/are necessary for causing” element. No \"is/are necessary for causing found in causal rule# "+str(rulenum+1)
                                elif success == 4:
                                    syntax_error = "Object property cannot be used as effect"
                                elif success == 5:
                                    syntax_error="Effect nodes must be caused by at least one of the functions"
                                elif success == 6:
                                    syntax_error="Goal node not present"
                                elif success== 9:
                                    syntax_error="Only one “is/are necessary for causing” element can exist in a single causal rule.Multiple \"is/are necessary for causing” found in causal rule# "+str(rulenum+1)
                                elif success==10:
                                    syntax_error="Each causal rule can only have one term on the right side of “is/are necessary for causing” element. More than one element to the right of “is/are necessary for causing” has been detected in causal rule# "+str(rulenum+1)
                                elif success==12:
                                    syntax_error="Each causal rule should have one term on the right side of “is/are necessary for causing” element. No element to the right of “is/are necessary for causing” has been detected in causal rule# "+str(rulenum+1)
                                elif success==13:
                                    syntax_error="Two keywords cannot exist side-by-side. \"AND\" should be used between two object functions.The keyword “is/are necessary for causing” can be used between two object functions or between an object function and the goal. Two adjacent keywords have been detected in causal rule#"+str(rulenum+1)
                                elif success==14:
                                    syntax_error="The goal node can be used only once in a causal rule. Multiple goal nodes detected in causal rule# "+str(rulenum+1)
                                elif success==15:
                                    syntax_error="The goal specified is not at the end of the causal rule in rule#"+str(rulenum+1)
                                elif success==11:
                                    syntax_error="Each function can appear atmost once in a causal rule. A function cannot cause itself or be ANDed to itself. Please check for repeated elements in causal rule#"+str(rulenum+1)
                            if syntax_error!="":
                                all_errors.append(syntax_error+"\n")
                    else:
                        if successes != 0:
                            if successes == 1:
                                # syntax_error="There is an error on the server end to save the causal model. Please report this to the developer."
                                syntax_error = "Some of your causal rules have errors."
                            elif successes == 2:
                                syntax_error = "All nodes must be connected to the goal node directly or indirectly"
                            elif successes == 8:
                                syntax_error = "There are syntax error in your causal rules #" + str(rulenum + 1)
                            elif successes == 7:
                                syntax_error = "Multiple terms on the left-hand side of “is/are necessary for causing” must be connected by “AND”. Missing \"AND\" in causal rule# " + str(
                                    rulenum + 1)
                            elif successes == 3:
                                syntax_error = "All causal rules must include one “is/are necessary for causing” element. No \"is/are necessary for causing found in causal rule# " + str(
                                    rulenum + 1)
                            elif successes == 4:
                                syntax_error = "Object property cannot be used as effect"
                            elif successes == 5:
                                syntax_error = "Effect nodes must be caused by at least one of the functions"
                            elif successes == 6:
                                syntax_error = "Goal node not present"
                            elif successes == 9:
                                syntax_error = "Only one “is/are necessary for causing” element can exist in a single causal rule.Multiple \"is/are necessary for causing” found in causal rule# " + str(
                                    rulenum + 1)
                            elif successes == 10:
                                syntax_error = "Each causal rule can only have one term on the right side of “is/are necessary for causing” element. More than one element to the right of “is/are necessary for causing” has been detected in causal rule# " + str(
                                    rulenum + 1)
                            elif successes == 11:
                                syntax_error = "Each function can appear atmost once in a causal rule. A function cannot cause itself or be ANDed to itself. Please check for repeated elements in causal rule#" + str(
                                    rulenum + 1)
                            elif successes==12:
                                syntax_error = "Each causal rule should have one term on the right side of “is/are necessary for causing” element. No element to the right of “is/are necessary for causing” has been detected in causal rule# " + str(
                                    rulenum + 1)
                            elif successes==13:
                                syntax_error = "Two keywords cannot exist side-by-side. \"AND\" should be used between two object functions.The keyword “is/are necessary for causing” can be used between two object functions or between an object function and the goal. Two adjacent keywords have been detected in causal rule#"+str(rulenum+1)
                            elif successes==14:
                                syntax_error = "The goal node can be used only once in a causal rule. Multiple goal nodes detected in causal rule# " + str(
                                    rulenum + 1)
                            elif successes==15:
                                syntax_error = "The goal specified is not at the end of the causal rule in rule#" + str(
                                    rulenum + 1)

                        if syntax_error != "":
                            all_errors.append(syntax_error + "\n")

                with open(info_path, "w") as file:
                    #json.dump(syntax_error, file)
                    json.dump(all_errors,file)
                return all_errors#success
            all_graph.append(reverse_graph)
        with open(info_path, "w") as file:
            json.dump(all_graph, file)
        print("dumped")
        #sleep(5)
        return "successfully saved the causal model."
        #return success_final

    def create_single_causal_info(self, all_sentences, reverse_graph):
        try:
            self.graph = {}
            self.reverse_graph = {}
            error_codes_all=[]
            syntax_error = False
            goal,gname = (all_sentences[-1][-1]).split(':')
            if goal!="goal":
                error_codes_all.append(6)
                return error_codes_all

                #return 6
            for sentence in all_sentences:
                print("Singleeeeee SENTENCE  ", sentence)
                children_list = []
                error_codes=[]
                before_key = True
                syntax_error = check_correctness_new(sentence);
                print("SYNTAX ERROR", syntax_error)
                if syntax_error != "success":
                    if isinstance(syntax_error,list):
                        for err in syntax_error:
                            #print(syntax_error)
                            if (err=="All causal rules must include one “is/are necessary for causing” element. No \"is/are necessary for causing” found"):
                                #return 3 #status code3: syntax error
                                error_codes.append(3)
                            elif (err=="Multiple terms on the left-hand side of “is/are necessary for causing” must be connected by “AND”. Missing \"AND\""):
                                error_codes.append(7)
                                #return 7
                            elif (err=="Only one “is/are necessary for causing” element can exist in a single causal rule.Multiple \"is/are necessary for causing” found"):
                                error_codes.append(9)
                            elif(err=="Each causal rule can only have one term on the right side of “is/are necessary for causing” element. More than one element to the right of “is/are necessary for causing” has been detected"):
                                error_codes.append(10)
                            elif(err=="Each function can appear atmost once in a causal rule. A function cannot cause itself or be ANDed to itself. Please check for repeated elements"):
                                error_codes.append(11)
                            elif(err=="Each causal rule should have one term on the right side of “is/are necessary for causing” element. No element to the right of “is/are necessary for causing” has been detected"):
                                error_codes.append(12)
                            elif(err=="Two keywords cannot exist side-by-side. \"AND\" should be used between two object functions.The keyword “is/are necessary for causing” can be used between two object functions or between an object function and the goal. Two adjacent keywords have been detected"):
                                error_codes.append(13)
                            elif(err=="The goal node can be used only once in a causal rule. Multiple goal nodes detected"):

                                error_codes.append(14)
                            elif(err=="The goal specified is not at the end of the causal rule"):
                                error_codes.append(15)
                            else:
                                error_codes.append(8)
                    else:
                        error_codes.append(8)
                        #return 8
                else:
                    error_codes.append(0)
                error_codes_all.append(error_codes)
                # optional,_ = check_optional(sentence);
                # for idx, field in enumerate(sentence):
                #     name, value = field.split(':')
                #     if before_key and (name == "prop" or name== "lat"):
                #         if (value not in self.graph):
                #             self.graph[value] = []
                #             self.reverse_graph[(value, name)] = []
                #         children_list.append((value, idx+1));
                #     else:
                #         if (name == "lat") or (name == "goal") or (name =="prop"):
                #             if value not in self.graph:
                #                 self.graph[value] = []
                #                 reverse_graph[value] = []
                #                 self.reverse_graph[(value, name)] = []
                #             for child in children_list:
                #                 self.graph[child[0]].append(value);
                #                 if optional:
                #                     score = int(sentence[child[1]].split(":")[1]);
                #                     reverse_graph[value].append((child[0], score))
                #                     self.reverse_graph[(value,name)].append((child[0], score));
                #                 else:
                #                     reverse_graph[value].append((child[0], -1));
                #                     self.reverse_graph[(value, name)].append((child[0], -1));
                #         # if(name == "prop"):
                #         #     return 4; # status code 4: function is used as intermidate effect
                #     if name == "key" and value.find("is/are")!=-1:
                #         before_key = False;

            # leaf_node_count = 0;
            # for key, val in self.graph.items():
            #     print(key, val)
            #     if len(val) == 0:
            #         leaf_node_count +=1
            # if leaf_node_count !=1:
            #     error_codes.append(2)
            #     #return 2; #status code 2: more than 1 leaf node
            # for key, val in self.reverse_graph.items():
            #     if len(val) == 0:
            #         name = key[1]
            #         if name == "lat":
            #             error_codes.append(5)
            # if goal!="goal":
            #     error_codes.append(6)
            sum_all = sum(sum(l) if isinstance(l, list) else l for l in error_codes_all)
            if sum_all==0:
                for sentence in all_sentences:
                    print("Singleeeeee SENTENCE  ", sentence)
                    children_list = []
                    before_key = True
                    optional, _ = check_optional(sentence);
                    for idx, field in enumerate(sentence):
                        name, value = field.split(':')
                        if before_key and (name == "prop" or name == "lat"):
                            if (value not in self.graph):
                                self.graph[value] = []
                                self.reverse_graph[(value, name)] = []
                            children_list.append((value, idx + 1));
                        else:
                            if (name == "lat") or (name == "goal") or (name == "prop"):
                                if value not in self.graph:
                                    self.graph[value] = []
                                    reverse_graph[value] = []
                                    self.reverse_graph[(value, name)] = []
                                for child in children_list:
                                    self.graph[child[0]].append(value);
                                    if optional:
                                        score = int(sentence[child[1]].split(":")[1]);
                                        reverse_graph[value].append((child[0], score))
                                        self.reverse_graph[(value, name)].append((child[0], score));
                                    else:
                                        reverse_graph[value].append((child[0], -1));
                                        self.reverse_graph[(value, name)].append((child[0], -1));
                            # if(name == "prop"):
                            #     return 4; # status code 4: function is used as intermidate effect
                        if name == "key" and value.find("is/are") != -1:
                            before_key = False;
                        #return 5; #status code 5: effect node cannot be leaf node
                # error_codes.append(0)
                leaf_node_count = 0;
                for key, val in self.graph.items():
                    print("HHHHHHEEEEEEEEEEEEEEEEELLLLLLLLLLOOOOOOOOOOOOOOOOO")
                    print("key", key, "val", val)
                    if len(val) == 0:
                        leaf_node_count += 1
                    print("leaf node", leaf_node_count)
                if leaf_node_count != 1:
                    error_codes_all.append(2)
                    # return 2; #status code 2: more than 1 leaf node
                for key, val in self.reverse_graph.items():
                    if len(val) == 0:
                        name = key[1]
                        if name == "lat":
                            error_codes_all.append(5)
            return error_codes_all
            #return 0; # status code 0: success
        except Exception as err:
            print("EXCEPTION")
            print("exception in create_single_causal_info: ", err)
            error_codes_all.append(1)
            return error_codes_all
            #return 1; # status code 1: exception happened



causalgraph = CausalInfo();
val = causalgraph.create_single_causal_info(all_sentences, {});
print(val)
