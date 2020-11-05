from Schedulers.ProcessList import ProcessList
from Schedulers.AbstractScheduler import AbstractScheduler

class ShortestJobFirstScheduler(AbstractScheduler):
    """
    A simple Shortest Job First Scheduler for multicore CPUS
    """

    def __init__(self):
        self.readyList = ProcessList()

    def name(self) -> str:
        return "Shortest Job First Scheduler"

    def __str__(self) -> str:
        return "[" + self.name() + "]\n" + str(self.readyList)

    def isEmpty(self) -> bool:
        return self.readyList.isEmpty()

    def addReadyProcess(self, pid: int, processTable) -> None:
        self.readyList.appendProcess(pid)

    def removeReadyProcess(self, pid: int) -> None:
        self.readyList.removeProcess(pid)

    def changePriorityBlockedProcess(self, pid: int, processTable) -> None:
        pass

    def getShortestPIDFromScheduler(self, processTable) -> int:
        ready_pid_time = []

        for elem in self.readyList.queue:
            ready_pid_time.append(
                (elem, processTable.predictTotalJobTime(elem)))

        return min(ready_pid_time, key=lambda tup: tup[1])[0]

    def getShortestTimeFromScheduler(self, processTable) -> int:
        ready_pid_time = []

        for elem in self.readyList.queue:
            ready_pid_time.append(
                (elem, processTable.predictTotalJobTime(elem)))

        return min(ready_pid_time, key=lambda tup: tup[1])[1]

    @staticmethod
    def getBiggestTimeFromProcessor(processor, processTable) -> int:
        ready_pid_time = []

        for thread in processor.threads:
            ready_pid_time.append(
                (thread.getPID(), processTable.predictTotalJobTime(thread.getPID())))

        return max(ready_pid_time, key=lambda tup: tup[1])[1]

    @staticmethod
    def getBiggestPIDFromProcessor(processor, processTable) -> int:
        ready_pid_time = []

        for thread in processor.threads:
            ready_pid_time.append(
                (thread.getPID(), processTable.predictTotalJobTime(thread.getPID())))

        return max(ready_pid_time, key=lambda tup: tup[1])[0]

    def run(self, processor, processTable, diagnostics) -> None:
        if self.isEmpty():
            return

        while not processor.isFull() and not self.isEmpty():
            processor.appendProcess(
                self.getShortestPIDFromScheduler(processTable))
            self.removeReadyProcess(
                self.getShortestPIDFromScheduler(processTable))

            diagnostics.processesAdded += 1

        if not processor.isEmpty() and not self.isEmpty():
            while self.getShortestTimeFromScheduler(processTable) < self.getBiggestTimeFromProcessor(processor, processTable):
                self.addReadyProcess(
                    self.getBiggestPIDFromProcessor(processor, processTable), processTable)
                processor.removeProcess(
                    self.getBiggestPIDFromProcessor(processor, processTable))

                processor.appendProcess(
                    self.getShortestPIDFromScheduler(processTable))
                self.removeReadyProcess(
                    self.getShortestPIDFromScheduler(processTable))

                diagnostics.contextSwitch += 1