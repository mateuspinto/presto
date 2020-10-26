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

    def getNPID(self, n: int = 0):
        return self.queue[n]

    def isEmpty(self) -> bool:
        return len(self.queue) == 0

    def __len__(self) -> int:
        return len(self.queue)

    def __str__(self):
        return str(self.queue)
