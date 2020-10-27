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
        while (processor.getNumberOfProcess() < processor.getNumberOfCores()) and (not self.isEmpty()):
            pid_to_be_scheduled = self.getOldestPID(processTable)

            self.removeReadyProcess(pid_to_be_scheduled)
            processor.appendProcess(pid_to_be_scheduled)
