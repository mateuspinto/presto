from Schedulers.ProcessList import ProcessList
from Schedulers.AbstractScheduler import AbstractScheduler


class PriorityScheduler(AbstractScheduler):
    """
    A simple Priority Scheduler for multicore CPUS
    """

    def __init__(self):
        self.readyList = ProcessList()

    def name(self) -> str:
        return "Priority Scheduler"

    def __str__(self) -> str:
        return "[" + self.name() + "]\n" + str(self.readyList)

    def isEmpty(self) -> bool:
        return self.readyList.isEmpty()

    def addReadyProcess(self, pid: int, processTable) -> None:
        self.readyList.appendProcess(pid)

    def removeReadyProcess(self, pid: int) -> None:
        self.readyList.removeProcess(pid)

    def changePriorityBlockedProcess(self, pid: int, processTable) -> None:
        processTable.setPriority(pid, processTable.getPriority(pid) + 1)

    def getHighestPriorityPID(self, processTable) -> int:
        ready_pid_time = []

        # Creating tuples on the form (PID, Init Time)
        for elem in self.readyList.queue:
            ready_pid_time.append((elem, processTable.getPriority(elem)))

        # Return the PID (first element of the tuple) from the tuple that has the minimal
        # value of Init Time
        return min(ready_pid_time, key=lambda tup: tup[1])[0]

    def run(self, processor, processTable, diagnostics) -> None:

        # While there is threads that can be executed and free processors
        while (not processor.isFull()) and (not self.isEmpty()):
            pid_to_be_scheduled = self.getHighestPriorityPID(processTable)

            self.removeReadyProcess(pid_to_be_scheduled)
            processor.appendProcess(pid_to_be_scheduled)

            diagnostics.processesAdded += 1
