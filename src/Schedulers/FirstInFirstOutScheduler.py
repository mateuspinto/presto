from Schedulers.ProcessList import ProcessList


class FirstInFirstOutScheduler(object):
    """
    A simple First-in First-out Scheduler for multicore CPUS
    """

    def __init__(self):
        self.readyList = ProcessList()
    
    def name(self):
        return "FIFO Scheduler"

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
