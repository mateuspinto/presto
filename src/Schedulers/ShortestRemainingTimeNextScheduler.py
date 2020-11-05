from Schedulers.ProcessList import ProcessList


class ShortestRemainingTimeNextScheduler(object):
    """
    A simple Shortest Remaining Time Next Scheduler for multicore CPUS
    """

    def __init__(self):
        self.readyList = ProcessList()

    def name(self):
        return "Shortest Remaining Time Next Scheduler"

    def __str__(self):
        return "[" + self.name() + "]\n" + str(self.readyList)

    def isEmpty(self):
        return self.readyList.isEmpty()

    def addReadyProcess(self, pid: int, processTable):
        self.readyList.appendProcess(pid)

    def removeReadyProcess(self, pid: int):
        self.readyList.removeProcess(pid)

    def changePriorityBlockedProcess(self, pid: int, processTable):
        pass

    def getShortestPIDFromScheduler(self, processTable) -> int:
        ready_pid_time = []

        for elem in self.readyList.queue:
            ready_pid_time.append(
                (elem, processTable.predictRemainingJobTime(elem)))

        return min(ready_pid_time, key=lambda tup: tup[1])[0]

    def getShortestTimeFromScheduler(self, processTable) -> int:
        ready_pid_time = []

        for elem in self.readyList.queue:
            ready_pid_time.append(
                (elem, processTable.predictRemainingJobTime(elem)))

        return min(ready_pid_time, key=lambda tup: tup[1])[1]

    @staticmethod
    def getBiggestTimeFromProcessor(processor, processTable) -> int:
        ready_pid_time = []

        for thread in processor.threads:
            ready_pid_time.append(
                (thread.getPID(), processTable.predictRemainingJobTime(thread.getPID())))

        return max(ready_pid_time, key=lambda tup: tup[1])[1]

    @staticmethod
    def getBiggestPIDFromProcessor(processor, processTable) -> int:
        ready_pid_time = []

        for thread in processor.threads:
            ready_pid_time.append(
                (thread.getPID(), processTable.predictRemainingJobTime(thread.getPID())))

        return max(ready_pid_time, key=lambda tup: tup[1])[0]

    def run(self, processor, processTable, diagnostics):
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
