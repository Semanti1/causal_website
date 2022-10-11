import sys
import os
import os.path
from os import path
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)
print(sys.path)

#from blockworld import BlockTower
from furniture import Furniture
from planner import Planner
from mcts_planner import MonteCarloSearch
import functools
#import causalmodel
from visualmodel import FurnitureVisualModel
#from blockworld import Goal, BlockTowerState
#from riverworld import RiverWorld
from furniture import Goal, FurnitureState
from heuristicgenerator import HeuristicGenerator
from furniture_heuristic import FurnitureHeuristicGenerator
#from visualizer import runSim
#from furniture_visualizer import runSim
from customerrors import SimulationOver
from abstracttypes import SpecificAction
import os
import time

# from pypddlparser.pddlparser import PDDLParser
# from pypddlparser import main
# import pypddl_parser.pypddl_parser.pddlparser
# import pypddl_parser.pypddl_parser.main

def runSimulation(myplanner):
	# temp_state = BlockTowerState()
	# temp_state.get("a").on = "b"
	# temp_state.get("b").on = "d"
	# temp_state.get("d").on = "c"
	# temp_state.total_weight = 2



	res = myplanner.plan()
	Planner.printHistory(res)
	try:
		# myplanner.domain.state = temp_state
		runSim(res, myplanner)
	except SimulationOver as e:
		print(type(e.message))
		if e.message == None:
			print("Sucess! Goal acheived")
		else:
			domain.state = e.message
			runSimulation(myplanner)

def website_plan( furniture_path, causal_path, encoding, plan_object,num=0, gen=""):
	if ("specific" in gen):
		causal_path = os.path.join(causal_path, "causal_" + gen + "_" +plan_object + "_"+str(num)+"_"+ encoding + ".json")
		prop_path = os.path.join(furniture_path, "object_property_" + gen + "_" +plan_object + "_"+encoding + ".json")

	else:
		causal_path = os.path.join(causal_path, "causal_" + gen + "_" +str(num)+"_"+ encoding+".json")
		prop_path = os.path.join(furniture_path, "object_property_" + gen + "_" + encoding+".json")


	print("plan object", plan_object)
	print("causal path", causal_path,  path.exists(causal_path))
	# print(causal_path, prop_path)
	# domain = Furniture(causal_path, prop_path, plan_object)
	# myPlan = Planner(domain)
	# print("here")

	if (not path.exists(causal_path)):
		return ["Feedback: Please submit causal model and try again."]

	# heur = FurnitureHeuristicGenerator(domain)
	# myPlan.setAlgo(functools.partial(myPlan.Causal, self=myPlan, pickBestAction=heur.chooseNextAction, repick=heur.repickNextAction))
	# res= myPlan.plan()
	# str = Planner.HistoryString(res)
	# return str;


	# MCTreePlan = MonteCarloSearch(domain)
	# start_time = time.time()
	# plan = MCTreePlan.run_tree(domain.state)
	# duration = time.time() - start_time
	# print("mcts one plan time", duration)


	'''myPlan.MDP_Init()
	start_time = time.time()
	all_plan = {}
	for i in range(20):
		plan = myPlan.policy_iteration()
		if str(plan) not in all_plan and len(plan) > 0:
			all_plan[str(plan)] = True

	duration = time.time() - start_time
	print("MDP plan time: ", duration)
	plan_str = []
	for plan, _ in all_plan.items():
		plan_str.append(str(plan))

	return plan_str'''
	if isinstance(plan_object,list):
		a=[]
		i=0
		# for obj in plan_object:
		# 	print(obj)
		# 	domain = Furniture(causal_path, prop_path, obj)
		# 	myPlan = Planner(domain)
		# 	a.append(myPlan.plan_causal_constrained(domain.state,i))
		# 	i=i+1
		# 	print("goal satisfied?? ",domain.isGoalSatisfied(domain.state))
		domain = Furniture(causal_path, prop_path, plan_object)
		myPlan = Planner(domain)
		a = myPlan.plan_causal_constrained(domain.state, plan_object)
		#return myPlan.plan_causal_constrained(domain.state)
		return a
	else:
		domain = Furniture(causal_path, prop_path, plan_object)
		myPlan = Planner(domain)
		res = myPlan.plan_causal_constrained(domain.state,plan_object)
		print("goal satisfied?? ", domain.isGoalSatisfied(domain.state))
		return res
		#return myPlan.plan_causal_constrained(domain.state,0)

if __name__ == "__main__":
	'''
	domain = BlockTower()
	myPlan = Planner(domain)
	causalmodel.generateCausalModels("./pypddl_parser/pypddl_parser/pddl/example_causal_model.pddl", domain)
	# print(cm[0].runModel(SpecificAction(domain.stack, ["a", "b"], domain.state)))


	heur = HeuristicGenerator(domain)
	myPlan.setAlgo(functools.partial(myPlan.Causal, self=myPlan, pickBestAction=heur.chooseNextAction))
	runSimulation(myPlan)

	print(domain.causal_models)
	'''
	# domain = Furniture()
	# myPlan = Planner(domain)
	# #
	# #
	# #
	# heur = FurnitureHeuristicGenerator(domain)
	# # myPlan.MDP_Init()
	# # myPlan.policy_iteration()
	# # #myPlan.setAlgo(functools.partial(myPlan.BFS, self=myPlan))
	# myPlan.setAlgo(functools.partial(myPlan.Causal, self=myPlan, pickBestAction=heur.chooseNextAction, repick=heur.repickNextAction))
	# res=myPlan.plan()
	# Planner.printHistory(res)
	furniture_path = "../static/causal_graph"
	encoding = "b13fe0f24c7f7d05e3cd41c4cfbd6a5fb99487b3632f5df72129ed07f5cafea7"
	str = website_plan(furniture_path, furniture_path, encoding, ["wall_lamp","flashlight"], "near")
	print(str)
	# runSimulation(myPlan)

	'''
	Add causal models to a domain
	For each action search through the causal models to find one who matches in name
	If no matches, raise error
	Or could do model completeness checking earlier
	'''


	# print(cm.getPredicates(SpecificAction(domain.stack, ["a", "b"], domain.state)))

	'''
	# #------Block Domain----------
	domain = BlockTower()
	myPlan = Planner(domain)


	#Uncomment to run BFS
	# viz = BlockVisualModel(domain)
	# myPlan.setAlgo(functools.partial(myPlan.BFS, self=myPlan))

	# #Uncomment to run naive Causal model w no visual model
	# viz = BlockVisualModel(domain)
	# myPlan.setAlgo(functools.partial(myPlan.Causal, self=myPlan, pickBestAction=CausalModel.chooseNextAction))

	# #Uncomment to run Causal model with visual model
	# viz = BlockVisualModel(domain)
	# viz_func = functools.partial(CausalModel.chooseNextActionVisual, viz=viz, domain=domain, debug=False)
	# myPlan.setAlgo(functools.partial(myPlan.Causal, self=myPlan, pickBestAction=viz_func))

	# Planner.printHistory(myPlan.plan())
	# # myPlan.collectStats(1000)
	# print()
	# print(viz.flatness_vals)

	#------------------Entirelly new domain----------
	viz = BlockVisualModel(domain)
	causal = CausalModel(viz)
	heur = HeuristicGenerator(causal)
	myPlan.setAlgo(functools.partial(myPlan.Causal, self=myPlan, pickBestAction=heur.chooseNextAction))
	runSimulation(myPlan)



	# print(domain.state)
	# myPlan.collectStats(1000)
	# res = myPlan.plan()
	# Planner.printHistory(res)
	# simret = runSim(res, myPlan)
	# if simret != None:
	# 	domain.state = copy.deepcopy(simret)




	#--------------River Domain----------------------
	# domain = RiverWorld()
	# planner = Planner(domain, None)
	# planner.setAlgo(functools.partial(planner.BFS, self=planner))
	# Planner.printHistory(planner.plan())
	# domain.cross.doAction(domain.state, ["Boat"])
	# domain.state.get("Boat").inside = "wolf"
	# domain.cross.doAction(domain.state, ["Boat"])
	# print(domain.state)
	'''
