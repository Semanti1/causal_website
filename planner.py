import inspect
import customerrors
import itertools
from copy import deepcopy
import random
#from causalmodel import CausalModel
from abstracttypes import SpecificAction
import time
import statistics
import numpy as np
import math
from graphviz import Digraph
from itertools import combinations


class Planner():
	class Node():
		def __init__(self, specifiedaction, history):
			self.specifiedaction = specifiedaction
			self.history = history #list of specific action

		def __str__(self):
			return "Action: " + str(self.specifiedaction) + " History: " + str(self.history)

	def __init__(self, domain):
		self.domain = domain
		self.init_state = domain.state
		self.MDP = dict() #mdp[s][a] = [prob, next_state, reward, done]


	def setAlgo(self, algo):
		self.algo = algo

	def plan(self):
		if self.algo == None:
			raise TypeError("Need to set the planning algo first!")
		return self.algo()[0]

	value_graph = Digraph(format="png")
	policy_graph = Digraph(format="png")

	def collectStats(self, num_times):
		plans = {}
		nodes = []
		backtracks = []
		time = []

		for _ in range(num_times):
			res = self.algo()
			plan = tuple(map((lambda x: str(x)), res[0]))
			# print(plan)

			try:
				plans[plan] += 1
			except KeyError as e:
				#We have no record of that plan yet
				plans[plan] = 1



			nodes.append(res[1])
			backtracks.append(res[2])
			time.append(res[3])


		### Implement sorter of plans from most popular to least

		sorted_plans = {k: v for k, v in sorted(plans.items(), key=lambda item: item[1], reverse=True)}

		print()
		print("------- Statistics ------- (" + str(num_times) + " runs)")
		print("All plans: " + str(sorted_plans))
		print("Avg nodes touched: " + str(statistics.mean(nodes)))
		print("Avg backtracks: " + str(statistics.mean(backtracks)))
		print("Avg time: " + str(statistics.mean(time)))


	@staticmethod
	def BFS(self):
		debug = True
		start_time = time.time()
		nodes_touched = 0

		def addNodes(state, history):
			for specifiedaction in self.domain.getValidActions(state):
				next_nodes.append(self.Node(deepcopy(specifiedaction), deepcopy(history)))

		#Initialization
		print("Initializing BFS planner....")

		#A node is an action and a state tuple
		#(action, state)

		#This stores all actions the BFS should go through
		#Can use it as a queue, just append,then pop(0)
		next_nodes = []
		#Add all current possible actions to BFS
		addNodes(self.domain.state, [])

		curr_node = self.Node(SpecificAction(None, None, self.domain.state), [])

		while not(self.domain.isGoalSatisfied(curr_node.specifiedaction.state)):
		# for i in range(2):
			if len(next_nodes) == 0:
				print("failed to generate a plan...")
				break
			curr_node = next_nodes.pop(0)

			# if debug:
			# 	#print(type(curr_node.specifiedaction.action).__name__ + " " + str(curr_node.specifiedaction.parameters))
			# 	print(curr_node.specifiedaction.state)

			nodes_touched += 1
			#Unpack the node into action and parameters
			action = curr_node.specifiedaction
			curr_history = curr_node.history

			action.action.doAction(action.state, action.parameters)

			#Now find all the next possible actions and add them to the actions list
			curr_history.append(action)
			if debug:
				for curr in curr_history:
					print(curr)
				print(curr_node.specifiedaction.state)
			# Planner.printHistory(curr_history)
			addNodes(action.state, curr_history)
			# for nodes in next_nodes:
			# 	print("next nodes")
			# 	print(str(type(nodes.specifiedaction.action).__name__) + " " +str(nodes.specifiedaction.parameters))
			# 	print(nodes.specifiedaction.state)

		print("Nodes touched: " + str(nodes_touched))
		time_taken = time.time() - start_time
		print("--- BFS Planner took %s seconds ---" % (time_taken))
		return [tuple(curr_node.history), nodes_touched, 0, time_taken]

	@staticmethod
	def printHistory(histarr):
		for h in histarr:
			if h.action != None:
				print(str(type(h.action).__name__) + " " +str(h.parameters))

	@staticmethod
	def HistoryString(histarr):
		string = ''
		for h in histarr:
			if h.action != None:
				string += str(type(h.action).__name__) + " " +str(h.parameters) + "\n"
		return string
	# @staticmethod
	# def getStacks(histarr):
	# 	print(histarr)

	# 	stackarr = []
	# 	if len(histarr) <= 2:
	# 		print("Whoops, histarr too small!")

	# 	stackarr.append(histarr[1].parameters[0])
	# 	stackarr.append(histarr[1].parameters[1])

	# 	for x in range(2, len(histarr)):
	# 		h = histarr[x]
	# 		stackarr.append(h.parameters[1])

	# 	return stackarr

	def parseHistorytoList(self, histarr):
		retarr = []
		for h in histarr:
			if h.action != None:
				name = type(h.action).__name__
				retarr.append([type(h.action).__name__, h.parameters])

		return retarr

	def MDP_Init(self):
		try:
			queue = []
			queue.append([self.domain.state, None, None])
			done = False
			while(len(queue) > 0):
				state, prev_action, prev_score = queue.pop(0)
				self.value_graph.node(str(state), label=str(state) + str(prev_score))
				self.MDP[state] = dict()
				valid_actions = self.domain.getValidActions(state)
				done = self.domain.isGoalSatisfied(state)
				score = state.causal_graph.getScore()
				# if done:
				# 	print("done")
				# 	print(state)

				if len(valid_actions) ==0 :
					if not done:
						self.MDP[state][0] = [1, 0, -10, 0]
						self.value_graph.node(str(state), label=str(state) + str(-10))
					else:
						self.MDP[state][0] = [1, 0, 10, 1]
						self.value_graph.node(str(state), label=str(state) + str(10))

					continue

				for action in valid_actions:
					#print("valid action: ", action)
					score = action.state.causal_graph.runModel(action.state, action)
					done = self.domain.isGoalSatisfied(action.state)
					#print(action, action.state.causal_graph, done)
					action.action.doAction(action.state, action.parameters)
					self.value_graph.edge(str(state), str(action.state))

					#next_valid_actions = self.domain.getValidActions(action.state)
					#print(len(next_valid_actions), action.state	)
					if done:
						score = 10
					self.MDP[state][action] = [1, action.state, score, done ]
					# if not (action.state in self.MDP):
					queue.append([action.state, action, score])
				#print("\n")
			# self.value_graph.render("image", view=True)
			#print("Printing MDP","\n")
			#print(self.MDP)
		except Exception as err:
			print("MDP_Init error: ", err);


		 #TESTING:
		print("Printing MDP","\n")
		for state, action_next_state in self.MDP.items():
			#print(state.causal_graph)
			
			for action, next_state in self.MDP[state].items():
				print('state')
				print (str(state))
				[prob, ns, reward, done] = next_state
				print('action nd next state')
				print(action, prob,str(ns), reward, done)


	def policy_iteration(self):
		try:
			policy = []
			v_old = dict() #dict[state] = value
			discount_factor = 0.4
			#initilize value
			for state, _ in self.MDP.items():
				v_old[state] = 0

			while True:
				delta = 0
				v_new = dict()
				for state , action_next_state in self.MDP.items():
					v_f = 0
					v_list = []
					for action, next_state in self.MDP[state].items():
						[prob, ns, reward, done] = next_state
						if ns not in v_old.keys(): # termination state
							v_f = prob * (reward)
						else:
							v_f = prob * (reward + discount_factor * v_old[ns])
						v_list.append(v_f)
					delta = max(delta, abs(max(v_list) - v_old[state]))
					v_new[state] = max(v_list)
				v_old = v_new
				if(delta < 0.2):
					break;

			#TEST:
			# for state, value in v_old.items():
			# 	print(state, value)
			#FIND POLICY //value iteration:
			done = False
			current_state = self.init_state
			while (not done):
			#for i in range(0):
				best_action = None
				max_score = -100
				next_s = None
				score_list = []
				next_state_list = []

				for action, next_state in self.MDP[current_state].items():
					[prob, ns, reward, done] = next_state
					if ns not in v_old.keys():
						continue
					else:
						score = prob * (reward + discount_factor * v_old[ns])
						score_list.append(score)
						next_state_list.append((action, ns, done))
						# print(action, score)
				if len(score_list) !=0:
					for idx, s in enumerate(score_list):
						a, _, _ = next_state_list[idx];
					picked_idx = self.sampleProbs(score_list)
					best_action, next_s, done = next_state_list[picked_idx]
					#print(best_action, next_s, done)
					# print("best_action: ", best_action)

				if best_action is not None:
					policy.append(type(best_action.action).__name__ +": "+ ",".join(best_action.parameters))
					#print(best_action)
				if next_s == None and done !=True:
					done = True
					policy = []
					print("failed to generate a plan. The current plan is as follows: ")
					return("failed to generate a plan")
				current_state = next_s
		except Exception as err:
			print("planning error: ", err);
			return("failed to generate a plan")

		return policy

	def sampleProbs(self, score):

		for idx, s in enumerate(score):
			if s < 0:
				score[idx] = 0;
		#print(score)
		cdf = np.cumsum(np.array(score))
		cdf_norm = cdf/cdf[-1]
		#print(cdf_norm)
		r = random.uniform(0, 1)
		for idx, c in enumerate(cdf_norm):
			if c > r:
				return idx
		return len(score)-1;



	def plan_causal(self, state):
		causal_graph = state.causal_graph.all_graph[0]
		causal_obj = state.causal_graph
		causal_node_dict = state.causal_graph.all_nodes[0]
		root = causal_graph[causal_obj.goal_name]
		action_list = []
		valid_actions = self.domain.getValidActions(state)
		print("valid actions", [v.parameters for v in valid_actions])
		def dfs(root):
			if len(root.children_node) ==0:
				if root.name in state.obj_func:
					return state.obj_func[root.name][0]
			prev_obj = None
			print("HHHHEEELLLLOOOO")
			print(root.children_node)
			for child in root.children_node: #connect subtree children object together
				obj = dfs(causal_node_dict[child])
				if prev_obj:
					action = SpecificAction(self.domain.connect, [prev_obj, obj], state)
					action_list.append(type(action.action).__name__ +": "+ ",".join(action.parameters))
					action.action.doAction(state, action.parameters)
					#print(state)
				prev_obj = obj
			if root.name in state.obj_func: # connect subtree root object with the children (if subtree root is a function node)
				obj = state.obj_func[root.name][0]
				action = SpecificAction(self.domain.connect, [prev_obj, obj], state)
				action_list.append(type(action.action).__name__ +": "+ ",".join(action.parameters))
				action.action.doAction(state, action.parameters)
				#print(state)
				prev_obj = obj
			return prev_obj

		dfs(root)

		print(action_list)
		return action_list

	# def plan_causal_constrained(self, state,i):
	# 	if (not state.causal_graph.all_graph):
	# 		return
	#
	# 	causal_graph = state.causal_graph.all_graph[0]
	# 	causal_obj = state.causal_graph
	# 	print("HIIII",state.obj_func)
	# 	causal_node_dict = state.causal_graph.all_nodes[0]
	# 	testdict = [[a,b.name] for a,b in causal_graph.items()]
	# 	print("causal node dict",causal_node_dict )
	# 	print( "length", len(state.causal_graph.all_graph) )
	# 	root = causal_graph[causal_obj.goal_name]
	# 	action_list = []
	# 	valid_actions = self.domain.getValidActions(state)
	# 	valid_actions_done = []
	# 	print("valid actions", [v.parameters for v in valid_actions])
	# 	def dfs(root):
	# 		if len(root.children_node) ==0:
	# 			if root.name in state.obj_func:
	# 				if (len(state.obj_func[root.name])>i):
	# 					return state.obj_func[root.name][i]
	# 				else:
	# 					return state.obj_func[root.name][0]
	#
	# 		prev_obj = None
	# 		print("HHHHEEELLLLOOOO")
	# 		print(root.children_node, root.name)
	# 		for bottom,top in combinations(root.children_node,2): #connect subtree children object together
	# 			bottom_obj = dfs(causal_node_dict[bottom])
	# 			print("bottom_obj",bottom_obj)
	# 			top_obj= dfs(causal_node_dict[top])
	# 			#if prev_obj:
	# 			action1 = SpecificAction(self.domain.connect, [bottom_obj, top_obj], state)
	# 			action2 = SpecificAction(self.domain.connect, [top_obj, bottom_obj], state)
	# 			print("Action1 ", action1.parameters)
	# 			print("Action2 ", action2.parameters)
	# 			if action1 in valid_actions:
	# 				if action1 not in valid_actions_done:
	# 					print("Action1 ", action1.parameters)
	# 					action_list.append(type(action1.action).__name__ +": "+ ",".join(action1.parameters))
	# 					action1.action.doAction(state, action1.parameters)
	# 					valid_actions_done.append(action1)
	# 			elif action2 in valid_actions:
	# 				if action2 not in valid_actions_done:
	# 					action_list.append(type(action2.action).__name__ + ": " + ",".join(action2.parameters))
	# 					action2.action.doAction(state, action2.parameters)
	# 					valid_actions_done.append(action2)
	# 			else:
	# 				continue
	#
	# 				#print(state)
	# 			#prev_obj = obj
	# 		# if root.name in state.obj_func: # connect subtree root object with the children (if subtree root is a function node)
	# 		# 	obj = state.obj_func[root.name][0]
	# 		# 	action = SpecificAction(self.domain.connect, [prev_obj, obj], state)
	# 		# 	action_list.append(type(action.action).__name__ +": "+ ",".join(action.parameters))
	# 		# 	action.action.doAction(state, action.parameters)
	# 		# 	#print(state)
	# 		# 	prev_obj = obj
	# 		# return prev_obj
	#
	# 	dfs(root)
	#
	# 	print(action_list)
	# 	#print("is goal satisfied?",state.)
	# 	return action_list
	def plan_causal_constrained_no_validactions(self, state, plan_object):
		if (not state.causal_graph.all_graph):
			return
		print("obj dict", state.obj_dict)
		causal_graph = state.causal_graph.all_graph[0]
		causal_obj = state.causal_graph
		print("HIIII",state.obj_func)
		causal_node_dict = state.causal_graph.all_nodes[0]
		testdict = [[a,b.name] for a,b in causal_graph.items()]
		print("causal node dict",causal_node_dict )
		print( "length", len(state.causal_graph.all_graph) )
		root = causal_graph[causal_obj.goal_name]
		action_list = []
		#valid_actions = self.domain.getValidActions(state)
		valid_actions_done = []
		error_code = 0
		print ("goal", self.domain.goal)
		#done = False
		#print("valid actions", [v.parameters for v in valid_actions])
		def dfs(root,planobj):


			#done = False
			#if len(uniquechild.values())==0:
			if len(root.children_node) ==0:
				if root.name in state.obj_func:
					i = self.valobjs(state.obj_func[root.name], planobj)
					if (i!=-1):
						#error_code+=1
						return state.obj_func[root.name][i]
					else:
						return None
					# if (len(state.obj_func[root.name])>0):
					# 	i = self.valobjs(state.obj_func[root.name],planobj)
					# 	return state.obj_func[root.name][i]
					# else:
					# 	return state.obj_func[root.name][0]
			#if len(uniquechild.values()) == 1:
			if len(root.children_node) == 1:
				#if root.name in state.obj_func:
				#i = self.valobjs(state.obj_func[root.name], planobj)
				if (root.name in state.obj_func):
					print("in 1 child")
					i = self.valobjs(state.obj_func[root.name], planobj)
					obj1 =  dfs(causal_node_dict[root.children_node[0]],planobj)
					#lastobj = state.obj_func[root.children_node[0]][i]
					if (i!=-1):
						#error_code += 1
						lastobj = state.obj_func[root.name][i]
					else:
						lastobj = None
					print('lastobj',lastobj)
					print('obj1',obj1)
					newact = SpecificAction(self.domain.connect, [lastobj, obj1], state)
					action_list.append(" " + type(newact.action).__name__ + " " + " with ".join(
						f'"{param}"' for param in newact.parameters))
					# if newact in valid_actions:
					# 	if newact not in valid_actions_done:
					# 		# action_list.append(" "+type(newact.action).__name__ + ": " + ",".join(newact.parameters))
					# 		action_list.append(" " + type(newact.action).__name__ + " " + " with ".join(f'"{param}"' for param in newact.parameters))
					# 		# newact.action.doAction(state, newact.parameters)
					# 		valid_actions_done.append(newact)
					# newact2 = SpecificAction(self.domain.connect, [ obj1,lastobj], state)
					# if newact2 in valid_actions:
					# 	if newact2 not in valid_actions_done:
					# 		# action_list.append(" "+type(newact2.action).__name__ + ": " + ",".join(newact2.parameters))
					# 		action_list.append(" " + type(newact2.action).__name__ + " " + " with ".join(f'"{param}"' for param in newact2.parameters))
					# 		# newact2.action.doAction(state, newact2.parameters)
					# 		valid_actions_done.append(newact2)
					valid_actions_done.append(newact)
					if valid_actions_done:
						return valid_actions_done[-1].parameters[-1]
					else:
						return None
				else:
					#dfs(causal_node_dict[root.children_node[0]], planobj)
					obj1 = dfs(causal_node_dict[root.children_node[0]], planobj)
					if(causal_node_dict[root.children_node[0]].name in state.obj_func):
						i = self.valobjs(state.obj_func[root.children_node[0]], planobj)
						lastobj = state.obj_func[root.children_node[0]][i]
						#lastobj = state.obj_func[root.name][i]
						print('lastobj', lastobj)
						print('obj1', obj1)
						newact = SpecificAction(self.domain.connect, [lastobj, obj1], state)
						action_list.append(" " + type(newact.action).__name__ + " " + " with ".join(
							f'"{param}"' for param in newact.parameters))
						# if newact in valid_actions:
						# 	if newact not in valid_actions_done:
						# 		# action_list.append(" "+type(newact.action).__name__ + ": " + ",".join(newact.parameters))
						# 		action_list.append(" " + type(newact.action).__name__ + " " + " with ".join(f'"{param}"' for param in newact.parameters))
						# 		# newact.action.doAction(state, newact.parameters)
						# 		valid_actions_done.append(newact)
						# newact2 = SpecificAction(self.domain.connect, [obj1, lastobj], state)
						# if newact2 in valid_actions:
						# 	if newact2 not in valid_actions_done:
						# 		# action_list.append(" "+type(newact2.action).__name__ + ": " + ",".join(newact2.parameters))
						# 		action_list.append(" " + type(newact2.action).__name__ + " " + " with ".join(
						# 			f'"{param}"' for param in newact2.parameters))
						# 		# newact2.action.doAction(state, newact2.parameters)
						# 		valid_actions_done.append(newact2)
						valid_actions_done.append(newact)
						if valid_actions_done:
							return valid_actions_done[-1].parameters[-1]
						else:
							return None
					else:
						return None
			prev_obj = None
			print("HHHHEEELLLLOOOO")
			print(root.children_node, root.name)
			uniquechild = {}
			for child in root.children_node:
				if causal_node_dict[child].name in state.obj_func:
					i = self.valobjs(state.obj_func[causal_node_dict[child].name], planobj)
					objpart = state.obj_func[causal_node_dict[child].name][i]
					if objpart in uniquechild:
						continue
					else:
						uniquechild[objpart] = child

			print("unique child ",uniquechild)
			#for bottom, top in combinations(uniquechild.values(), 2):
			for bottom,top in combinations(root.children_node,2): #connect subtree children object together
				bottom_obj = dfs(causal_node_dict[bottom],planobj)
				print("bottom_obj",bottom_obj)
				top_obj= dfs(causal_node_dict[top],planobj)
				print("top_obj", top_obj)
				#if prev_obj:
				if (bottom_obj!=None and top_obj!=None):
					action1 = SpecificAction(self.domain.connect, [bottom_obj, top_obj], state)
					action2 = SpecificAction(self.domain.connect, [top_obj, bottom_obj], state)
					print("Action1 ", action1.parameters)
					print("Action2 ", action2.parameters)
					valid_actions_done.append(action1)
					action_list.append(" " + type(action1.action).__name__ + " " + " with ".join(
					f'"{param}"' for param in action1.parameters))
					# if action1 in valid_actions:
					# 	if action1 not in valid_actions_done:
					# 		print("Action1 ", action1.parameters)
					# 		# action_list.append(" "+type(action1.action).__name__ +": "+ ",".join(action1.parameters))
					# 		action_list.append(" "+type(action1.action).__name__ + " " + " with ".join(f'"{param}"' for param in action1.parameters))
					# 		# action1.action.doAction(state, action1.parameters)
					# 		valid_actions_done.append(action1)
					#
					# 		# if not done:
					# 		# 	if(self.domain.isGoalSatisfied(action1.state)):
					# 		# 		done = True
					#
					# elif action2 in valid_actions:
					# 	if action2 not in valid_actions_done:
					# 		#action_list.append(" "+type(action2.action).__name__ + ": " + ",".join(action2.parameters))
					# 		action_list.append(" "+type(action2.action).__name__ + " " + " with ".join(f'"{param}"' for param in action2.parameters))
					# 		# action2.action.doAction(state, action2.parameters)
					# 		valid_actions_done.append(action2)
					# 		# if not done:
					# 		# 	if(self.domain.isGoalSatisfied(action2.state)):
					# 		# 		done = True
					#
					# else:
					# 	continue
				else:
					print("ONE IS NONE")
					if(bottom_obj==None and top_obj!=None and valid_actions_done ):
						lastobj = valid_actions_done[-1].parameters[-1]
						newact = SpecificAction(self.domain.connect, [lastobj, top_obj], state)
						valid_actions_done.append(newact)
						action_list.append(" " + type(newact.action).__name__ + " " + " with ".join(
						f'"{param}"' for param in newact.parameters))
						# if newact in valid_actions:
						# 	if newact not in valid_actions_done:
						# 		# action_list.append(" "+type(newact.action).__name__ + ": " + ",".join(newact.parameters))
						# 		action_list.append(" " + type(newact.action).__name__ + " " + " with ".join(f'"{param}"' for param in newact.parameters))
						# 		# newact.action.doAction(state, newact.parameters)
						# 		valid_actions_done.append(newact)
					if (bottom_obj != None and top_obj == None and valid_actions_done):
						lastobj = valid_actions_done[-1].parameters[-1]
						newact = SpecificAction(self.domain.connect, [lastobj, bottom_obj], state)
						action_list.append(" " + type(newact.action).__name__ + " " + " with ".join(
							f'"{param}"' for param in newact.parameters))
						# if newact in valid_actions:
						# 	if newact not in valid_actions_done:
						# 		# action_list.append(" "+type(newact.action).__name__ + ": " + ",".join(newact.parameters))
						# 		action_list.append(" " + type(newact.action).__name__ + " " + " with ".join(f'"{param}"' for param in newact.parameters))
						# 		# newact.action.doAction(state, newact.parameters)
						# 		valid_actions_done.append(newact)
						valid_actions_done.append(newact)

			#connecting to parent

			if (root.name in state.obj_func):
				print("in 1 child")
				i = self.valobjs(state.obj_func[root.name], planobj)
				if len(uniquechild)==1:
					obj1 = list(uniquechild.keys())[0]
				elif valid_actions_done:
					obj1 = valid_actions_done[-1].parameters[-1]
				else:
					obj1 = None

				#obj1 = valid_actions_done[-1].parameters[-1] if valid_actions_done else None
				# lastobj = state.obj_func[root.children_node[0]][i]
				if (i != -1):
					# error_code += 1
					lastobj = state.obj_func[root.name][i]
				else:
					lastobj = None
				print('lastobj', lastobj)
				print('obj1', obj1)
				newact = SpecificAction(self.domain.connect, [lastobj, obj1], state)
				valid_actions_done.append(newact)
				action_list.append(
				" " + type(newact.action).__name__ + " " + " with ".join(f'"{param}"' for param in newact.parameters))
				# if newact in valid_actions:
				# 	if newact not in valid_actions_done:
				# 		# action_list.append(" "+type(newact.action).__name__ + ": " + ",".join(newact.parameters))
				# 		action_list.append(" " + type(newact.action).__name__ + " " + " with ".join(f'"{param}"' for param in newact.parameters))
				# 		# newact.action.doAction(state, newact.parameters)
				# 		valid_actions_done.append(newact)
				# newact2 = SpecificAction(self.domain.connect, [obj1, lastobj], state)
				# if newact2 in valid_actions:
				# 	if newact2 not in valid_actions_done:
				# 		# action_list.append(" "+type(newact2.action).__name__ + ": " + ",".join(newact2.parameters))
				# 		action_list.append(" " + type(newact2.action).__name__ + " " + " with ".join(f'"{param}"' for param in newact2.parameters))
				# 		# newact2.action.doAction(state, newact2.parameters)
				# 		valid_actions_done.append(newact2)
				# if valid_actions_done:
				# 	return valid_actions_done[-1].parameters[-1]
				# else:
				# 	return None
			if valid_actions_done:
				return  valid_actions_done[-1].parameters[-1]
			else:
				return None

			#done = self.domain.isGoalSatisfied(state)
			# done = len(action_list)>0
			action_list.append("done?: "+str(True))
					#print(state)
				#prev_obj = obj
			# if root.name in state.obj_func: # connect subtree root object with the children (if subtree root is a function node)
			# 	obj = state.obj_func[root.name][0]
			# 	action = SpecificAction(self.domain.connect, [prev_obj, obj], state)
			# 	action_list.append(type(action.action).__name__ +": "+ ",".join(action.parameters))
			# 	action.action.doAction(state, action.parameters)
			# 	#print(state)
			# 	prev_obj = obj
			# return prev_obj

		i = 0
		#self.domain.isGoalSatisfied(state)
		if isinstance(plan_object,list):
			i=0
			new_action_list = []
			for obj in plan_object:
				#action_list = ["Assembly plan for " + str(obj) + " : "]
				action_list=[]
				valid_actions_done=[]
				error_code = 0
				dfs(root,obj)
				visited=set()
				ct=[]
				ctn = self.ctnodes(state,root,obj,visited,ct,causal_node_dict)
				if (len(action_list) < 1 and ctn == 0):
					action_list.append("None. Feedback: No parts for this object found. Please update causal model.")

				if (len(action_list) < 1 and ctn == 1):
					action_list.append(	"None. Feedback: Only 1 part found. Atleast 2 parts needed for assembly. Please update causal model.")
				elif (len(action_list) < 1 and ctn != 0):
					action_list.append("None. Feedback: The parts cannot be connected together. Please update causal model.")
				print("NUMBER OF NODES  ",ctn)
				# action_list[0] = "Assembly plan for " + str(obj) + " - " + action_list[0]
				action_list = ["Assembly plan for " + str(obj) + " : "] + action_list
				new_action_list.append(action_list)
				i=i+1


			print(new_action_list)
			#print("is goal satisfied?",state.)
			return new_action_list

		else:
			#action_list = ["Assembly plan for " + str(plan_object) +" : "]
			action_list = []
			dfs(root,plan_object)
			visited = set()
			ct = []
			ctn = self.ctnodes(state, root, plan_object, visited, ct,causal_node_dict)
			if (len(action_list)<1 and ctn==0):
				action_list.append("None. Feedback: No parts for this object found. Please update causal model.")

			if (len(action_list) < 1 and ctn == 1):
				action_list.append("None. Feedback: Only 1 part found. Atleast 2 parts needed for assembly. Please update causal model or function associations")
			elif (len(action_list) < 1 and ctn != 0):
				action_list.append("None. Feedback: The parts cannot be connected together. Please update causal model or function associations")
			#action_list[0]="Assembly plan for " + str(plan_object) +" - " + action_list[0]
			action_list = ["Assembly plan for " + str(plan_object) + " : "] + action_list
			print("NUMBER OF NODES  ", ctn)
			print(action_list)
			return [action_list]


	def plan_causal_constrained(self, state, plan_object):
		if (not state.causal_graph.all_graph):
			return
		print("obj dict", state.obj_dict)
		causal_graph = state.causal_graph.all_graph[0]
		causal_obj = state.causal_graph
		print("HIIII",state.obj_func)
		causal_node_dict = state.causal_graph.all_nodes[0]
		testdict = [[a,b.name] for a,b in causal_graph.items()]
		print("causal node dict",causal_node_dict )
		print( "length", len(state.causal_graph.all_graph) )
		root = causal_graph[causal_obj.goal_name]
		action_list = []
		valid_actions = self.domain.getValidActions(state)
		valid_actions_done = []
		error_code = 0
		print ("goal", self.domain.goal)
		#done = False
		print("valid actions", [v.parameters for v in valid_actions])
		def dfs(root,planobj):


			#done = False
			#if len(uniquechild.values())==0:
			if len(root.children_node) ==0:
				if root.name in state.obj_func:
					i = self.valobjs(state.obj_func[root.name], planobj)
					if (i!=-1):
						#error_code+=1
						return state.obj_func[root.name][i]
					else:
						return None
					# if (len(state.obj_func[root.name])>0):
					# 	i = self.valobjs(state.obj_func[root.name],planobj)
					# 	return state.obj_func[root.name][i]
					# else:
					# 	return state.obj_func[root.name][0]
			#if len(uniquechild.values()) == 1:
			if len(root.children_node) == 1:
				#if root.name in state.obj_func:
				#i = self.valobjs(state.obj_func[root.name], planobj)
				if (root.name in state.obj_func):
					print("in 1 child")
					i = self.valobjs(state.obj_func[root.name], planobj)
					obj1 =  dfs(causal_node_dict[root.children_node[0]],planobj)
					#lastobj = state.obj_func[root.children_node[0]][i]
					if (i!=-1):
						#error_code += 1
						lastobj = state.obj_func[root.name][i]
					else:
						lastobj = None
					print('lastobj',lastobj)
					print('obj1',obj1)
					newact = SpecificAction(self.domain.connect, [lastobj, obj1], state)
					if newact in valid_actions:
						if newact not in valid_actions_done:
							# action_list.append(" "+type(newact.action).__name__ + ": " + ",".join(newact.parameters))
							action_list.append(" " + type(newact.action).__name__ + " " + " with ".join(f'"{param}"' for param in newact.parameters))
							# newact.action.doAction(state, newact.parameters)
							valid_actions_done.append(newact)
					newact2 = SpecificAction(self.domain.connect, [ obj1,lastobj], state)
					if newact2 in valid_actions:
						if newact2 not in valid_actions_done:
							# action_list.append(" "+type(newact2.action).__name__ + ": " + ",".join(newact2.parameters))
							action_list.append(" " + type(newact2.action).__name__ + " " + " with ".join(f'"{param}"' for param in newact2.parameters))
							# newact2.action.doAction(state, newact2.parameters)
							valid_actions_done.append(newact2)
					if valid_actions_done:
						return valid_actions_done[-1].parameters[-1]
					else:
						return None
				else:
					#dfs(causal_node_dict[root.children_node[0]], planobj)
					obj1 = dfs(causal_node_dict[root.children_node[0]], planobj)
					if(causal_node_dict[root.children_node[0]].name in state.obj_func):
						i = self.valobjs(state.obj_func[root.children_node[0]], planobj)
						lastobj = state.obj_func[root.children_node[0]][i]
						#lastobj = state.obj_func[root.name][i]
						print('lastobj', lastobj)
						print('obj1', obj1)
						newact = SpecificAction(self.domain.connect, [lastobj, obj1], state)
						if newact in valid_actions:
							if newact not in valid_actions_done:
								# action_list.append(" "+type(newact.action).__name__ + ": " + ",".join(newact.parameters))
								action_list.append(" " + type(newact.action).__name__ + " " + " with ".join(f'"{param}"' for param in newact.parameters))
								# newact.action.doAction(state, newact.parameters)
								valid_actions_done.append(newact)
						newact2 = SpecificAction(self.domain.connect, [obj1, lastobj], state)
						if newact2 in valid_actions:
							if newact2 not in valid_actions_done:
								# action_list.append(" "+type(newact2.action).__name__ + ": " + ",".join(newact2.parameters))
								action_list.append(" " + type(newact2.action).__name__ + " " + " with ".join(
									f'"{param}"' for param in newact2.parameters))
								# newact2.action.doAction(state, newact2.parameters)
								valid_actions_done.append(newact2)
						if valid_actions_done:
							return valid_actions_done[-1].parameters[-1]
						else:
							return None
					else:
						return None
			prev_obj = None
			print("HHHHEEELLLLOOOO")
			print(root.children_node, root.name)
			uniquechild = {}
			for child in root.children_node:
				if causal_node_dict[child].name in state.obj_func:
					i = self.valobjs(state.obj_func[causal_node_dict[child].name], planobj)
					objpart = state.obj_func[causal_node_dict[child].name][i]
					if objpart in uniquechild:
						continue
					else:
						uniquechild[objpart] = child

			print("unique child ",uniquechild)
			#for bottom, top in combinations(uniquechild.values(), 2):
			for bottom,top in combinations(root.children_node,2): #connect subtree children object together
				bottom_obj = dfs(causal_node_dict[bottom],planobj)
				print("bottom_obj",bottom_obj)
				top_obj= dfs(causal_node_dict[top],planobj)
				print("top_obj", top_obj)
				#if prev_obj:
				if (bottom_obj!=None and top_obj!=None):
					action1 = SpecificAction(self.domain.connect, [bottom_obj, top_obj], state)
					action2 = SpecificAction(self.domain.connect, [top_obj, bottom_obj], state)
					print("Action1 ", action1.parameters)
					print("Action2 ", action2.parameters)
					if action1 in valid_actions:
						if action1 not in valid_actions_done:
							print("Action1 ", action1.parameters)
							# action_list.append(" "+type(action1.action).__name__ +": "+ ",".join(action1.parameters))
							action_list.append(" "+type(action1.action).__name__ + " " + " with ".join(f'"{param}"' for param in action1.parameters))
							# action1.action.doAction(state, action1.parameters)
							valid_actions_done.append(action1)

							# if not done:
							# 	if(self.domain.isGoalSatisfied(action1.state)):
							# 		done = True

					elif action2 in valid_actions:
						if action2 not in valid_actions_done:
							#action_list.append(" "+type(action2.action).__name__ + ": " + ",".join(action2.parameters))
							action_list.append(" "+type(action2.action).__name__ + " " + " with ".join(f'"{param}"' for param in action2.parameters))
							# action2.action.doAction(state, action2.parameters)
							valid_actions_done.append(action2)
							# if not done:
							# 	if(self.domain.isGoalSatisfied(action2.state)):
							# 		done = True

					else:
						continue
				else:
					print("ONE IS NONE")
					if(bottom_obj==None and top_obj!=None and valid_actions_done ):
						lastobj = valid_actions_done[-1].parameters[-1]
						newact = SpecificAction(self.domain.connect, [lastobj, top_obj], state)
						if newact in valid_actions:
							if newact not in valid_actions_done:
								# action_list.append(" "+type(newact.action).__name__ + ": " + ",".join(newact.parameters))
								action_list.append(" " + type(newact.action).__name__ + " " + " with ".join(f'"{param}"' for param in newact.parameters))
								# newact.action.doAction(state, newact.parameters)
								valid_actions_done.append(newact)
					if (bottom_obj != None and top_obj == None and valid_actions_done):
						lastobj = valid_actions_done[-1].parameters[-1]
						newact = SpecificAction(self.domain.connect, [lastobj, bottom_obj], state)
						if newact in valid_actions:
							if newact not in valid_actions_done:
								# action_list.append(" "+type(newact.action).__name__ + ": " + ",".join(newact.parameters))
								action_list.append(" " + type(newact.action).__name__ + " " + " with ".join(f'"{param}"' for param in newact.parameters))
								# newact.action.doAction(state, newact.parameters)
								valid_actions_done.append(newact)

			#connecting to parent

			if (root.name in state.obj_func):
				print("in 1 child")
				i = self.valobjs(state.obj_func[root.name], planobj)
				if len(uniquechild)==1:
					obj1 = list(uniquechild.keys())[0]
				elif valid_actions_done:
					obj1 = valid_actions_done[-1].parameters[-1]
				else:
					obj1 = None

				#obj1 = valid_actions_done[-1].parameters[-1] if valid_actions_done else None
				# lastobj = state.obj_func[root.children_node[0]][i]
				if (i != -1):
					# error_code += 1
					lastobj = state.obj_func[root.name][i]
				else:
					lastobj = None
				print('lastobj', lastobj)
				print('obj1', obj1)
				newact = SpecificAction(self.domain.connect, [lastobj, obj1], state)
				if newact in valid_actions:
					if newact not in valid_actions_done:
						# action_list.append(" "+type(newact.action).__name__ + ": " + ",".join(newact.parameters))
						action_list.append(" " + type(newact.action).__name__ + " " + " with ".join(f'"{param}"' for param in newact.parameters))
						# newact.action.doAction(state, newact.parameters)
						valid_actions_done.append(newact)
				newact2 = SpecificAction(self.domain.connect, [obj1, lastobj], state)
				if newact2 in valid_actions:
					if newact2 not in valid_actions_done:
						# action_list.append(" "+type(newact2.action).__name__ + ": " + ",".join(newact2.parameters))
						action_list.append(" " + type(newact2.action).__name__ + " " + " with ".join(f'"{param}"' for param in newact2.parameters))
						# newact2.action.doAction(state, newact2.parameters)
						valid_actions_done.append(newact2)
				# if valid_actions_done:
				# 	return valid_actions_done[-1].parameters[-1]
				# else:
				# 	return None
			if valid_actions_done:
				return  valid_actions_done[-1].parameters[-1]
			else:
				return None

			#done = self.domain.isGoalSatisfied(state)
			# done = len(action_list)>0
			action_list.append("done?: "+str(True))
					#print(state)
				#prev_obj = obj
			# if root.name in state.obj_func: # connect subtree root object with the children (if subtree root is a function node)
			# 	obj = state.obj_func[root.name][0]
			# 	action = SpecificAction(self.domain.connect, [prev_obj, obj], state)
			# 	action_list.append(type(action.action).__name__ +": "+ ",".join(action.parameters))
			# 	action.action.doAction(state, action.parameters)
			# 	#print(state)
			# 	prev_obj = obj
			# return prev_obj

		i = 0
		#self.domain.isGoalSatisfied(state)
		if isinstance(plan_object,list):
			i=0
			new_action_list = []
			for obj in plan_object:
				#action_list = ["Assembly plan for " + str(obj) + " : "]
				action_list=[]
				valid_actions_done=[]
				error_code = 0
				dfs(root,obj)
				visited=set()
				ct=[]
				ctn = self.ctnodes(state,root,obj,visited,ct,causal_node_dict)
				if (len(action_list) < 1 and ctn == 0):
					action_list.append("None. Feedback: No parts for this object found. Please update causal model.")

				if (len(action_list) < 1 and ctn == 1):
					action_list.append(	"None. Feedback: Only 1 part found. Atleast 2 parts needed for assembly. Please update causal model.")
				elif (len(action_list) < 1 and ctn != 0):
					action_list.append("None. Feedback: The parts cannot be connected together. Please update causal model.")
				print("NUMBER OF NODES  ",ctn)
				# action_list[0] = "Assembly plan for " + str(obj) + " - " + action_list[0]
				action_list = ["Assembly plan for " + str(obj) + " : "] + action_list
				new_action_list.append(action_list)
				i=i+1


			print(new_action_list)
			#print("is goal satisfied?",state.)
			return new_action_list

		else:
			#action_list = ["Assembly plan for " + str(plan_object) +" : "]
			action_list = []
			dfs(root,plan_object)
			visited = set()
			ct = []
			ctn = self.ctnodes(state, root, plan_object, visited, ct,causal_node_dict)
			if (len(action_list)<1 and ctn==0):
				action_list.append("None. Feedback: No parts for this object found. Please update causal model.")

			if (len(action_list) < 1 and ctn == 1):
				action_list.append("None. Feedback: Only 1 part found. Atleast 2 parts needed for assembly. Please update causal model or function associations")
			elif (len(action_list) < 1 and ctn != 0):
				action_list.append("None. Feedback: The parts cannot be connected together. Please update causal model or function associations")
			#action_list[0]="Assembly plan for " + str(plan_object) +" - " + action_list[0]
			action_list = ["Assembly plan for " + str(plan_object) + " : "] + action_list
			print("NUMBER OF NODES  ", ctn)
			print(action_list)
			return [action_list]

	def ctnodes(self,state, root, obj,visited,ct,causal_node_dict):
		visited.add(root)
		i = self.valobjs(state.obj_func[root.name], obj)
		if (i!=-1):
			ct.append(1)
		for child in root.children_node:
			if child not in visited:
				self.ctnodes(state,causal_node_dict[child],obj,visited,ct,causal_node_dict)
		return len(ct)

	def valobjs(self,listofparts,planObj):
		validparts=[]
		if planObj == "kerosene_lamp":
			validparts.append("fuel tank with kerosene")
			validparts.append("burner")
			validparts.append("chimney");
		elif planObj == "flashlight":
			validparts.append("head");
			validparts.append("batteries");
			validparts.append("case");
		elif planObj == "candle":
			validparts.append("wax");
			validparts.append("wick");
		elif planObj == "lamp":
			validparts.append("base with cables");
			validparts.append("light bulb");
			validparts.append("shade");
		elif planObj == "wall_lamp":
			validparts.append("backplate");
			validparts.append("lamp body");
			validparts.append("light bulb");
		elif planObj == "oil_lamp":
			validparts.append("container with oil");
			validparts.append("wick")
		elif planObj == "recorder":
			validparts.append("mouth piece");
			validparts.append("body")
		objneeded = list(set(validparts).intersection(set(listofparts)))
		#print("obj needed",objneeded)
		if (objneeded==[]):
			return -1
		else:
			return listofparts.index(objneeded[0])



	@staticmethod
	def Causal(self, pickBestAction, repick=None):
		debug = True


		#Initialization
		nodes_touched = 0
		backtracks = 0
		start_time = time.time()

		#Get valid actions copies from a domain so don't need to worry about mutation
		valid_actions = self.domain.getValidActions(self.domain.state)

				#Sanity check
		if len(valid_actions) == 0:
			print("ERROR: No possible actions from initial state!")
			exit(0)

		curr_action = SpecificAction(None, None, deepcopy(self.domain.state))
		# print("In planner")
		# print(self.domain.state)

		#Deep copy because if backtrack to initial state, don't want to manipulate states
		#This special first action holds the first initial state before no action has been done
		#This is why its action type is none
		#Effectively each state stored w an action in the history is the state after an action has been applied
		first_specified_action = deepcopy(curr_action)
		first_specified_action.action = None

		#Place into node
		curr_node = self.Node(curr_action, [first_specified_action])

		#While the current state is not the goal state
		done=False
		while not(self.domain.isGoalSatisfied(curr_node.specifiedaction.state)):


			next_actions = self.domain.getValidActions(curr_node.specifiedaction.state)
			#implement look-ahead step where the next action will result in a dead-end state

			print("current state", curr_node.specifiedaction.state)
			print("current causal", curr_node.specifiedaction.state.causal_graph)

			#We are at a "dead end" state
			if len(next_actions) == 0:
				if debug:
					print("Stuck... backtracking")
				backtracks += 1
				#Want to revert state to a previous state, and try and
				#find some new actions
				curr_node.specifiedaction.state = deepcopy(curr_node.history[-2].state)
				curr_node.specifiedaction.action = deepcopy(curr_node.history[-2].action)
				# print("unsuccess attemp")
				# self.printHistory(curr_node.history)
				curr_node.history.pop()
				#Restart and try and get new actions from beginning
				continue

			curr_node.specifiedaction, all_probs = pickBestAction(next_actions)
			if debug:
				print("picked action: ", type(curr_node.specifiedaction.action).__name__,  curr_node.specifiedaction.parameters)
				print("show current available action prob")
				for i in range(len(next_actions)):
					print("potential action", type(next_actions[i].action).__name__,  next_actions[i].parameters, all_probs[i])

			action = curr_node.specifiedaction

			#Perform the perviously defined action
			nodes_touched += 1

			action.action.doAction(action.state, action.parameters)
			curr_node.specifiedaction.state.causal_graph.runModel(curr_node.specifiedaction.state, action)
			print(curr_node.specifiedaction.state.causal_graph)
			#add one look-ahead step, not needed for this appplication yet:

			potential_next_actions = self.domain.getValidActions(action.state)
			while((len(potential_next_actions) ==0 and not self.domain.isGoalSatisfied(action.state))):
				#curr_node.specifiedaction.state = deepcopy(curr_node.history[-1].state)
				#curr_node.specifiedaction.action = deepcopy(curr_node.history[-1].action)
				repick_indx = next_actions.index(curr_node.specifiedaction)
				next_actions.remove(curr_node.specifiedaction)

				if len(next_actions) == 0:
					done = True
					print("Failed generating a plan")
					break
				curr_node.specifiedaction =  repick(picked_idx=repick_indx)
				print("look ahead found dead-end, repick action...", type(curr_node.specifiedaction.action).__name__,  curr_node.specifiedaction.parameters)

				action = curr_node.specifiedaction
				action.action.doAction(action.state, action.parameters)

				potential_next_actions = self.domain.getValidActions(action.state)


			if done:
				break

			if debug:
				# print("-> Performed action: " + str(type(action.action).__name__) + " " + str(action.parameters))
				# print("New state: ")
				# print(action.state)
				pass

			#Record the action and resultant state in the history
			curr_node.history.append(deepcopy(action))

		time_taken = (time.time() - start_time)

		if debug:
			# print("Nodes touched: " + str(nodes_touched))
			# print("Backtracks taken: " + str(backtracks))
			# print("--- Causal Planner took %s seconds ---" % time_taken)
			pass
		return [tuple(curr_node.history), nodes_touched, backtracks, time_taken]
