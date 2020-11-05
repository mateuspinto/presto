from Schedulers.ProcessList import ProcessList
from Schedulers.AbstractScheduler import AbstractScheduler


class MultipleQueuesScheduler(AbstractScheduler):
    """
    A simple Priority Scheduler for multicore CPUS
    """

    def __init__(self, NQueues: int = 3):
        self.NQueues = NQueues
        self.queues = []

        for _i in range(self.NQueues):
            self.queues.append([])

    def name(self) -> str:
        return str(self.NQueues) + " Queues Scheduler"

    def __str__(self):
        display = "[" + self.name() + "]"
        for queue in range(self.NQueues):
            display += "\nQueue " + str(queue) + " :"
            for pid in self.queues[queue]:
                display += " " + str(pid)

        return display

    def __len__(self) -> int:
        lenght = 0

        for i in range(self.NQueues):
            lenght += len(self.queues[i])

        return lenght

    def isEmpty(self) -> bool:
        return len(self) == 0

    def addReadyProcess(self, pid: int, processTable) -> None:
        self.queues[processTable.getPriority(pid)].append(pid)

    def changePriorityBlockedProcess(self, pid: int, processTable) -> None:
        if processTable.getPriority(pid) > 0:
            processTable.setPriority(pid, processTable.getPriority(pid) - 1)

    def run(self, processor, processTable, diagnostics) -> None:

        was_in_processor = []
        diagnostics.processesAdded += min(
            processor.getEmptyThreads(), len(self))

        if self.isEmpty():
            return

        for thread in processor.threads:
            if thread.getQuantum() >= pow(2, processTable.getPriority(thread.getPID())):
                self.addReadyProcess(thread.getPID(), processTable)
                processor.removeProcess(thread.getPID())
                was_in_processor.append(thread.getPID())

                if processTable.getPriority(thread.getPID()) < self.NQueues:
                    processTable.setPriority(
                        thread.getPID(), processTable.getPriority(thread.getPID()) + 1)

        i = 0
        while not processor.isFull() and not self.isEmpty() and i < self.NQueues:
            try:
                pid_sched = self.queues[i].pop()
                processor.appendProcess(pid_sched)

                if not pid_sched in was_in_processor:
                    diagnostics.contextSwitch += 1

            except IndexError:
                pass
            finally:
                i += 1
