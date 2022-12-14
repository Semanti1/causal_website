import random
from visualmodel import BlockVisualModel
import sys
import numpy as np
from abc import ABC, abstractmethod
import sys
import json
import collections
from causal_graph import CausalGraph

# import pypddl_parser as p1
from abstracttypes import SpecificAction, Action

# This superclass maintains a list of objects and their names in a domain state
# The model looks like:
# Init -> power_out -> conduct -> produce
# class Function(ABC):
# 	def __init__(self, obj):
# 		if obj is not None:
# 			self.name = obj.function
# 		else:
# 			self.name = "init"
# 		self.objects = []
# 		self.next_func = None
# 	def __str__(self):
# 		ret = "function of " + self.name +" has following objects: \n"
# 		for obj in self.objects:
# 			ret+= obj + ", "
# 		ret += "\n"
# 		return ret
# #THIS CAUSAL MODEL WILL TAKE HUMAN COMMAND AND GENERATE FUNCTIONAL CAUSAL GRAPH FOR THE STATE
# class Function_Causal():
# 	def __init__(self):
# 		self.obj_func = {}
#
# 	def initModel(self, state):
# 		self.obj_func["init"] = Function(None)
# 		for obj in state.objects:
# 			try:
# 				self.obj_func[obj.function].objects.append(obj.name)
# 			except KeyError as e:
# 				self.obj_func[obj.function] = Function(obj)
# 				self.obj_func[obj.function].objects.append(obj.name)
#
# 	def add_connect(self, obj1, obj2):
# 		#human commands combine obj2 to obj1
# 		if self.obj_func["init"].next_func is None:
# 			self.obj_func["init"].next_func = obj1.function
# 		self.obj_func[obj1.function].next_func = obj2.function
#
# 	def __str__(self):
# 		ret = "Function_Causal: \n"
# 		for key, val in self.obj_func.items():
# 			ret += str(val)
# 		return ret


class Function_Causal_Node():
	def __init__(self, name, param=[]):
		self.name = name
		self.causal_function = None
		self.properties = {p: 0 for p in param}
		self.children_node = [] #cause node_name
		self.parent_node = [] # effect
		self.neighbor_node = [] #common causes
		self.value = 0
		# self.latent= latent
	def assign_causal_function(self, func):
		self.causal_function = func
	# def run_causal_function(self, state, parameters):
	# 	#parameter: obj1, obj2..
	# 	properties = state.causal_graph.children_node[self.name].properties
	# 	if state.current_func == "init":
	# 		for param in parameters:
	# 			for func in state.obj_dict[param].function:
	# 				if properties.get(func) is not None:
	# 					properties[func] =1
	# 				else:
	# 					continue
	#
	# 	else:
	# 		for func in state.obj_dict[parameters[1]].function:
	# 			if properties.get(func) is not None:
	# 				properties[func] +=1
	# 			else:
	# 				continue
	# 	#run causal function for latent casal nodes:
	# 	# if self.latent ==True:
	# 	# 	self.value = self.causal_function(properties)
		# self.value = self.causal_function(properties)
		# print(self.name, self.properties, self.value, parameters)
		# return self.value
	def get_causal_score(self, state):
		return self.value


class Function_Causal_Graph():
	def __init__(self, goal):
		self.value = 0
		self.all_graph = []
		self.all_nodes = []
		self.coef_map = collections.defaultdict(dict)
		#self.causal_graph = CausalGraph()
		self.goal_name = goal

	def addNode(self, causal_node):
		self.all_node[causal_node.name] = causal_node
	def addCausalGraphFromfile(self, filepath):
		try:
			with open(filepath) as f:
				data = json.load(f)
			#self.causal_graph.show(data)
			#swap between parent and children
			# causal_dict = {}
			# for parent, children in data.items():
			# 	for child in children:
			# 		try:
			# 			causal_dict[child].append(parent)
			# 		except KeyError:
			# 			causal_dict[child] = [parent]
			for graph in data:
				causal_graph = {}
				nodes_dict = {}
				for parent, children in graph.items():
					causal_node = Function_Causal_Node(name=parent);
					#print("parent: ", parent)
					all_children = [child_pair[0] for child_pair in children]
					for child_pair in children:
						#print("child: ", child_pair)
						child, coef = child_pair
						if child not in nodes_dict:
							new_node = Function_Causal_Node(name=child);
							new_node.neighbor = all_children
							new_node.parent_node.append(parent)
							nodes_dict[new_node.name] = new_node
							causal_graph[new_node.name] = new_node
						else:
							child_node = nodes_dict[child]
							child_node.parent_node.append(parent)
							child_node.neighbor = all_children


						self.coef_map[parent][child] = coef;
						causal_node.children_node.append(child)


					# self.addNode(causal_node)
					nodes_dict[causal_node.name] = causal_node
					causal_graph[causal_node.name] = causal_node
					self.all_graph.append(causal_graph)
					self.all_nodes.append(nodes_dict)
		except Exception as err:
			print("error from addCausalGraphFromfile: ", err);


	def subtreeUtil(self, root, nodes_dict, state):
		if(len(root.children_node) ==0):
			return root.value;
		value = 1
		all_plus = True
		coef_sum = 0;
		for child in root.children_node:
			coef = self.coef_map[root.name][child]
			if coef !=-1:
				coef_sum += coef

		for child in root.children_node:
			#print("child: ", child.name, child.value)
			coef = self.coef_map[root.name][child]
			if coef == -1:
				value *=  self.subtreeUtil(nodes_dict[child], nodes_dict, state);
				all_plus=False;
			elif coef == 1:
				value += self.subtreeUtil(nodes_dict[child], nodes_dict, state)
			# 	all_plus=False
			else:
				value += (coef/coef_sum) * self.subtreeUtil(nodes_dict[child], nodes_dict, state)
		if root.name in state.obj_functions: #if the current node is a function node, then need to check if its parents =1 and itself=1
			value *= root.value
		else:
			value = value

		if all_plus:
			root.value = value-1;
		else:
			root.value = value
		return root.value

	def runModel(self, state, action):
		try:
			for param in action.parameters:
				for func in state.obj_dict[param].function:
					for i in range(len(self.all_nodes)):
						if func in self.all_nodes[i]:
							self.all_nodes[i][func].value = 1
			# print("----state function-------")
			# for node in self.all_nodes:
			# 	for func, func_node in node.items():
			# 		print(func, func_node.value)

			for idx, graph in enumerate(self.all_graph):
				value = self.subtreeUtil(graph[self.goal_name], self.all_nodes[idx], state);
				if(value > self.value):
					self.value = value
			print("run model: ", self.value, action)
			return self.value
		except Exception as err:
			print("error from runModel: ", err)

	def runModelfromState(self, state):
		for tower_name, tower in state.tower.items():
			for block in tower:
				for func in state.obj_dict[block.name].function:
					for i in range(len(self.all_nodes)):
						if func in self.all_nodes[i]:
							self.all_nodes[i][func].value = 1
		for idx, graph in enumerate(self.all_graph):
			value = self.subtreeUtil(graph[self.goal_name], self.all_nodes[idx], state);
			if(value > self.value):
				self.value = value;
			# print("run model: ", self.value, action)
		return self.value


	def getScore(self):
		return self.value

	# def __str__(self):
	# 	ret = ""
	# 	for graph in self.all_graph:
	# 		for key, nodes in graph.items():
	# 			if len(nodes.children_node) !=0:
	# 				ret += nodes.name + " \t value: " + str(nodes.value) + "\n\t"
	# 			for cn in nodes.children_node:
	# 				ret+=str(graph[cn].name)+ " : " + str(graph[cn].value)  + " coef: " + str(self.coef_map[nodes.name][cn])+ "\n\t"
	# 			ret +="\n"
	# 	return ret

	def __str__(self):
		ret = ""
		for nodes in self.all_nodes:
			for name, node in nodes.items():
				ret += name + "\t \n"
				ret += "children node: "
				for child in node.children_node:
					ret+= child +"\t"
				ret += "\n neighboring node: "
				for neigh in node.neighbor_node:
					ret += neigh + "\t"
				ret += "\n parent node: "
				for par in node.parent_node:
					ret += par + "\t"
				ret += "\n\n"
		return ret