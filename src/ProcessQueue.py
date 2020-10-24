class ProcessQueue(object):
    """
    A queue of PIDs. 
    """

    def __init__(self):
        self.queue = []

    def appendProcess(self, pid: int):
        self.queue.append(pid)

    def popProcess(self, pid: int):
        return self.queue.remove(pid)

    def __str__(self):
        return str(self.queue)