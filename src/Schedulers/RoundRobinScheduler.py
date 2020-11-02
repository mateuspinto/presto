from Schedulers.ProcessList import ProcessList


class RoundRobinScheduler(object):
    """
    Girando girando girando pra um lado, girando pro outro (brazilian music)
    """

    def __init__(self, quantum: int = 3):
        self.readyList = ProcessList()
        self.quantum = quantum
        self.currentTime = 0

    def __str__(self):
        return "[Round Robin Scheduler]\n" + str(self.readyList)

    def __len__(self):
        return len(self.readyList)

    def isEmpty(self):
        return self.readyList.isEmpty()

    def addReadyProcess(self, pid: int, processTable):
        self.readyList.appendProcess(pid)

    def removeReadyProcess(self, pid: int = 0):
        self.readyList.removeProcess(pid)

    def unqueueProcess(self):
        return self.readyList.unqueue()

    def changePriorityBlockedProcess(self, pid: int, processTable):
        pass

    def run(self, processor, processTable, diagnostics):

        if (self.currentTime < self.quantum) or self.isEmpty():
            self.currentTime += 1
            return

        for thread in processor.threads:
            self.addReadyProcess(thread.getPID(), processTable)
            processor.removeProcess(thread.getPID())

        while not processor.isFull() and not self.isEmpty():
            processor.appendProcess(self.unqueueProcess())
            diagnostics.contextSwitch += 1
