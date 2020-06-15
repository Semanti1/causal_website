import customerrors as err
from planner import *
from abstracttypes import Action, Domain, State
from causalmodel import CausalModel

def getType(obj):
		return type(obj).__name__

def checkType(obj, expected):
	objType = getType(obj)
	if objType != expected:
		raise err.WrongInputType(objType, expected)

def checkPredicateTrue(lambd, obj):
	if not(lambd(obj)):
		raise err.PredicateFailed()

class stack(Action):
	def __init__(self, state, name = "stack"):
		super().__init__(state, name)

	def checkTypes(self, state, b1_name: str, b2_name: str):
		b1 = state.get(b1_name)
		b2 = state.get(b2_name)

		checkType(b1, "Block")
		checkType(b2, "Block")

	def checkPredicates(self, state, b1_name: str, b2_name: str):
		b1 = state.get(b1_name)
		b2 = state.get(b2_name)

		#Predicates, maybe should move them
		stacked = (lambda x: x.stacked)
		notstacked = (lambda x: not(x.stacked))
		top = (lambda x: x.top)
		stackable = (lambda x: x.stackable)

		checkPredicateTrue(stackable, b1)
		checkPredicateTrue(top, b1)
		checkPredicateTrue(stacked, b1)
		checkPredicateTrue(notstacked, b2)

	def doAction(self, state, b1_name: str, b2_name: str):
		self.checkPredicates(state, b1_name, b2_name)

		b1 = state.get(b1_name)
		b2 = state.get(b2_name)

		b1.top = False
		b2.top = True
		b2.stacked = True
		state.total_weight += b2.weight

class unstack(Action):
	def __init__(self, domain, name = "unstack"):
		super().__init__(domain, name)

	def checkTypes(self, state, b1_name: str, b2_name: str):
		b1 = state.get(b1_name)
		b2 = state.get(b2_name)

		checkType(b1, "Block")
		checkType(b2, "Block")

	def checkPredicates(self, state, b1_name: str, b2_name: str):
		b1 = state.get(b1_name)
		b2 = state.get(b2_name)

		stacked = (lambda x: x.stacked)
		top = (lambda x: x.top)

		checkPredicateTrue(stacked, b1)
		checkPredicateTrue(stacked, b2)
		checkPredicateTrue(top, b2)

	def doAction(self, state, b1_name: str, b2_name: str):
		self.checkPredicates(state, b1_name, b2_name)

		b1 = state.get(b1_name)
		b2 = state.get(b2_name)

		b2.stacked = False
		b2.top = False
		b1.top = True
		state.total_weight -= b2.weight


class BlockTowerState(State):
	def __init__(self):
		super().__init__()
		self.addObject(Block("a", False, 1))
		self.addObject(Block("b", True, 1))
		self.addObject(Block("c", True, 3))
		self.addObject(Block("floor", True, 0, True, True))
		self.total_weight = 0

	def __eq__(self, other):
		for objname in self.objname:
			if self.get(objname) == other.get(objname):
				pass
			else:
				return False

		return self.total_weight == other.total_weight


	def __str__(self):
		ret = "Weight: " + str(self.total_weight) + "\n"
		
		for x in self.objects:
			ret += str(x)
		return ret

	def isGoalSatisfied(self):
		return self.total_weight >= 4


class BlockTower(Domain):
	def __init__(self):
		super().__init__(BlockTowerState())
		self.stack = stack(self)
		self.unstack = unstack(self)

class Block():
	def __init__(self, name, stackable, weight, stacked = False, top = False):
		self.name = name
		self.stacked = stacked
		self.top = top
		self.stackable = stackable
		self.weight = weight

	def __str__(self):
		return "(" + self.name + ") " + "Stacked: " + str(self.stacked) + " Top: " + str(self.top) + " Stackable: " + str(self.stackable) + " Weight: " + str(self.weight) + "\n"

	def __eq__(self, other):
		return ((((self.stacked == other.stacked) 
		and self.top == other.top)
		and self.stackable == other.stackable)
		and self.weight == other.weight)

if __name__ == "__main__":
	domain = BlockTower()
	myPlan = Planner(domain)
	myPlan.planCausal()
	# state = BlockTowerState()
	# actions = domain.getValidActions(state)
	# print(CausalModel.chooseNextAction(actions))

