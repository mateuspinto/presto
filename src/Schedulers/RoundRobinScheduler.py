from Schedulers.ProcessList import ProcessList
from Schedulers.AbstractScheduler import AbstractScheduler


class RoundRobinScheduler(AbstractScheduler):
    """
    Girando girando girando pra um lado, girando pro outro (brazilian music)
    """

    def __init__(self, quantum: int = 3):
        self.readyList = ProcessList()
        self.quantum = quantum
        self.currentTime = 0

    def name(self) -> str:
        return "Round Robin Scheduler (quantum: " + str(self.quantum) + ")"

    def __str__(self) -> str:
        return "[" + self.name() + "]\n" + str(self.readyList)

    def __len__(self) -> int:
        return len(self.readyList)

    def isEmpty(self) -> bool:
        return self.readyList.isEmpty()

    def addReadyProcess(self, pid: int, processTable) -> None:
        self.readyList.appendProcess(pid)

    def removeReadyProcess(self, pid: int = 0) -> None:
        self.readyList.removeProcess(pid)

    def unqueueProcess(self) -> int:
        return self.readyList.unqueue()

    def changePriorityBlockedProcess(self, pid: int, processTable) -> None:
        pass

    def run(self, processor, processTable, diagnostics) -> None:

        if (self.currentTime < self.quantum) or self.isEmpty():
            self.currentTime += 1
            return

        for thread in processor.threads:
            self.addReadyProcess(thread.getPID(), processTable)
            processor.removeProcess(thread.getPID())

        while not processor.isFull() and not self.isEmpty():
            processor.appendProcess(self.unqueueProcess())
            diagnostics.contextSwitch += 1
