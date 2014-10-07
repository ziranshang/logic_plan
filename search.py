# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
from logic import pycoSAT
from game import Game, Directions


# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import sys
import logic

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostSearchProblem)
        """
        util.raiseNotDefined()

    def terminalTest(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionSearchProblem
        """
        util.raiseNotDefined()

    def result(self, state, action):
        """
        Given a state and an action, returns resulting state and step cost, which is
        the incremental cost of moving to that successor.
        Returns (next_state, cost)
        """
        util.raiseNotDefined()

    def actions(self, state):
        """
        Given a state, returns available actions.
        Returns a list of actions
        """        
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

    def getWidth(self):
        """
        Returns the width of the playable grid (does not include the external wall)
        Possible x positions for agents will be in range [1,width]
        """
        util.raiseNotDefined()

    def getHeight(self):
        """
        Returns the height of the playable grid (does not include the external wall)
        Possible y positions for agents will be in range [1,height]
        """
        util.raiseNotDefined()

    def isWall(self, position):
        """
        Return true if position (x,y) is a wall. Returns false otherwise.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def atLeastOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that at least one of the expressions in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    
    if len(expressions) <= 1:
        return expressions[0]
    
    expression_to_return = expressions[0]

    for i in range(len(expressions)):
        if i == 0:
            continue
        expression_to_return = expression_to_return | expressions[i]
    
    return expression_to_return


def atMostOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that at most one of the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"

    if len(expressions) <= 1:
        return expressions[0]

    expression_to_return = (~expressions[0]) | (~expressions[1]) 

    for i in range(len(expressions)):
        for j in range(len(expressions)):
            if (i == 0 and j == 1) or i == j:
                continue
                
            expression_to_return = expression_to_return & ((~expressions[i]) | (~expressions[j]))

    return expression_to_return


def exactlyOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that exactly one of the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    
    return atMostOne(expressions) & atLeastOne(expressions)
    
    util.raiseNotDefined()


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    plan = []
    for i in range(len(model.keys())): #TODO: check if I can simplify the possibilities of times...
        for action in actions:
            action_step = str(action) + "[" + str(i) + "]"
            if logic.PropSymbolExpr(action_step) in model.keys() and model[logic.PropSymbolExpr(action_step)]:
                plan.append(action)
    return plan


def positionLogicPlan(problem):
    """
    Given an instance of a PositionSearchProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    
    MAX_TIME_STEPS = 50
    
    def transition_models(problem, t):
        initial_state = problem.getStartState()
        transition_list = generate_successor_transitions(problem, initial_state, 0, t, [])
                
        return transition_list
    
    # generate successor state axioms for the next states
    # of the form: (next state at time t + 1) iff ((current state at time t) and (action to get to next state at time t))
    def generate_successor_transitions(problem, current_state, t_curr, t_max, visited_states):
        transition_list = []
#         if t_curr > t_max:
#             return []
        
        if current_state in visited_states:
            return []
        
        for action in problem.actions(current_state):
            current_state_symbol = logic.PropSymbolExpr('At', current_state[0], current_state[1], t_curr)
            current_state_expr = logic.Expr(str(current_state_symbol))
            next_state = problem.result(current_state, action)[0]
        
            # if we've already seen the resulting state, don't visit it
            if next_state in visited_states:
                continue
        
            next_state_symbol = logic.PropSymbolExpr('At', next_state[0], next_state[1], t_curr + 1)
            next_state_expr = logic.Expr(str(next_state_symbol))
            action_symbol = logic.PropSymbolExpr(action, t_curr)
            action_expr = logic.Expr(str(action_symbol))
            next_state_axiom = ~(next_state_expr ^ (current_state_expr & action_expr))            
            visited_states.append(current_state)
            transition_list.append(logic.to_cnf(next_state_axiom))
            
            # not sure if this should be here, may generate extra axioms in the loop
            action_exclusions = action_exclusion(problem, problem.actions(current_state), t_curr)
            
            print('successor axiom: ' + str(next_state_axiom))
            print('action exclusion axiom: ' + str (action_exclusions))
            
            # remove action exclusions for now
            #transition_list += action_exclusions
            
            # if the next state is the goal, don't find its successors
            if next_state == problem.getGoalState():
                continue
            
            transition_list += generate_successor_transitions(problem, next_state, t_curr + 1, t_max, visited_states) # generate successors for the next state
            
        transition_list += location_exclusion(problem, t_curr) # add location exclusions for this time step
        
        return transition_list
    
    # for all pairs of legal actions at a given time, ensure that you can only do one action at that time
    def action_exclusion(problem, actions, t):
        action_expression_list = []
        
        for action in actions:
            action_symbol = logic.PropSymbolExpr(action, t)
            action_expr = logic.Expr(str(action_symbol))
            action_expression_list.append(action_expr)
            
        action_exclusion_list = exactlyOne(action_expression_list)
        
        return [action_exclusion_list]
    
    # ensure that you cannot be in 2 places at the same time
    def location_exclusion(problem, t):
        location_expression_list = []

        for i in range(1, problem.getWidth() + 1):
            for j in range(1, problem.getHeight() + 1):
                location_symbol = logic.PropSymbolExpr('At', i, j, t)
                location_expr = logic.Expr(str(location_symbol))
                location_expression_list.append(location_expr)
                
        location_exclusion_list = exactlyOne(location_expression_list)        
    
        return [location_exclusion_list]
            
    # return goal sentence        
    def goal_sentence(problem, t):
        goal_state = problem.getGoalState()
        goal_symbol = logic.PropSymbolExpr('At', goal_state[0], goal_state[1], t)
        goal_expr = logic.Expr(str(goal_symbol)) # at goal state at time t
        
        return logic.to_cnf(goal_expr)
        
    # try to solve the sentence, starting with t = 1 and increasing if no solution is found
    def solve_sentence(problem, t_max):
        initial_state = problem.getStartState() # pacman initial position
        initial_symbol = logic.PropSymbolExpr('At', initial_state[0], initial_state[1], 0)
        initial_cnf = logic.to_cnf(logic.Expr(str(initial_symbol))) # pacman at initial position at time 0
        
        for t in range(1, t_max + 1):
            transition_and_exclusion_cnf = transition_models(problem, t)
            goal_cnf = goal_sentence(problem, t)
            cnf_to_solve = [initial_cnf] + transition_and_exclusion_cnf + [goal_cnf]
            
            solution_model = logic.pycoSAT(cnf_to_solve)
            
            print('initial state: ' + str(initial_cnf))
            print('transition states: ' + str(transition_and_exclusion_cnf))
            print('goal state: ' + str(goal_cnf))
            
            if not solution_model == False:
                return solution_model
    
    solution = solve_sentence(problem, MAX_TIME_STEPS) # max 50 time steps 
    actions = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
    
    print('solution model: ' + str(solution))
    print('solution moves: ' + str(extractActionSequence(solution, actions)))

    return extractActionSequence(solution, actions)
    
    util.raiseNotDefined()


def foodLogicPlan(problem):
    """
    Given an instance of a FoodSearchProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def foodGhostLogicPlan(problem):
    """
    Given an instance of a FoodGhostSearchProblem, return a list of actions that help Pacman
    eat all of the food and avoid patrolling ghosts.
    Ghosts only move east and west. They always start by moving East, unless they start next to
    and eastern wall. 
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan
fglp = foodGhostLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)



