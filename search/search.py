# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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
import dataclasses

import util

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

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
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

def dfsRecursive(problem, state, actions, visited):
    for available_action in problem.getSuccessors(state):
        new_state, new_action, _ = available_action
        if new_state in visited:
            # already visited, choose another
            continue

        visited.add(new_state)
        actions.push(new_action)
        if problem.isGoalState(new_state):
            # found the goal, return the actions
            return actions.list
        else:
            # still looking
            result = dfsRecursive(problem, new_state, actions, visited)
            if not result:
                # did not find, revert action, choose another
                actions.pop()
            if result:
                return result
    # could not find
    return None

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    actions = util.Stack()
    state = problem.getStartState()
    visited = set([state])
    result = dfsRecursive(problem, state, actions, visited)
    return result

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    start = problem.getStartState()
    queue = util.Queue()
    actions = util.Stack()
    # initialise
    for successor in problem.getSuccessors(start):
        queue.push((successor, actions))
    visited = set([start])

    while not queue.isEmpty():
        successors, actions = queue.pop()
        state, action, _ = successors
        if state in visited:
            continue
        # copy actions stack
        updated_actions = util.Stack()
        for a in actions.list:
            updated_actions.push(a)

        updated_actions.push(action)
        if problem.isGoalState(state):
            return updated_actions.list
        visited.add(state)
        for successor in problem.getSuccessors(state):
            new_state, _, _ = successor
            queue.push((successor, updated_actions))

@dataclasses.dataclass
class Frontier:
    state: any
    actions: list
    total_cost: int


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    start = problem.getStartState()
    explored = set([start])
    # initialise first frontier
    frontiers = util.PriorityQueue()
    for successor, action, stepCost in problem.getSuccessors(start):
        frontiers.push(Frontier(state=successor, actions=[action], total_cost=stepCost), stepCost)
    while True:
        cheapest_frontier = frontiers.pop()
        state = cheapest_frontier.state
        if state in explored:
            continue
        explored.add(state)
        actions = cheapest_frontier.actions
        total_cost = cheapest_frontier.total_cost
        if problem.isGoalState(state):
            break
        for successor, action, stepCost in problem.getSuccessors(state):
            if successor in explored:
                continue
            new_total_cost = total_cost + stepCost
            frontiers.push(Frontier(state=successor, actions=[*actions, action], total_cost=new_total_cost), new_total_cost)
    return actions
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    start = problem.getStartState()
    explored = set([start])
    # initialise first frontier
    frontiers = util.PriorityQueue()
    for successor, action, stepCost in problem.getSuccessors(start):
        combined_cost = stepCost + heuristic(successor, problem)
        frontiers.push(Frontier(state=successor, actions=[action], total_cost=stepCost), combined_cost)
    while True:
        cheapest_frontier = frontiers.pop()
        state = cheapest_frontier.state
        if state in explored:
            continue
        explored.add(state)
        actions = cheapest_frontier.actions
        total_cost = cheapest_frontier.total_cost
        if problem.isGoalState(state):
            break
        for successor, action, stepCost in problem.getSuccessors(state):
            if successor in explored:
                continue
            new_total_cost = total_cost + stepCost
            combined_cost = new_total_cost + heuristic(successor, problem)
            frontiers.push(Frontier(state=successor, actions=[*actions, action], total_cost=new_total_cost), combined_cost)
    return actions

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
