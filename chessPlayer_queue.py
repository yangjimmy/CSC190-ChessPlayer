"""
Queue helper class
"""

class Queue:
    """
    the class for queue implementation in Python
    includes enqueue and dequeue
    """

    def __init__(self):
        """
        :type self: Queue
        :rtype: None
        """
        self.data = []

    def enqueue(self, item):
        """

        :param item:
        :type item:
        :return:
        :rtype: None
        """
        self.data.append(item)

    def dequeue(self):
        """

        :return: completed operation or not
        :rtype:
        """
        if len(self.data) == 0:
            raise IndexError
        else:
            item = self.data[0]
            self.data = self.data[1:len(self.data)]
            return item


    def is_empty(self):
        """
        check if it is empty. if so return true else return false
        :return: if empty
        :rtype: bool
        """
        if len(self.data) == 0:
            return True
        else:
            return False

    def allint(self):
        """
        Checks if queue is all integers
        :return: true or false
        :rtype: bool
        """
        for i in self.data:
            if not isinstance(i, int):
                return False
        return True
