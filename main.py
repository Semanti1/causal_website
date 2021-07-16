import sys
import os
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

def website_plan( furniture_path, causal_path, encoding, plan_object):
	causal_path = os.path.join(causal_path, "causal_"+encoding+".json")
	if plan_object == None:
		prop_path = os.path.join(furniture_path, "object_property_"+encoding+".json")
	else:
		prop_path = os.path.join(furniture_path, "object_property_" + plan_object + "_" + encoding+".json")
	domain = Furniture(causal_path, prop_path, plan_object)
	myPlan = Planner(domain)
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
	myPlan.MDP_Init()
	start_time = time.time()
	all_plan = {}
	for i in range(20):
		plan = myPlan.policy_iteration()
		if str(plan) not in all_plan:
			all_plan[str(plan)] = True

	duration = time.time() - start_time
	print("MDP plan time: ", duration)
	plan_str = []
	for plan, _ in all_plan.items():
		plan_str.append(str(plan))
	return plan_str

	# for i in range(20):
	# 	print(myPlan.policy_iteration())
	# return myPlan.policy_iteration()
	# return None

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
	furniture_path = "./causal_models/new_7_15/"
	encoding = "ea5709909ea33f286f4df2c1b1a5d4e50d8a76d2e9214c76c264e64b2f23d25e"
	str = website_plan(furniture_path, furniture_path, encoding, None)
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