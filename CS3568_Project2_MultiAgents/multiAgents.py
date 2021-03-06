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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        legalMoves.remove('Stop')

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        #for i in range(len(legalMoves)):
            #print(legalMoves[i], " -> ", scores[i])
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

        "*** CS3568 YOUR CODE HERE ***"
        "Decribe your function: ghost penalty is 3^(16-4d) where d is the distance to ghost. food reward is 1/d^4 where d is the distance from food."
        
        import math

        score = 0.0
        for g in currentGameState.getGhostStates():
            gDistance = manhattanDistance(successorGameState.getPacmanPosition(),g.getPosition())
            if g.scaredTimer<=1:
                score -= (3.0**(2.0-gDistance))
            else:
                score += (3.0**(2.0-gDistance))

        #print(successorGameState.getFood().height, successorGameState.getFood().width)
        nearest = math.inf
        for y in range(successorGameState.getFood().height):
            for x in range(successorGameState.getFood().width):
                if currentGameState.getFood()[x][y]:
                    #score += 1.0/(manhattanDistance(successorGameState.getPacmanPosition(),(x,y))**4.0)
                    #print("Food: ", (x,y))
                    if manhattanDistance(successorGameState.getPacmanPosition(),(x,y)) < nearest:
                        nearest = manhattanDistance(successorGameState.getPacmanPosition(),(x,y))
        score += 1.0/(nearest+0.5)
        #print("Pacman: ", successorGameState.getPacmanPosition())

        #return -manhattanDistance(successorGameState.getPacmanPosition(),(2,1))
        #print(successorGameState.getGhostStates()[0].getPosition())

        return score

        return successorGameState.getScore()

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** CS3568 YOUR CODE HERE ***"
        "PS. It is okay to define your own new functions. For example, value, min_function,max_function"

        import math
        legalMoves = gameState.getLegalActions(0)
        if 'Stop' in legalMoves:
            legalMoves.remove('Stop')
        successors = []
        for m in legalMoves:
            successors.append(gameState.generateSuccessor(0, m))
        value = -math.inf
        chosen_one = legalMoves[0]
        for s in successors:
            minimax_val = self.minimax(1, self.depth, s)
            if minimax_val > value:
                value = minimax_val
                chosen_one = legalMoves[successors.index(s)]

        return chosen_one

        util.raiseNotDefined()

    def minimax(self, agent, depth, gameState):
        import math
        if agent>=gameState.getNumAgents():
            agent=0
            depth -= 1
        if depth==0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agent==0:
            value = -math.inf
        else:
            value = math.inf
        legalMoves = gameState.getLegalActions(agent)
        if 'Stop' in legalMoves:
            legalMoves.remove('Stop')
        successors = []
        for m in legalMoves:
            successors.append(gameState.generateSuccessor(agent, m))
        for s in successors:
            minimax_val = self.minimax(agent+1, depth, s)
            if agent==0:
                if minimax_val > value:
                    value = minimax_val
            else:
                if minimax_val < value:
                    value = minimax_val

        return value

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** CS3568 YOUR CODE HERE ***"
        "PS. It is okay to define your own new functions. For example, value, min_function,max_function"
        util.raiseNotDefined()

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
        "*** CS3568 YOUR CODE HERE ***"
        "PS. It is okay to define your own new functions. For example, value, min_function,max_function"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** CS3568 YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
