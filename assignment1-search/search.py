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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    from util import Stack

    path = Stack()
    visited = set()

    path = dfsHelper(problem,path,problem.getStartState(),visited)

    return path.list
    

def dfsHelper(problem,path,currentNode,visited):
    visited.add(currentNode)

    if(problem.isGoalState(currentNode)):
        return path

    for successor in problem.getSuccessors(currentNode):
        if successor[0] not in visited:
            path.push(successor[1])
            result = dfsHelper(problem,path,successor[0],visited)
            if result is None:
                path.pop()
            else:
                return result
    
     


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    from util import Queue

    visited = set()
    frontier = Queue()
    cameFrom = {} # (k,v): node, node parent

    start = (problem.getStartState(),None,1)

    frontier.push(start)
    visited.add(start[0])
    while not frontier.isEmpty():
        currentNode = frontier.pop()

        if problem.isGoalState(currentNode[0]):
            return buildPathFromDict(currentNode, cameFrom)

        for successor in problem.getSuccessors(currentNode[0]):
            if successor[0] not in visited:
                frontier.push(successor)
                visited.add(successor[0])
                cameFrom[successor] = currentNode


def buildPathFromDict(currentNode, cameFrom):
    path = []
    while currentNode[1] is not None:
        path.append(currentNode[1])
        currentNode = cameFrom[currentNode]
    path.reverse()
    return path


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    from util import PriorityQueue

    nodePathCost = {} # (k,v): coordinate, lowest cost from start to node
    # frontier entry (coordinate, [path])
    frontier = PriorityQueue()
    frontier.push((problem.getStartState(),[]),0)
    nodePathCost[problem.getStartState()] = 0


    while not frontier.isEmpty():
        currentNode = frontier.pop()
        if problem.isGoalState(currentNode[0]):
            return currentNode[1]

        for successor in problem.getSuccessors(currentNode[0]):
            # compute path and cost for this node
            actions = currentNode[1] + [successor[1]]
            temp_pathCost = problem.getCostOfActions(actions)

            if successor[0] not in nodePathCost: # discovered new node
                frontier.push((successor[0],actions),temp_pathCost)
                nodePathCost[successor[0]] = temp_pathCost
            elif (nodePathCost[successor[0]] > temp_pathCost): 
                frontier.push((successor[0],actions),temp_pathCost) #if path to this node is better than a previously found path
                nodePathCost[successor[0]] = temp_pathCost



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearchOLD(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    from util import PriorityQueue

    closedSet = set() # set of nodes that have been evaluated
    cameFrom = {} # (k,v): node, parent node that reaches child most efficiently
    gScore = {} # g(node): cost of getting from start to node
    fScore = {} # f(node): g(node) + heuristic

    # priority queue with priority f(x) = g(x) + h(x)
    # entry = (coordinate, [path])
    openList = PriorityQueue()
    
    #initialize start values
    start = (problem.getStartState(),None,0)
    gScore[start[0]] = 0
    fScore[start[0]] = heuristic(start[0],problem)

    openList.push(start,fScore[start])

    while not openList.isEmpty():
        currentNode = openList.pop()
        closedSet.add(currentNode[0])

        if problem.isGoalState(currentNode[0]):
            return buildPathFromDict(currentNode,cameFrom)

  
        for successor in problem.getSuccessors(currentNode[0]):

            temp_gScore = gScore[currentNode[0]] + successor[2] # cost(start-current) + cost(current-successor)

            if successor[0] in closedSet:
                continue
            elif (successor[0] in gScore) and (temp_gScore >= gScore[successor[0]]):
                continue

            # this path is the best so far
            cameFrom[successor[0]] = currentNode
            gScore[successor[0]] = temp_gScore
            fScore[successor[0]] = gScore[successor[0]] + heuristic(successor[0],problem)
            openList.push(successor,fScore[successor[0]])

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    """Search the node that has the lowest combined cost and heuristic first."""
    from util import PriorityQueue

    closedSet = set() # set of nodes that have been evaluated
    cameFrom = {} # (k,v): node, parent node that reaches child most efficiently
    gScore = {} # g(node): cost of getting from start to node
    fScore = {} # f(node): g(node) + heuristic

    # priority queue with priority f(x) = g(x) + h(x)
    # entry = (coordinate, [path])
    openList = PriorityQueue()
    
    #initialize start values
    start = (problem.getStartState(),None,0)
    gScore[start[0]] = 0
    fScore[start[0]] = heuristic(start[0],problem)

    openList.push(start,fScore[start[0]])

    while not openList.isEmpty():
        currentNode = openList.pop()
        closedSet.add(currentNode[0])

        if problem.isGoalState(currentNode[0]):
            return buildPathFromDict(currentNode,cameFrom)

  
        for successor in problem.getSuccessors(currentNode[0]):

            temp_gScore = gScore[currentNode[0]] + successor[2] # cost(start-current) + cost(current-successor)

            if successor[0] in closedSet:
                continue
            elif (successor[0] in gScore) and (temp_gScore >= gScore[successor[0]]):
                continue

            # this path is the best so far
            cameFrom[successor] = currentNode
            gScore[successor[0]] = temp_gScore
            fScore[successor[0]] = gScore[successor[0]] + heuristic(successor[0],problem)
            openList.push(successor,fScore[successor[0]])



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
