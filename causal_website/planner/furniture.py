import customerrors as err
from abstracttypes import Action, Domain, State, getType, checkPredicateTrue, checkParams, SpecificAction
import random
from visualmodel import FurnitureVisualModel
from object_causalmodel import Function_Causal_Graph, Function_Causal_Node
from copy import deepcopy
import json

class connect(Action):
	def __init__(self, domain):
		super().__init__(domain)
		self.param_types = ["Block", "Block"]
	def causal_predicate(self, b1, b2):
		#return (b1.socket["top_width"] == b2.socket["bottom_width"] and b1.socket["top_width"]!=0) and (b1.connection == b2.connection)
		b2_socket_list = b2.socket_name["bottom"]
		b1_socket_list = b1.socket_name["top"]
		b1_in_b2 = False
		b2_in_b1 = False
		if b1.shape in b2_socket_list:
			b1_in_b2 = True
		if b2.shape in b1_socket_list:
			b2_in_b1 = True
		return b1_in_b2 and b2_in_b1

	@checkParams
	def checkPredicates(self, state, b1_name: str, b2_name: str):
		b1 = state.get(b1_name)
		b2 = state.get(b2_name)
		#specific_action = SpecificAction(self, [b1_name, b2_name], deepcopy(state))

		#clear = (lambda x: x.clear)

		# checkPredicateTrue(clear, b1)
		# checkPredicateTrue(clear, b2)
		clear_b1 = False
		clear_b2 = False
		for c in b1.clear:
			clear_b1 = clear_b1 or c
		for c in b2.clear:
			clear_b2 = clear_b2 or c
		if clear_b1 == False or clear_b2==False:
			raise err.PredicateFailed("no more connection");
		if b2.on != "floor":
			raise err.PredicateFailed("block already in tower")

		#allow multiple tower
		if not(state.no_placement_yet):
			#Check that b1.on != None
			if b1.on == "floor":
				raise err.PredicateFailed("Can only make one tower")

		if b1_name == b2_name:
			raise err.PredicateFailed("Can't connect block on self")

		if not self.causal_predicate(b1, b2):
			raise err.PredicateFailed("Cannot connect");

	@checkParams
	def doAction(self, state, b1_name: str, b2_name: str):
		# self.checkPredicates(state, [b1_name, b2_name])

		b1 = state.get(b1_name)
		b2 = state.get(b2_name)

		# Multi tower enabled
		if b1.on == "floor":
			# Single tower
			state.no_placement_yet = False
			state.total_height += b1.height
			state.tower[b1_name] = [b1]
			b1.on = "floor2"
			b1.tower_name = b1_name

		state.total_height += b2.height
		state.tower[b1.tower_name].append(b2)
		b2.tower_name = b1.tower_name


		for idx, c in enumerate(b1.clear):
			if c:
				b1.clear[idx] = False
				break

		b2.clear = b2.clear
		b2.on = b1_name
		# print("do action: ", b1_name,  b1.clear, b2_name, b2.clear, b_temp.name, b_temp.clear)

class insert(Action):
	def __init__(self, domain):
		super().__init__(domain)
		self.param_types = ["Block", "Block"]

	def causal_predicate(self, b1, b2):
		return b1.socket["top_width"] == b2.socket["bottom_width"] and b1.socket["top_width"] !=0
	@checkParams
	def checkPredicates(self, state, b1_name: str, b2_name: str):
		b1 = state.get(b1_name)
		b2 = state.get(b2_name)
		specific_action = SpecificAction(self, [b1_name, b2_name], deepcopy(state))

		#predicates = self.domain.causal_models[type(specific_action.action).__name__].runModel(specific_action)

		#top basically means clear
		#stacked means
		#Yeah wait with unstack gonna need to change the predicates
		#Stack a on b. Unstack a, now cant stack b on anything because b.stacked is true

		#So you can stack anything that is clear on top of anything that is clear??
		#I think so

		#Predicates, maybe should move them
		# stacked = (lambda x: x.stacked)
		# notstacked = (lambda x: not(x.stacked))
		# top = (lambda x: x.top)
		clear = (lambda x: x.clear)

		checkPredicateTrue(clear, b1)
		checkPredicateTrue(clear, b2)
		if self.causal_predicate(b1, b2)==False:
			raise err.PredicateFailed()


		#Only one tower allowed
		if not(state.no_placement_yet):
			#Check that b1.on != None
			if b1.on == "floor":
				raise err.PredicateFailed("Can only make one tower")

		if b1_name == b2_name:
			raise err.PredicateFailed("Can't insert block on self")


		# Non deterministic stacking
		# print("[" + b1_name + ", " + b2_name + "]")
		# print("Probability of stacking: " + str(state.visual.flatness_vals[b1_name]))
		# if random.random() > state.visual.flatness_vals[b1_name]:
		# 	#Stack should fail
		# 	print("Stacking failed")
		# 	raise err.PredicateFailed("Not stackable enough!")
		# print("Stacking succeeded")

		#Normal
		# if state.visual.getStackability(b1_name, b2_name) < 0.3:
		# # if state.visual.getStackability(b1_name, b2_name) < 0.476:
		# 	raise err.PredicateFailed("Not stackable enough!")



	@checkParams
	def doAction(self, state, b1_name: str, b2_name: str):
		# self.checkPredicates(state, [b1_name, b2_name])

		b1 = state.get(b1_name)
		b2 = state.get(b2_name)

		# Multi tower enabled
		if b1.on == "floor":
			# Single tower
			state.no_placement_yet = False
			state.total_height += b1.height
			state.tower.append(b1)
		# b1.top = False
		# b2.top = True
		# b2.stacked = True
		# b1.stacked = True
		# b2.on = b1_name
		# state.total_weight += b2.weight
		state.total_height += b2.height
		state.tower.append(b2)

		b1.clear = False
		b2.clear = True
		b2.on = b1_name
		state.current_func = b2.function

class stack(Action):
	def __init__(self, domain):
		super().__init__(domain)
		self.param_types = ["Block", "Block"]

	def causal_predicate(self, b1, b2):
		return b1.flatness["top"] and b2.flatness["bottom"]
	@checkParams
	def checkPredicates(self, state, b1_name: str, b2_name: str):
		b1 = state.get(b1_name)
		b2 = state.get(b2_name)
		specific_action = SpecificAction(self, [b1_name, b2_name], deepcopy(state))


		clear = (lambda x: x.clear)

		checkPredicateTrue(clear, b1)
		checkPredicateTrue(clear, b2)
		if self.causal_predicate(b1, b2)==False:
			raise err.PredicateFailed()


		#Only one tower allowed
		if not(state.no_placement_yet):
			#Check that b1.on != None
			if b1.on == "floor":
				raise err.PredicateFailed("Can only make one tower")

		if b1_name == b2_name:
			raise err.PredicateFailed("Can't stack block on self")



	@checkParams
	def doAction(self, state, b1_name: str, b2_name: str):
		# self.checkPredicates(state, [b1_name, b2_name])

		b1 = state.get(b1_name)
		b2 = state.get(b2_name)

		# Multi tower enabled
		if b1.on == "floor":
			# Single tower
			state.no_placement_yet = False
			state.total_height += b1.height
			state.tower.append(b1)

		# b1.top = False
		# b2.top = True
		# b2.stacked = True
		# b1.stacked = True
		# b2.on = b1_name
		#state.total_weight += b2.weight
		state.total_height += b2.height
		state.tower.append(b2)

		b1.clear = False
		b2.clear = True
		b2.on = b1_name
		state.current_func = b2.function



class FurnitureState(State):
	def __init__(self, prop_path, plan_object=None):
		super().__init__()
		# #Normal
		self.all_object = {}
		print(prop_path)

		for object in plan_object:
			if object=="kerosene lamp":
				self.addObjectwithName("fuel tank");
				self.addObjectwithName("burner");
				self.addObjectwithName("chimney");
			elif object == "flashlight":
				self.addObjectwithName("head");
				self.addObjectwithName("batteries");
				self.addObjectwithName("case");
			elif object =="candle":
				self.addObjectwithName("wax");
				self.addObjectwithName("wick");
			elif object =="lamp":
				self.addObjectwithName("base with cables");
				self.addObjectwithName("light bulb");
				self.addObjectwithName("shade");
			elif object == "wall_lamp":
				self.addObjectwithName("backplate");
				self.addObjectwithName("lamp body");
				self.addObjectwithName("light bulb");
			elif object == "oil_lamp":
				self.addObjectwithName("container");
				self.addObjectwithName("wick");
		# if plan_object != None:
		# 	self.addObjectwithName("wax");
		# 	self.addObjectwithName("wick");
		# 	self.addObjectwithName("fuel tank");
		# 	self.addObjectwithName("burner");
		# 	self.addObjectwithName("chimney");
		# 	self.addObjectwithName("head");
		# 	self.addObjectwithName("batteries");
		# 	self.addObjectwithName("case");
		# 	self.addObjectwithName("base with cables");
		# 	self.addObjectwithName("light bulb");
		# 	self.addObjectwithName("shade");

		self.addObjectFromfile(prop_path);

		#print
		print("-----init state--------")
		for key, obj in self.obj_dict.items():
			print(key, obj.function)

		FurnitureVisualModel().initState(self)

		self.tower = {}

		self.current_func = "init"
		self.total_height = 0
		self.no_placement_yet = True


	# def addObjectFromfile(self, file_path):
	# 	try:
	# 		with open(file_path) as f:
	# 			 data = json.load(f)
	# 		obj_prop_dict = {}
	# 		for i in range(int(len(data)/2)):
	# 			obj_name = data[2*i]["value"];
	# 			obj_prop = data[2*i+1]["value"];
	# 			print(obj_name, obj_prop)
	# 			try:
	# 				obj_prop_dict[obj_name].append(obj_prop);
	# 			except KeyError as e:
	# 				obj_prop_dict[obj_name] = [obj_prop];
	# 		for obj_name, obj_prop_list in obj_prop_dict.items():
	# 			block = Block(obj_name, shape=obj_name, func=obj_prop_list, clear=[True]);
	# 			self.all_object[obj_name] = block
	# 			self.addObject(block)
	# 	except Exception as err:
	# 		print("error from addObjectFromfile", err);
	def addObjectFromfile(self, file_path):
		try:
			with open(file_path) as f:
				 data = json.load(f)
			obj_prop_dict = {}
			for i in range(int(len(data)/2)):
				obj_name = data[2*i]["value"];
				obj_prop = data[2*i+1]["value"];
				self.obj_functions.add(obj_prop)
				self.obj_func[obj_prop].append(obj_name)
				print(obj_name, obj_prop)
				try:
					self.obj_dict[obj_name].function.append(obj_prop);
				except KeyError as e:
					block = Block(obj_name, shape=obj_name, func=[obj_prop], clear=[True]);
					self.addObject(block)
		except Exception as err:
			print("error from addObjectFromfile", err);


	def addObjectwithName(self, name):
		block = Block(name, shape=name, func=[], clear=[True])
		self.addObject(block)

	def __eq__(self, other):
		if other == None:
			return False
		# print(self.obj_names, other.obj_names)
		# for objname in self.obj_names:
		# 	if self.get(objname) == other.get(objname):
		# 		pass
		# 	else:
		# 		return False
		#
		# return self.total_height == other.total_height
		
		return str(self.tower) == str(other.tower)


	def __str__(self):
		# ret  = "no place yet: " + str(self.no_placement_yet) + " \n"
		# ret += "function state at: " + str(self.current_func) + "\n"
		# for x in self.objects:
		# 	ret += str(x)
		# return ret
		ret = ""
		for tower_name, tower in self.tower.items():
			for block in tower:
				ret += block.name + "-> "
			ret+= "\n"
		return ret
	def __hash__(self):
		return hash(tuple(self.tower))

	def getShapeDict(self):
		shapedict = {}
		stackarr = self.obj_types["Block"]

		#stackarr get shapes
		for name in stackarr:
			shapedict[name] = self.get(name).shape

		return shapedict

		#T1
		# return self.total_weight > 8

class Furniture(Domain):
	def __init__(self, causal_path, prop_path, plan_object=None):
		super().__init__(FurnitureState(prop_path, plan_object))
		# self.stack = stack(self)
		# self.insert = insert(self)
		self.connect = connect(self)
		self.goal = Goal()
		self.constraint = Constraint()


		# LIGHT = Function_Causal_Node("light", ["CPS", "PD"])
		# LS = Function_Causal_Node("lamp structure", ["STABILITY", "EXTENSION", "PROTECTION"])
		# def light_causal_func(self):
		# 	return self["CPS"] and self["PD"]
		#light_causal_func(self)

		#
		# LIGHT.assign_causal_function(light_causal_func)
		#
		# def LS_causal_func(self):
		# 	return 0.6*self["STABILITY"] + 0.2*self["EXTENSION"] + 0.2*self["PROTECTION"]
		#
		# LS.assign_causal_function(LS_causal_func)
		# self.state.causal_graph = Function_Causal_Graph()
		# self.state.causal_graph.addNode(LIGHT)
		# self.state.causal_graph.addNode(LS)

		# LAMP = Function_Causal_Node("lamp", ["CPS", "PD", "STABILITY", "EXTENSION", "PROTECTION"])
		# def lamp_casual_func(self):
		# 	return 0.2*self["CPS"] + 0.2*self["PD"] + 0.2*self["STABILITY"] + 0.2*self["EXTENSION"] + 0.2*self["PROTECTION"]
		# LAMP.assign_causal_function(lamp_casual_func);
		# self.state.causal_graph = Function_Causal_Graph()
		# self.state.causal_graph.addNode(LAMP)

		self.state.causal_graph = Function_Causal_Graph("Light")
		self.state.causal_graph.addCausalGraphFromfile(causal_path)

		#connect cables to base by default

		# action = SpecificAction(self.connect, ["cable_0", "base_0"], self.state)
		# self.connect.checkPredicates(self.state, ["cable_0", "base_0"])
		# action.action.doAction(self.state, action.parameters)
		# self.state.causal_graph.runModel(self.state, action)
		# #
		# action = SpecificAction(self.connect, ["base_0", "rod_0"], self.state)
		# self.connect.checkPredicates(self.state, ["base_0", "rod_0"])
		# action.action.doAction(self.state, action.parameters)
		# #print("HERE ", self.state)
		# self.state.causal_graph.runModel(self.state, action)
		# #
		# action = SpecificAction(self.connect, ["rod_0", "base_1"], self.state)
		# self.connect.checkPredicates(self.state, ["rod_0", "base_1"])
		# action.action.doAction(self.state, action.parameters)
		# self.state.causal_graph.runModel(self.state, action)
		# print("HERE ", self.state)
		#
		# result = self.connect.checkPredicates(self.state, ["base_1", "rod_1"])
		# print("result", result)
		#
		# action = SpecificAction(self.connect, ["seat", "arm rest"], self.state)
		# self.connect.checkPredicates(self.state, ["seat", "arm rest"])
		# action.action.doAction(self.state, action.parameters)
		# self.state.causal_graph.runModel(self.state, action)
		#
		# action = SpecificAction(self.connect, ["seat", "back frame"], self.state)
		# self.connect.checkPredicates(self.state, ["seat", "back frame"])
		# action.action.doAction(self.state, action.parameters)
		# self.state.causal_graph.runModel(self.state, action)

		#self.goal = Goal(weight=5, height=9)
		print("----causal graph ------")
		print(self.state)
		print("hi")
		print(self.state.causal_graph)

		# self.unstack = unstack(self)
	def isGoalSatisfied(self, state):
		return self.goal.isSatisfied(state)
	def isConstraintSatisfied(self, state):
		return self.constraint.statisfyConstraint(state)

class Block():
	def __init__(self, name, shape, height=0, func=None, clear = [True]):
		self.name = name
		self.clear = clear
		self.on = "floor"
		self.shape = shape
		self.height = height
		self.function = func
		self.tower_name  = "floor"

	def __str__(self):
		return "(" + self.name + ") " + "Clear: " + str(self.clear) + " On: " + str(self.on) + " Function: " + str(self.function) + "\n"

	def __eq__(self, other):
		return (((self.on == other.on)
		and self.clear == other.clear)
		)
	def __hash__(self):
		return hash(self.name)
class Goal():
	def __init__(self):
		self.goal = "lamp"
	def isSatisfied(self, state):
		#define goal reached if there is one base on ground, one rod on base and one light on rod

		# light = state.causal_graph.children_node["light"].properties
		# light_score = light["CPS"] & light["PD"]
		# LS = state.causal_graph.children_node["lamp structure"].properties
		# LS_score =  LS["STABILITY"] ==1 and LS["EXTENSION"] >=1 and LS["PROTECTION"] ==1
		# return light_score and LS_score
		goal_score = state.causal_graph.runModelfromState(state)
		# goal = True
		# b = state.get("base")
		# goal = goal and (b.on == "wheels")
		# b = state.get("rod")
		# goal = goal and (b.on == "base")
		# b = state.get("seat")
		# goal = goal and (b.on == "rod")
		# b = state.get("arm rest")
		# goal = goal and (b.on == "seat")
		# b = state.get("back frame")
		# goal = goal and (b.on == "seat")
		goal = (goal_score >=1)
		return goal
class Constraint():
	def __init__(self):
		self.height = 5
	def statisfyConstraint(self, state):
		return state.total_height > self.height
