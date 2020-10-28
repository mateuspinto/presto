from ProcessList import ProcessList
from random import seed, randint, choice


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

    def changePriorityBlockedProcess(self, pid: int, processTable):
        pass

    def getOldestPID(self, processTable) -> int:
        ready_pid_time = []

        # Creating tuples on the form (PID, Init Time)
        for elem in self.readyList.queue:
            ready_pid_time.append((elem, processTable.getInitTime(elem)))

        # Return the PID (first element of the tuple) from the tuple that has the minimal
        # value of Init Time
        return min(ready_pid_time, key=lambda tup: tup[1])[0]

    def run(self, processor, processTable, diagnostics):

        # While there is threads that can be executed and free processors
        while (not processor.isFull()) and (not self.isEmpty()):
            pid_to_be_scheduled = self.getOldestPID(processTable)

            self.removeReadyProcess(pid_to_be_scheduled)
            processor.appendProcess(pid_to_be_scheduled)

            diagnostics.processesAdded += 1


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

    def changePriorityBlockedProcess(self, pid: int, processTable):
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
                    self.getBiggestPIDFromProcessor(processor, processTable))
                processor.removeProcess(
                    self.getBiggestPIDFromProcessor(processor, processTable))

                processor.appendProcess(
                    self.getShortestPIDFromScheduler(processTable))
                self.removeReadyProcess(
                    self.getShortestPIDFromScheduler(processTable))

                diagnostics.contextSwitch += 1


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
                    self.getBiggestPIDFromProcessor(processor, processTable))
                processor.removeProcess(
                    self.getBiggestPIDFromProcessor(processor, processTable))

                processor.appendProcess(
                    self.getShortestPIDFromScheduler(processTable))
                self.removeReadyProcess(
                    self.getShortestPIDFromScheduler(processTable))

            diagnostics.contextSwitch += 1


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

    def addReadyProcess(self, pid: int):
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
            self.addReadyProcess(thread.getPID())
            processor.removeProcess(thread.getPID())

        while not processor.isFull() and not self.isEmpty():
            processor.appendProcess(self.unqueueProcess())
            diagnostics.contextSwitch += 1


class PriorityScheduler(object):
    """
    A simple Priority Scheduler for multicore CPUS
    """

    def __init__(self):
        self.readyList = ProcessList()

    def __str__(self):
        return "[Priority Scheduler]\n" + str(self.readyList)

    def isEmpty(self):
        return self.readyList.isEmpty()

    def addReadyProcess(self, pid: int):
        self.readyList.appendProcess(pid)

    def removeReadyProcess(self, pid: int):
        self.readyList.removeProcess(pid)

    def changePriorityBlockedProcess(self, pid: int, processTable):
        processTable.setPriority(pid, processTable.getPriority(pid) + 1)

    def getHighestPriorityPID(self, processTable) -> int:
        ready_pid_time = []

        # Creating tuples on the form (PID, Init Time)
        for elem in self.readyList.queue:
            ready_pid_time.append((elem, processTable.getPriority(elem)))

        # Return the PID (first element of the tuple) from the tuple that has the minimal
        # value of Init Time
        return min(ready_pid_time, key=lambda tup: tup[1])[0]

    def run(self, processor, processTable, diagnostics):

        # While there is threads that can be executed and free processors
        while (not processor.isFull()) and (not self.isEmpty()):
            pid_to_be_scheduled = self.getHighestPriorityPID(processTable)

            self.removeReadyProcess(pid_to_be_scheduled)
            processor.appendProcess(pid_to_be_scheduled)

            diagnostics.processesAdded += 1


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

    def addReadyProcess(self, pid: int):
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
            self.addReadyProcess(thread.getPID())
            processor.removeProcess(thread.getPID())

            removed_from_processor.append(thread.getPID())

        # While there is threads that can be executed and free processors
        while (not processor.isFull()) and (not self.isEmpty()):
            sorted_PID = self.readyList.frontPID(randint(0, len(self)-1))
            processor.appendProcess(sorted_PID)
            self.removeReadyProcess(sorted_PID)

            if not sorted_PID in removed_from_processor:
                diagnostics.contextSwitch += 1


class OrwellLotteryScheduler(object):
    """
    A simple Lottery Scheduler for multicore CPUS with preferencing.
    All processes are equal, but some processes are more equal - Orwell +-
    """

    def __init__(self):
        self.readyList = ProcessList()

    def __str__(self):
        return "[Orwell Lottery Scheduler]\n" + str(self.readyList)

    def __len__(self):
        return len(self.readyList)

    def isEmpty(self):
        return self.readyList.isEmpty()

    def addReadyProcess(self, pid: int):
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
            self.addReadyProcess(thread.getPID())
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
