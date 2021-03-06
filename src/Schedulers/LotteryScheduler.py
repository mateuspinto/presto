from Schedulers.ProcessList import ProcessList
from random import seed, randint, choice
from Schedulers.AbstractScheduler import AbstractScheduler


class LotteryScheduler(AbstractScheduler):
    """
    A simple Lottery Scheduler for multicore CPUS
    """

    def __init__(self):
        self.readyList = ProcessList()

    def name(self) -> str:
        return "Lottery Scheduler"

    def __str__(self) -> str:
        return "[" + self.name() + "]\n" + str(self.readyList)

    def __len__(self) -> int:
        return len(self.readyList)

    def isEmpty(self) -> bool:
        return self.readyList.isEmpty()

    def addReadyProcess(self, pid: int, processTable) -> None:
        self.readyList.appendProcess(pid)

    def removeReadyProcess(self, pid: int) -> None:
        self.readyList.removeProcess(pid)

    def changePriorityBlockedProcess(self, pid: int, processTable) -> None:
        pass

    def run(self, processor, processTable, diagnostics) -> None:

        if self.isEmpty():
            return

        diagnostics.processesAdded += min(
            processor.getEmptyThreads(), len(self))

        removed_from_processor = []

        for thread in processor.threads:
            self.addReadyProcess(thread.getPID(), processTable)
            processor.removeProcess(thread.getPID())

            removed_from_processor.append(thread.getPID())

        # While there is threads that can be executed and free processors
        while (not processor.isFull()) and (not self.isEmpty()):
            sorted_PID = self.readyList.frontPID(randint(0, len(self)-1))
            processor.appendProcess(sorted_PID)
            self.removeReadyProcess(sorted_PID)

            if not sorted_PID in removed_from_processor:
                diagnostics.contextSwitch += 1
