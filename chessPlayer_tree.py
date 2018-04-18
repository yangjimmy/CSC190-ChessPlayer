"""
Tree class
"""
from __future__ import print_function
import chessPlayer_queue as Queue

class tree:
    def __init__(self, x):
        self.store = [x, []]

    def AddSuccessor(self, x):
        """
        add child to tree (i.e. adds to list part of the tree node)
        NOTE: child is of type tree
        :param x: tree
        :type x: tree
        :return: completed operation
        :rtype: bool
        """
        self.store[1] = self.store[1] + [x]
        return True


    def Print_DepthFirst(self):
        """
        :return:
        :rtype: None
        """
        if self.store[1] == []:
            print(self.store[0])
        else:
            self.Print_DepthFirstHelper(0)


    def Print_DepthFirstHelper(self, depth):
       """

       :param: depth
       :type: int
       :return:
       :rtype: None
       """
       tabString = ""
       for i in range(depth):
           tabString = tabString + "\t"
       if self.store[1] == []:
           print(self.store[0])
       else:
           print(self.store[0])
           for t in self.store[1]:
               print(tabString+"\t", end="")
               t.Print_DepthFirstHelper(depth + 1)


    def Get_LevelOrder(self):
        """
        Gets level order traversal of tree
        :return: list
        """
        treequeue = Queue.Queue()
        for i in range(len(self.store)):
            treequeue.enqueue(self.store[i])
        levelorder = []
        while not treequeue.is_empty():
            item = treequeue.dequeue()
            if type(item) == None:
                pass
            elif type(item) == list and item == []:
                pass
            elif type(item) == list and type(item[0]) == list:
                # is a list of lists, can be added to the queue
                levelorder.append(item)
            else:
                # unpackage the tree
                for subtree in item:
                    for j in subtree.store:
                        treequeue.enqueue(j)
        return levelorder