# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        
        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newCapsules = successorGameState.getCapsules()

        from util import manhattanDistance, pause
        evaluation = successorGameState.getScore()
        #---------------------------------------------

        closestFood = 0
        stopweight = 0.75
        
        # penalize staying in the same place for an extended amount of time
        if(action == 'Stop'):
          if evaluation > 0: 
            return evaluation * stopweight
          else:
            return evaluation * 1/stopweight 


        numCurrentFood = len(currentGameState.getFood().asList())

        foodDists = [manhattanDistance(food, newPos) for food in newFood.asList()]
        numNewFood = len(foodDists)
        if(numNewFood): 
          closestFood = min(foodDists) # find closest new food
          evaluation += evaluation*(numCurrentFood - numNewFood) # give extra points for eating a food
          evaluation -= closestFood # the further you move away from food, the more you are penalized


        ghostsDist = [manhattanDistance(ghostState.getPosition(),newPos) for ghostState in newGhostStates]
        closestGhost = min(ghostsDist)

        if(closestGhost):
          evaluation -= abs(evaluation)*(1/closestGhost**4)

        return evaluation

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """
    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    def isTerminal(self,state,depth):
      return self.depth==depth or state.isWin() or state.isLose()

    def isPacMan(self,state,agent):
      return agent%state.getNumAgents() == self.index


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        def getValue(state,depth,agent,fn):
          successors = []
          for action in state.getLegalActions(agent):
            successors.append(minimax(state.generateSuccessor(agent,action),depth,agent+1))
          return fn(successors)


        def minimax(state,depth,agent):
          if agent == state.getNumAgents():
            return minimax(state,depth+1,0)

          if self.isTerminal(state,depth):
            return self.evaluationFunction(state)

          # if agent is maximizing player
          if self.isPacMan(state,agent): 
            return getValue(state,depth,agent,max) 
          else:
            return getValue(state,depth,agent,min)

        scores = []
        actions = gameState.getLegalActions(self.index)
        for action in actions:
          scores.append(minimax(gameState.generateSuccessor(0,action),0,1))

        return actions[scores.index(max(scores))]



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
<<<<<<< HEAD
        _MIN_START = float('Inf')
        _MAX_START = -_MIN_START

=======
>>>>>>> f4e23cf7d64be136c3ae5df7cae355884ae17ae2
        def getValue(state,depth,agent,alpha,beta,startScore,fn):
          bestScore = startScore
          bestAction = Directions.STOP
          for action in state.getLegalActions(agent):
            score,_ = minimax(state.generateSuccessor(agent,action),depth,agent+1,alpha,beta)
            bestScore,bestAction = fn((bestScore,bestAction),(score,action))
<<<<<<< HEAD

            if self.isPacMan(state,agent):
              if bestScore > beta:
                return bestScore,bestAction
              alpha = fn(alpha,bestScore)
            else:
              if bestScore < alpha:
                return bestScore,bestAction
              beta = fn(beta,bestScore)

          return bestScore,bestAction

=======

            if self.isPacMan(state,agent):
              if bestScore > beta:
                return bestScore,bestAction
              alpha = fn(alpha,bestScore)
            else:
              if bestScore < alpha:
                return bestScore,bestAction
              beta = fn(beta,bestScore)

          return bestScore,bestAction
>>>>>>> f4e23cf7d64be136c3ae5df7cae355884ae17ae2

        def minimax(state,depth,agent,alpha,beta):
          if agent == state.getNumAgents():
            return minimax(state,depth+1,0,alpha,beta)

<<<<<<< HEAD
          if self.isTerminal(state,depth):
            return self.evaluationFunction(state),None

          if self.isPacMan(state,agent): 
            return getValue(state,depth,agent,alpha,beta,_MAX_START,max) 
          else:
            return getValue(state,depth,agent,alpha,beta,_MIN_START,min)

        _,action = minimax(gameState,0,self.index,_MAX_START,_MIN_START)

        return action

=======
        def minimax(state,depth,agent,alpha=-float('Inf'),beta=float('Inf')):
          #print 'depth:',depth
          if agent == state.getNumAgents():
            return minimax(state,depth+1,0,alpha,beta)

          if self.isTerminal(state,depth):
            #print 'reached terminal state, depth=',depth
            return self.evaluationFunction(state),None

          # if agent is maximizing player
          if self.isPacMan(state,agent): 
            return getValue(state,depth,agent,alpha,beta,-float('Inf'),max) 
          else:
            return getValue(state,depth,agent,alpha,beta,float('Inf'),min)


        _,action = minimax(gameState,0,self.index)

        return action

>>>>>>> f4e23cf7d64be136c3ae5df7cae355884ae17ae2


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

