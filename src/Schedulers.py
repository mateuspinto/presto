from ProcessList import ProcessList


class FirstInFirstOutScheduler(object):
    """
    A simple First-in First-out Scheduler for multicore CPUS
    """

    def __init__(self):
        self.readyList = ProcessList()

    def __str__(self):
        return "[FIFO Scheduler]\n" + str(self.readyList)

    def isEmpty(self):
        return self.readyList.isEmpty()

    def addReadyProcess(self, pid: int):
        self.readyList.appendProcess(pid)

    def removeReadyProcess(self, pid: int):
        self.readyList.removeProcess(pid)

    def changePriorityBlockedProcess(self, pid: int):
        pass

    def getOldestPID(self, processTable) -> int:
        ready_pid_time = []

        # Creating tuples on the form (PID, Init Time)
        for elem in self.readyList.queue:
            ready_pid_time.append((elem, processTable.getInitTime(elem)))

        # Return the PID (first element of the tuple) from the tuple that has the minimal
        # value of Init Time
        return min(ready_pid_time, key=lambda tup: tup[1])[0]

    def run(self, processor, processTable):

        # While there is threads that can be executed and free processors
        while (not processor.isFull()) and (not self.isEmpty()):
            pid_to_be_scheduled = self.getOldestPID(processTable)

            self.removeReadyProcess(pid_to_be_scheduled)
            processor.appendProcess(pid_to_be_scheduled)


class ShortestJobFirstScheduler(object):
    """
    A simple Shortest Job First Scheduler for multicore CPUS
    """

    def __init__(self):
        self.readyList = ProcessList()

    def __str__(self):
        return "[Shortest Job First Scheduler]\n" + str(self.readyList)

    def isEmpty(self):
        return self.readyList.isEmpty()

    def addReadyProcess(self, pid: int):
        self.readyList.appendProcess(pid)

    def removeReadyProcess(self, pid: int):
        self.readyList.removeProcess(pid)

    def changePriorityBlockedProcess(self, pid: int):
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

    def run(self, processor, processTable):
        if self.isEmpty():
            return

        while not processor.isFull() and not self.isEmpty():
            processor.appendProcess(
                self.getShortestPIDFromScheduler(processTable))
            self.removeReadyProcess(
                self.getShortestPIDFromScheduler(processTable))

        if not processor.isEmpty() and not self.isEmpty():
            while self.getShortestTimeFromScheduler(processTable) < self.getBiggestTimeFromProcessor(processor, processTable):
                self.addReadyProcess(
                    self.getBiggestPIDFromProcessor(processor, processTable))
                processor.removeProcess(
                    self.getBiggestPIDFromProcessor(processor, processTable))

                processor.appendProcess(
                    self.getShortestPIDFromScheduler(processTable))
                self.removeReadyProcess(
                    self.getShortestPIDFromScheduler(processTable))


class ShortestRemainingTimeNextScheduler(object):
    """
    A simple Shortest Remaining Time Next Scheduler for multicore CPUS
    """

    def __init__(self):
        self.readyList = ProcessList()

    def __str__(self):
        return "[Shortest Remaining Time Next Scheduler]\n" + str(self.readyList)

    def isEmpty(self):
        return self.readyList.isEmpty()

    def addReadyProcess(self, pid: int):
        self.readyList.appendProcess(pid)

    def removeReadyProcess(self, pid: int):
        self.readyList.removeProcess(pid)

    def changePriorityBlockedProcess(self, pid: int):
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

    def run(self, processor, processTable):
        if self.isEmpty():
            return

        while not processor.isFull() and not self.isEmpty():
            processor.appendProcess(
                self.getShortestPIDFromScheduler(processTable))
            self.removeReadyProcess(
                self.getShortestPIDFromScheduler(processTable))

        if not processor.isEmpty() and not self.isEmpty():
            while self.getShortestTimeFromScheduler(processTable) < self.getBiggestTimeFromProcessor(processor, processTable):
                self.addReadyProcess(
                    self.getBiggestPIDFromProcessor(processor, processTable))
                processor.removeProcess(
                    self.getBiggestPIDFromProcessor(processor, processTable))

                processor.appendProcess(
                    self.getShortestPIDFromScheduler(processTable))
                self.removeReadyProcess(
                    self.getShortestPIDFromScheduler(processTable))
