# qlearningAgents.py
# ------------------
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



from game import *
from menu import *
import random,math
class StateItem:
    def __init__(self, ball, player):
         
        self.x = int(ball.rect.centerx - player.rect.centerx)
        self.y = int(ball.rect.centery - player.rect.centery)
        self.size = ball.size
        self.speed = ball.speed.copy()
        
    def __str__(self):
        #print(str(self.x) + str(self.y) + str(self.size) + str(self.speed))
        return str(self.x) + str(self.y) + str(self.size) + str(self.speed)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.size == other.size and self.speed == other.speed
    def __hash__(self):
       # print(hash(str(self)))
        return hash(str(self))
class State:
    def __init__(self, stateItems, score, player):
         
        self.stateItems = stateItems
        self.player = player.getCopy()
        self.score = score
    def __str__(self):
        #print(repr(self.stateItems))
        return repr(self.stateItems)
    def __eq__(self, other):
        for item in self.stateItems:
            if(item not in other.stateItems):
                return False
        return True
    def __hash__(self):
      #  print(hash(str(self)))
        return hash(str(self))
class QLearningAgent:
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
      

        "*** YOUR CODE HERE ***"
        self.lastAction = None
        self.lastState = None
        self.qvalues = {}
        self.epsilon=0.05
        self.gamma=0.8
        self.alpha=0.4
        self.discount=0.5
 

        
            
    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
       
        #print('das')
            
        if str(state)+ action not in self.qvalues:
          return 0.0
        #print(self.qvalues[str(state)+ action])
        
        value = self.qvalues[str(state)+ action]
        del self.qvalues[str(state)+ action]
        self.qvalues[str(state)+ action] = value
        return value


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        nextLegalActions = self.legalAction(state.player)
        if len(nextLegalActions) == 0:
            return 0
        value = max([self.getQValue(state,action) for action
                     in nextLegalActions])
        
        return value

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        
        #if(player.rect.centerx < WINDOWWIDTH)
        nextPossibleActions = self.legalAction(state.player)[2:]
        #print(nextPossibleActions)
        random.shuffle(nextPossibleActions)
     
        if len(nextPossibleActions) == 0:
         #   print('asd')
            return None

        maxValue = float("-inf")
        newAction = None
        
        for action in nextPossibleActions:
            currValue = self.getQValue(state, action)
            if currValue > maxValue:
              maxValue = currValue
              newAction = action
        if(self.getQValue(state, 'FIRE')>=self.getQValue(state, 'NOT') ):
            
            return newAction,'FIRE'
    #    print('here')
        return newAction,'NOT'
    def legalAction(self, player):
        actions = ['FIRE','NOT']
        if player.rect.left > 0:
            actions.append('LEFT')
        if player.rect.right < WINDOWWIDTH:
            actions.append('RIGHT')

      #  print(actions)
        return actions
            
    def getAction(self, game):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.legalAction(game.players[0])
        fireAction = ['FIRE','NOT']
        action = None
        "*** YOUR CODE HERE ***"
        actionRandom = random.choice(legalActions[2:])
        fireRandom = random.choice(legalActions[:2])
        prob = self.flipCoin(self.epsilon)
        if(prob):
            return actionRandom,fireRandom

        state = State(set(StateItem(ball, game.players[0]) for ball in game.balls), game._score(game.players[0]),game.players[0])
        action,fire = self.computeActionFromQValues(state)
       # print(action,fire)
        self.update(state)
        self.lastState = state
        self.lastAction = action
        
        return action,fire

    def flipCoin( self,p ):
        r = random.random()
        return r < p
     
    def update(self, nextState):
        action = self.lastAction
        state = self.lastState
        #print(self.qvalues)
        if not self.lastState is None:
          #  print(state.score)
            reward = 0
            if(nextState.score > self.lastState.score):
                reward += nextState.score - self.lastState.score
            #print(nextState.player.lives - self.lastState.player.lives )
            reward += (nextState.player.lives - self.lastState.player.lives)* 10
            
            
            """
              The parent class calls this to observe a
              state = action => nextState and reward transition.
              You should do your Q-Value update here

              NOTE: You should never call this function,
              it will be called on your behalf
            """
            "*** YOUR CODE HERE ***"
            if str(state)+ action not in self.qvalues:
                #print('add')
                self.qvalues[str(state)+ action] = 0.0

            nextStateValue = self.computeValueFromQValues(nextState)
            currStateValue = self.qvalues[str(state)+ action]
            value = reward + (self.discount * nextStateValue) - currStateValue
           # print(value)

            self.qvalues[str(state)+ action] = currStateValue + (self.alpha * value)
            

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)
    


class BubbleTroubleQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(BubbleTroubleQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        BubbleTroubleQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        features = self.featExtractor.getFeatures(state, action)
        
        return sum([features[feature] * self.weights[feature] for feature in features])

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        features = self.featExtractor.getFeatures(state, action)
        difference = reward + self.discount * self.getValue(nextState) - self.getQValue(state, action)
        for feature in features:
            self.weights[feature] = self.weights[feature] + self.alpha * features[feature] * difference
       # util.raiseNotDefined()

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        BubbleTroubleQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            #print( self.weights)
            pass
