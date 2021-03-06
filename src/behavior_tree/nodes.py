#!/usr/bin/env python3

import rospy

from abc import ABC, abstractmethod
import random


class Node(ABC):
    '''
    The Node class is an abstract class for every type of node in the behavior tree.
    This class is not meant to be initialized and instead used as a blueprint for other types
    of nodes.
    '''

    def __init__(self):

        return None 


    '''
    When tick() is called on a node it will return either "failure" if the action(s) associated with 
    the node have failed, "success" if they have completed, or "running" if they are still in progress.
    '''
    @abstractmethod
    def tick(self):

        options = ['failure', 'success', 'running']

        status = random.choice(options)

        return status


class ParentNode(Node):
    '''
    This class is a blueprint for different types of parent nodes in the behavior tree. 
    All parents will take in a list of child nodes as a parameter when initialized.
    The child nodes can either be action/conditional nodes, sequencers, or other selectors.
    '''

    def __init__(self, children):

        super().__init__()

        self.num_children = len(children)
        
        self.children = children
        

class Selector(ParentNode):
    '''
    The Selector class is a parent node in the behavior tree which ticks each of its children nodes
    in left-right order until one of them returns "success" or "running", and then returns the
    status back up the tree. If each child returns "failure", then the Selector will return 
    "failure" back up the tree.
    '''
        
    def tick(self, blackboard):

        status = 'failure'
        i = 0
        while (status == 'failure') and (i < self.num_children):

            status = self.children[i].tick(blackboard)
            i += 1
        
        return status


class Sequencer(ParentNode):
    '''
    The Sequencer class is a parent node in the behavior tree which ticks each of its children nodes
    in left-right order until one of them returns "failure" or "running", and then returns the
    status back up the tree. If each child returns "success", then the Sequencer will return 
    "success" back up the tree.
    '''

    def tick(self, blackboard):

        status = 'success'
        i = 0

        while (status == 'success') and (i < self.num_children):

            status = self.children[i].tick(blackboard)
            i += 1

        return status



class Action(Node):
    '''
    The Action class is a leaf node in the behavior tree which completes an action
    specified in the __init__ method. The user is required to customize their action 
    methods using this blueprint as a guide.

    Each action should be tick based, so during each tick the .tick() method of an action
    will either return "running", "failure", or "success" depending on the state of the action.

    This class is not meant to be initialized, but serves as an abstract parent class for users
    to construct their own actions with custom methods.
    '''


class Conditional(Node):
    '''
    The Conditional class is a leaf node in the behavior tree which returns either
    "success" or "failure" based on the boolean output from the callback function.
    Note that unlike other types of behavior tree nodes, a Conditional node will never
    return "running".
    
    The callback functon is passed in by the user and takes in the blackboard as the
    only input parameter.
    '''

    def __init__(self, cb):

        super().__init__()

        self.cb = cb



    def tick(self, blackboard):

        condition_met = self.cb(blackboard)

        if condition_met:
            
            return 'success'
        
        else:

            return 'failure'       