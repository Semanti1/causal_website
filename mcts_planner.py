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

class MCTreeValue():
    def __init__(self):
        self.playout = [0,0]
        self.action_state_list = []
        self.prev_state = None



class MonteCarloSearch():
    def __init__(self, domain):
        self.tree = dict() #[state][[play_out,visit_times], list(a',s'), prev_state]
        self.num_simulation = 20;
        self.domain = domain
        self.start_state = None
        self.action_seq = []

    def selection(self, state_list):
        score = []
        for state in state_list:
            playout = self.tree[state].playout;
            score.append(playout[0]/playout[1]);
        print("selection score: ", score)
        sel_idx = np.argmax(np.array(score))
        return state_list[sel_idx];

    def expansion(self, state):
        valid_action_list = self.domain.getValidActions(state);
        next_action_state_list = self.tree[state].action_state_list;
        #next_action_list = [a for a, _ in next_action_state_list]

        #print("in expansion: ", valid_action_list, next_action_state_list)
        select_action = None
        for action in valid_action_list:
            not_exist = True
            for next_action, _ in next_action_state_list:
                if(action == next_action):
                    not_exist =False;
                    break;
            if(not_exist):
                select_action = action
                break;
        if (select_action): #if there is an valid action not in current explored action list
            action.action.doAction(action.state, action.parameters)
            self.tree[state].action_state_list.append([action, action.state]) #update (a', s') list
            self.tree[action.state] = MCTreeValue();
            self.tree[action.state].prev_state = state; #update prev_state
            return action.state;
        else:
            return None;

    def simulation(self, state):
        valid_action_list = self.domain.getValidActions(state)
        final_score = -1;
        if (len(valid_action_list) ==0):
            playout_score, playout_times = self.tree[state].playout
            playout_score += 0
            playout_times += 1
            self.tree[state].playout = [playout_score, playout_times]
            return

        while(len(valid_action_list)!=0):
            random_action_index = math.floor(random.uniform(0, len(valid_action_list)))
            action = valid_action_list[random_action_index]
            #score = action.state.causal_graph.runModel(action.state, action)
            action.action.doAction(action.state, action.parameters)
            score = action.state.causal_graph.runModelfromState(action.state)
            valid_action_list = self.domain.getValidActions(action.state)
            if(len(valid_action_list) ==0):
                print(action.state, score)
                final_score = score
                break;
        #update playout score
        assert(final_score != -1)
        playout_score, playout_times = self.tree[state].playout
        playout_score += final_score
        playout_times += 1
        self.tree[state].playout = [playout_score, playout_times]

    def backprop(self, state):
        prev_state = self.tree[state].prev_state
        play_score = self.tree[state].playout
        while(prev_state != self.start_state):
            play_score_prev, play_times_prev = self.tree[prev_state].playout
            play_score_prev += play_score[0]
            play_times_prev +=1
            if prev_state not in self.tree:
                assert(1)
            self.tree[prev_state].playout = [play_score_prev, play_times_prev]
            prev_state = self.tree[prev_state].prev_state


    def run_tree(self, state):
        self.tree[state] = MCTreeValue();
        self.start_state = state
        while(not self.domain.isGoalSatisfied(state)):
            for i in range(0, self.num_simulation):
                next_state = self.expansion(state)
                if (next_state != None):
                    print("expansion: ", next_state)
                    self.simulation(next_state)
                    self.backprop(next_state)
                else: #expansion finish, need to explore deeper, call selection
                    action_state_list = self.tree[state].action_state_list
                    state_list = [s for _, s in action_state_list]
                    if (len(state_list)==0):
                        continue
                    next_state = self.selection(state_list)
                    print("selection: ", next_state)
                    state = next_state
            #decide which action to take from start_state
            final_score_list = []
            for action, next_state in self.tree[self.start_state].action_state_list:
                final_score_list.append(self.tree[next_state].playout[1])
            print("final_score_list", final_score_list)
            picked_idx = np.argmax(np.array(final_score_list))
            print("picked action: ", self.tree[self.start_state].action_state_list[picked_idx][0])
            state = self.tree[self.start_state].action_state_list[picked_idx][1]
            self.start_state = state
            self.tree = dict()
            self.tree[self.start_state] = MCTreeValue()
