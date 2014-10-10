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
from logic_extra import is_valid_cnf
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
    return reduce(lambda x, y: x | y, expressions)


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
    for i in xrange(50): #Assume MAX_TIME_STEPS = 50
        for action in actions:
            action_step = str(action) + "[" + str(i) + "]"
            if logic.PropSymbolExpr(action_step) in model.keys() and model[logic.PropSymbolExpr(action_step)]:
                plan.append(action)
    return plan

def transition_models(problem, time, actions, legal_actions):
    """
    Most important function, writes axioms about our fluents
    """
    models = []
    for i in xrange(1, problem.getWidth()+1):
        for j in xrange(1, problem.getHeight()+1):
            if not problem.isWall((i, j)):
                current_symbol = logic.PropSymbolExpr('P', i, j, time)
                expressions = []
                for action in actions:
                    previous_symbol = None
                    action_symbol = None
                    if action == Directions.EAST:
                        if (i-1, j, action) in legal_actions:
                            previous_symbol = logic.PropSymbolExpr('P', i-1, j, time-1)
                            action_symbol = logic.PropSymbolExpr(action, time-1)
                        else: continue
                    elif action == Directions.WEST:
                        if (i+1, j, action) in legal_actions:
                            previous_symbol = logic.PropSymbolExpr('P', i+1, j, time-1)
                            action_symbol = logic.PropSymbolExpr(action, time-1)
                        else: continue
                    elif action == Directions.NORTH:
                        if (i, j-1, action) in legal_actions:
                            previous_symbol = logic.PropSymbolExpr('P', i, j-1, time-1)
                            action_symbol = logic.PropSymbolExpr(action, time-1)
                        else: continue
                    elif action == Directions.SOUTH:
                        if (i, j+1, action) in legal_actions:
                            previous_symbol = logic.PropSymbolExpr('P', i, j+1, time-1)
                            action_symbol = logic.PropSymbolExpr(action, time-1)
                        else: continue
                        # NOTE: SHOULD NOT NEED TO STOP!
                        # elif action == Directions.STOP:
                        #     pass
                    expressions.append(previous_symbol & action_symbol)
            # before_cnf = current_symbol  % atLeastOne(expressions)

            models.append(logic.to_cnf(current_symbol  % atLeastOne(expressions))) # % means <=>, this is VERY UGLY
    return models

def get_initial_models(problem):
    initial_state = problem.getStartState() # pacman initial position
    models = [logic.PropSymbolExpr('P', initial_state[0], initial_state[1], 0)] # pacman at initial position at time 0
    walls = problem.walls
    width = problem.getWidth() + 2 #walls surround original grid
    height = problem.getHeight() + 2
    for i in xrange(width):
        for j in xrange(height):
            if i >= 1 and j >= 1 and i <=width-1 and j <= height-1:
                if i is not initial_state[0] or j is not initial_state[1]:
                    if walls[i][j]:
                        models.append(logic.PropSymbolExpr('W', i, j))
                    else:
                        models.append(~logic.PropSymbolExpr('W', i, j))
                    not_start_state = ~logic.PropSymbolExpr('P', i, j, 0)
                    models.append(not_start_state)
            else:
                if walls[i][j]:
                    models.append(logic.PropSymbolExpr('W', i, j))
                else:
                    models.append(~logic.PropSymbolExpr('W', i, j))
    return models

def goal_sentence(problem, t):
    goal_state = problem.getGoalState()
    goal_sentence = logic.PropSymbolExpr('P', goal_state[0], goal_state[1], t)
    return [goal_sentence]    
def create_action_exclusion_axioms(actions, time):
    expressions = []
    for action in actions:
        expressions.append(logic.PropSymbolExpr(action, time))
    return [exactlyOne(expressions)]


def positionLogicPlan(problem):
    """
    Given an instance of a PositionSearchProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    
    MAX_TIME_STEPS = 50
    actions = [Directions.NORTH, Directions.EAST, Directions.SOUTH, Directions.WEST]
    initial_models = get_initial_models(problem)
    successor_state_axioms = []
    action_exclusion_axioms = []
    legal_actions = set()
    for x in xrange(1, problem.getWidth()+1):
        for y in xrange(1, problem.getHeight()+1):
            if not problem.isWall((x, y)):
                for action in problem.actions((x, y)):
                    legal_actions.add((x, y, action))
    for t in xrange(MAX_TIME_STEPS):
        goal_assertion = goal_sentence(problem, t)
        if t > 0:
            successor_state_axioms += transition_models(problem, t, actions, legal_actions)
            action_exclusion_axioms += create_action_exclusion_axioms(actions, t-1)
        solution_model = logic.pycoSAT(initial_models + successor_state_axioms + goal_assertion + action_exclusion_axioms)
        if solution_model is not False:
            return extractActionSequence(solution_model, actions)
    return None

def get_food_initial_models(problem):
    initial_state = problem.getStartState() # pacman initial position
    models = [logic.PropSymbolExpr('P', initial_state[0][0], initial_state[0][1], 0)] # pacman at initial position at time 0
    walls = problem.walls
    width = problem.getWidth() + 2 #walls surround original grid
    height = problem.getHeight() + 2
    for i in xrange(width):
        for j in xrange(height):
            if i >= 1 and j >= 1 and i <=width-1 and j <= height-1:
                if i is not initial_state[0][0] or j is not initial_state[0][1]:
                    if walls[i][j]:
                        models.append(logic.PropSymbolExpr('W', i, j))
                    else:
                        models.append(~logic.PropSymbolExpr('W', i, j))
                    not_start_state = ~logic.PropSymbolExpr('P', i, j, 0)
                    models.append(not_start_state)
            else:
                if walls[i][j]:
                    models.append(logic.PropSymbolExpr('W', i, j))
                else:
                    models.append(~logic.PropSymbolExpr('W', i, j))
    return models

def get_food_axioms(problem, max_time):
        models = []
        food_list = problem.getStartState()[1].asList()
        for food in food_list:
            expressions = []
            for t in xrange(max_time+1):
                expressions.append(logic.PropSymbolExpr("P", food[0], food[1], t))
            if expressions:
                position_sentences = atLeastOne(expressions)
                before_cnf = ~logic.PropSymbolExpr("F", food[0], food[1]) % position_sentences
                models.append(logic.to_cnf(before_cnf))
        return models

def food_goal_sentence(problem, time):
        goal = []
        food_list = problem.getStartState()[1].asList()
        for food in food_list:
            goal.append(~logic.PropSymbolExpr("F", food[0], food[1]))
        expressions = []
        for position in food_list:
            expressions.append(logic.PropSymbolExpr("P", position[0], position[1], time))
        goal.append(atLeastOne(expressions))
        return goal

def foodLogicPlan(problem):
    """
    Given an instance of a FoodSearchProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    
    MAX_TIME_STEPS = 50
    actions = [Directions.NORTH, Directions.EAST, Directions.SOUTH, Directions.WEST]
    initial_models = get_food_initial_models(problem)
    successor_state_axioms = []
    action_exclusion_axioms = []
    legal_actions = set()
    for x in xrange(1, problem.getWidth()+1):
        for y in xrange(1, problem.getHeight()+1):
            if not problem.isWall((x, y)):
                for action in problem.actions(((x, y), problem.getStartState()[1])):
                    legal_actions.add((x, y, action))
    for t in xrange(MAX_TIME_STEPS):
        food_axioms = get_food_axioms(problem, t)
        goal_assertion = food_goal_sentence(problem, t)
        if t > 0:
            successor_state_axioms += transition_models(problem, t, actions, legal_actions)
            action_exclusion_axioms += create_action_exclusion_axioms(actions, t-1)
        sentence = initial_models + successor_state_axioms + goal_assertion + action_exclusion_axioms + food_axioms
        solution_model = logic.pycoSAT(sentence)
        if solution_model is not False:
            actions = extractActionSequence(solution_model, actions)
            return actions
    return None

def update_ghost_state(problem, location, goingEast):
    if goingEast:
        if problem.isWall((location[0]+1, location[1])):
            return [(location[0]-1, location[1]), False]
        else:
            return [(location[0]+1, location[1]), True]
    else: # go West young man!
        if problem.isWall((location[0]-1, location[1])):
            return [(location[0]+1, location[1]), True]
        else:
            return [(location[0]-1, location[1]), False]


def get_ghost_axioms(locations, time):
    axioms = []
    for location in locations:
        axioms.append(~logic.PropSymbolExpr('P', location[0], location[1], time))
        axioms.append(~logic.PropSymbolExpr('P', location[0], location[1], time+1))
    return axioms

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
    
    MAX_TIME_STEPS = 50
    actions = [Directions.NORTH, Directions.EAST, Directions.SOUTH, Directions.WEST]
    initial_models = get_food_initial_models(problem)
    successor_state_axioms = []
    action_exclusion_axioms = []
    ghost_axioms = []
    legal_actions = set()
    for x in xrange(1, problem.getWidth()+1):
        for y in xrange(1, problem.getHeight()+1):
            if not problem.isWall((x, y)):
                for action in problem.actions(((x, y), problem.getStartState()[1])):
                    legal_actions.add((x, y, action))
    ghost_states = []
    for agentstate in problem.getGhostStartStates():
        ghost_states.append([agentstate.getPosition(), True]) #(position, goingEast?)
    ghost_axioms += get_ghost_axioms(map(lambda x: x[0], ghost_states), 0)
    for t in xrange(MAX_TIME_STEPS):
        for i in xrange(len(ghost_states)):
            ghost_state = ghost_states[i]
            new_ghost_state = update_ghost_state(problem, ghost_state[0], ghost_state[1])
            ghost_states[i] = new_ghost_state
        ghost_axioms += get_ghost_axioms(map(lambda x: x[0], ghost_states), t+1)
        food_axioms = get_food_axioms(problem, t)
        goal_assertion = food_goal_sentence(problem, t)
        if t > 0:
            successor_state_axioms += transition_models(problem, t, actions, legal_actions)
            action_exclusion_axioms += create_action_exclusion_axioms(actions, t-1)
        sentence = initial_models + successor_state_axioms + goal_assertion + action_exclusion_axioms + food_axioms + ghost_axioms
        solution_model = logic.pycoSAT(sentence)

        if solution_model is not False:
            actions = extractActionSequence(solution_model, actions)
            return actions
    return None


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan
fglp = foodGhostLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)



