from Schedulers.ProcessList import ProcessList
from random import seed, randint, choice


class LotteryScheduler(object):
    """
    A simple Lottery Scheduler for multicore CPUS
    """

    def __init__(self):
        self.readyList = ProcessList()

    def __str__(self):
        return "[Lottery Scheduler]\n" + str(self.readyList)

    def __len__(self):
        return len(self.readyList)

    def isEmpty(self):
        return self.readyList.isEmpty()

    def addReadyProcess(self, pid: int, processTable):
        self.readyList.appendProcess(pid)

    def removeReadyProcess(self, pid: int):
        self.readyList.removeProcess(pid)

    def changePriorityBlockedProcess(self, pid: int, processTable):
        pass

    def run(self, processor, processTable, diagnostics):

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
