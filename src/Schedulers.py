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


class ShortestFirstScheduler(object):
    """
    A simple Shortest First Scheduler for multicore CPUS
    """

    def __init__(self):
        self.readyList = ProcessList()

    def __str__(self):
        return "[Shortest First Scheduler]\n" + str(self.readyList)

    def isEmpty(self):
        return self.readyList.isEmpty()

    def addReadyProcess(self, pid: int):
        self.readyList.appendProcess(pid)

    def removeReadyProcess(self, pid: int):
        self.readyList.removeProcess(pid)

    def changePriorityBlockedProcess(self, pid: int):
        pass

    def getSmallestJobPID(self, processTable) -> int:
        ready_pid_time = []

        # Creating tuples on the form (PID, Job Time)
        for elem in self.readyList.queue:
            ready_pid_time.append(
                (elem, processTable.predictTotalJobTime(elem)))

        # Return the PID (first element of the tuple) from the tuple that has the minimal
        # value of Job Time
        return min(ready_pid_time, key=lambda tup: tup[1])[0]

    def run(self, processor, processTable):

        if not self.isEmpty():
            # While there is threads that can be executed and free processors
            for thread in processor.threads:
                if processTable.predictTotalJobTime(thread.getPID()) > self.getSmallestJobPID(processTable):
                    processor.removeProcess(thread.getPID())
                    self.addReadyProcess(thread.getPID())

            while (not processor.isFull()) and (not self.isEmpty()):
                pid_to_be_scheduled = self.getSmallestJobPID(processTable)

                self.removeReadyProcess(pid_to_be_scheduled)
                processor.appendProcess(pid_to_be_scheduled)


class ShortestRemainingTimeNextScheduler(object):
    """
    A simple Shortest Remaining Time Next for multicore CPUS
    """

    def __init__(self):
        self.readyList = ProcessList()

    def __str__(self):
        return "[Shortest Remaining Time Next]\n" + str(self.readyList)

    def isEmpty(self):
        return self.readyList.isEmpty()

    def addReadyProcess(self, pid: int):
        self.readyList.appendProcess(pid)

    def removeReadyProcess(self, pid: int):
        self.readyList.removeProcess(pid)

    def changePriorityBlockedProcess(self, pid: int):
        pass

    def getSmallestJobPID(self, processTable) -> int:
        ready_pid_time = []

        # Creating tuples on the form (PID, Job Time)
        for elem in self.readyList.queue:
            ready_pid_time.append(
                (elem, processTable.predictRemainingJobTime(elem)))

        # Return the PID (first element of the tuple) from the tuple that has the minimal
        # value of Job Time
        return min(ready_pid_time, key=lambda tup: tup[1])[0]

    def run(self, processor, processTable):

        if not self.isEmpty():
            # While there is threads that can be executed and free processors
            for thread in processor.threads:
                if processTable.predictRemainingJobTime(thread.getPID()) > self.getSmallestJobPID(processTable):
                    processor.removeProcess(thread.getPID())
                    self.addReadyProcess(thread.getPID())

            while (not processor.isFull()) and (not self.isEmpty()):
                pid_to_be_scheduled = self.getSmallestJobPID(processTable)

                self.removeReadyProcess(pid_to_be_scheduled)
                processor.appendProcess(pid_to_be_scheduled)
