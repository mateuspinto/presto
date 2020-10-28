class MemoryManager(object):

    def __init__(self):
        self.blockedQueue = []

    def __len__(self):
        return len(self.blockedQueue)

    def __str__(self):
        display = "[Blocked by Memory Heap]"
        for tuple in self.blockedQueue:
            display += "\n" + str(tuple)

        return display

    def isEmpty(self):
        return len(self) == 0

    def addBlockedProcess(self, pid: int, numberOfVariables: int):
        self.blockedQueue.append((pid, numberOfVariables))

    def frontProcessNumberOfVariables(self):
        return min(self.blockedQueue, key=lambda tup: tup[1])[1]

    def popProcessPIDLessMemory(self):
        to_be_removed = (min(self.blockedQueue, key=lambda tup: tup[1])[
                         0], min(self.blockedQueue, key=lambda tup: tup[1])[1])
        self.blockedQueue.remove(to_be_removed)

        return to_be_removed[0]

    def run(self, memory, processor, scheduler, processTable):
        if not self.isEmpty():

            if processor.isFull():
                PID_to_remove = processor.thread[0].getPID()

                processor.removeProcess(PID_to_remove)
                scheduler.addReadyProcess(PID_to_remove, processTable)

            if memory.haveMemoryAvailable(self.frontProcessNumberOfVariables()):
                processor.appendPreferencialProcess(
                    self.popProcessPIDLessMemory())
