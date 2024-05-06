"""  		  	   		  		 		  		  		    	 		 		   		 		  
Template for implementing QLearner  (c) 2015 Tucker Balch  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		  		 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		  		 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		  		 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		  		 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 		  		  		    	 		 		   		 		  
or edited.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		  		 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		  		 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Student Name: Yu-Wei Lai 		  	   		  		 		  		  		    	 		 		   		 		  
GT User ID: ylai67  		  	   		  		 		  		  		    	 		 		   		 		  
GT ID: 903399610  		  	   		  		 		  		  		    	 		 		   		 		  
"""

import numpy as np
import random as rand

class QLearner(object):
    def __init__(  		  	   		  		 		  		  		    	 		 		   		 		  
        self,  		  	   		  		 		  		  		    	 		 		   		 		  
        num_states=100,  		  	   		  		 		  		  		    	 		 		   		 		  
        num_actions=4,  		  	   		  		 		  		  		    	 		 		   		 		  
        alpha=0.2,  		  	   		  		 		  		  		    	 		 		   		 		  
        gamma=0.9,  		  	   		  		 		  		  		    	 		 		   		 		  
        rar=0.5,  		  	   		  		 		  		  		    	 		 		   		 		  
        radr=0.99,  		  	   		  		 		  		  		    	 		 		   		 		  
        dyna=0,  		  	   		  		 		  		  		    	 		 		   		 		  
        verbose=False,  		  	   		  		 		  		  		    	 		 		   		 		  
    ):
        """  		  	   		  		 		  		  		    	 		 		   		 		  
        Constructor method  		  	   		  		 		  		  		    	 		 		   		 		  
        """
        
        self.verbose = verbose  		  	   		  		 		  		  		    	 		 		   		 		  
        self.num_actions = num_actions
        self.num_states = num_states  	   		  		 		  		  		    	 		 		   		 		  
        self.s = 0  		  	   		  		 		  		  		    	 		 		   		 		  
        self.a = 0
        
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        
        # initialize Q table with 0s following the project requirement
        self.Q = np.zeros((num_states, num_actions)) 
        
        # initialize list of experience for dyna
        self.experiences = []
        
    
    def author(self):
        return 'ylai67'
 
    def querysetstate(self, s):
        """  		  	   		  		 		  		  		    	 		 		   		 		  
        Update the state without updating the Q-table  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
        :param s: The new state  		  	   		  		 		  		  		    	 		 		   		 		  
        :type s: int  		  	   		  		 		  		  		    	 		 		   		 		  
        :return: The selected action  		  	   		  		 		  		  		    	 		 		   		 		  
        :rtype: int  		  	   		  		 		  		  		    	 		 		   		 		  
        """ 
        self.s = s
        # print('self.q', self.Q)
        
        # first, we flip a coin to decide whether we want to randomly chose an action  		  	   		  		 		  		  		    	 		 		   		 		  
        if rand.random() > self.rar:
            action = np.argmax(self.Q[s])
        else: 
            action = rand.randint(0, self.num_actions - 1)		  	   		  		 		  		  		    	 		 		   		 		  
        if self.verbose:  		  	   		  		 		  		  		    	 		 		   		 		  
            print(f"s = {s}, a = {action}")
        self.a = action  		  	   		  		 		  		  		    	 		 		   		 		  
        return action

    def query(self,s_prime,r):
        """  		  	   		  		 		  		  		    	 		 		   		 		  
        Update the Q table and return an action  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
        :param s_prime: The new state  		  	   		  		 		  		  		    	 		 		   		 		  
        :type s_prime: int  		  	   		  		 		  		  		    	 		 		   		 		  
        :param r: The immediate reward  		  	   		  		 		  		  		    	 		 		   		 		  
        :type r: float  		  	   		  		 		  		  		    	 		 		   		 		  
        :return: The selected action  		  	   		  		 		  		  		    	 		 		   		 		  
        :rtype: int  		  	   		  		 		  		  		    	 		 		   		 		  
        """
        
        # update Q table with value calculated from current s, a, s', r values
        self.calculate_Q(self.s, self.a, s_prime, r)
        
        # update experiences table
        self.experiences.append((self.s, self.a, s_prime, r))

        if self.dyna != 0:
            for _ in range(self.dyna):
                random_choice = np.random.randint(len(self.experiences))
                
                # pick a random experience from recorded experiences  
                experience = self.experiences[random_choice]
                
                # update Q table with the s, a, s', and r obtained from that experience
                self.calculate_Q(experience[0], experience[1], experience[2], experience[3])	 
                

        if rand.random() < self.rar:
            # random action
            action = rand.randint(0, self.num_actions - 1)
        else: 
            # choose the action with the highest Q value
            action = np.argmax(self.Q[s_prime])
            
        # update rar (random action decay rate), after each update, rar = rar * radr
        self.rar = self.rar * self.radr
        
        # update state and action
        self.s = s_prime
        self.a = action	
        
        if self.verbose: print("s =", s_prime,"a =", action,"r =",r)
        return action

    def calculate_Q(self, s, a, s_prime, r):
        """  		  	   		  		 		  		  		    	 		 		   		 		  
        Calculate values in the Q table 
        	   		  		 		  		  		    	 		 		   		 		  
  		:param s: The old new state  		  	   		  		 		  		  		    	 		 		   		 		  
        :type s: int 	   
        :param a: The action  		  	   		  		 		  		  		    	 		 		   		 		  
        :type a: int 		  		 		  		  		    	 		 		   		 		  
        :param s_prime: The new state  		  	   		  		 		  		  		    	 		 		   		 		  
        :type s_prime: int  		  	   		  		 		  		  		    	 		 		   		 		  
        :param r: The reward  		  	   		  		 		  		  		    	 		 		   		 		  
        :type r: float  		  	   		  		 		  		  		    	 		 		   		 		  
        :return: None		  	   		  		 		  		  		    	 		 		   		 		  
        :rtype: None  		  	   		  		 		  		  		    	 		 		   		 		  
        """
        self.Q[s, a] = (1 - self.alpha) * self.Q[s,a] + self.alpha * (r + self.gamma * self.Q[s_prime, np.argmax(self.Q[s_prime])]) 
                        

if __name__=="__main__":
    print("Remember Q from Star Trek? Well, this isn't him")
