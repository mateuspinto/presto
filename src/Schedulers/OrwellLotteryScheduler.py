from Schedulers.ProcessList import ProcessList
from random import seed, randint, choice


class OrwellLotteryScheduler(object):
    """
    A simple Lottery Scheduler for multicore CPUS with preferencing.
    All processes are equal, but some processes are more equal - Orwell +-
    """

    def __init__(self):
        self.readyList = ProcessList()

    def name(self):
        return "Orwell Lottery Scheduler"

    def __str__(self):
        return "[" + self.name() + "]\n" + str(self.readyList)

    def __len__(self):
        return len(self.readyList)

    def isEmpty(self):
        return self.readyList.isEmpty()

    def addReadyProcess(self, pid: int, processTable):
        self.readyList.appendProcess(pid)

    def removeReadyProcess(self, pid: int):
        self.readyList.removeProcess(pid)

    def changePriorityBlockedProcess(self, pid: int, processTable):
        processTable.setPriority(pid, processTable.getPriority(pid) + 1)

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

        to_be_sorted = []

        for pid in self.readyList.queue:
            for _i in range(processTable.getPriority(pid)+1):
                to_be_sorted.append(pid)

        # While there is threads that can be executed and free processors
        while (not processor.isFull()) and (not self.isEmpty()):
            sorted_PID = choice(to_be_sorted)
            processor.appendProcess(sorted_PID)
            to_be_sorted = list(
                filter(lambda x: x != sorted_PID, to_be_sorted))
            self.removeReadyProcess(sorted_PID)

            if not sorted_PID in removed_from_processor:
                diagnostics.contextSwitch += 1
