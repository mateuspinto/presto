class Processor(object):
    """
    A simple processor for the simulated language 
    """

    @staticmethod
    def allocMemory(pid: int, numberOfVariables: int, memory, processTable):
        """
        Alloc some memory for the process
        """

        processTable.increasePC(pid)
        processTable.increaseCPUTime(pid)

        processTable.setVariables(
            pid, memory.appendProcess(pid, numberOfVariables))

    @staticmethod
    def declare(pid: int, variableNumber: int, memory, processTable):
        """
        Declare some variable of the process
        """

        processTable.increasePC(pid)
        processTable.increaseCPUTime(pid)

        memory.declare(pid, variableNumber)

    @staticmethod
    def setValue(pid: int, variableNumber: int, x: int, memory, processTable):

        processTable.increasePC(pid)
        processTable.increaseCPUTime(pid)

        memory.setValue(pid, variableNumber, x)


    @staticmethod
    def addValue(pid: int, variableNumber: int, x: int, memory, processTable):

        processTable.increasePC(pid)
        processTable.increaseCPUTime(pid)

        memory.setValue(pid, variableNumber,
                        memory.getValue(pid, variableNumber) + x)

    @staticmethod
    def subValue(pid: int, variableNumber: int, x: int, memory, processTable):

        processTable.increasePC(pid)
        processTable.increaseCPUTime(pid)

        memory.setValue(pid, variableNumber,
                        memory.getValue(pid, variableNumber) - x)

    @staticmethod
    def blockProcess(pid: int, memory, processTable, runningQueue, blockedQueue):

        processTable.increasePC(pid)
        processTable.increaseCPUTime(pid)

        runningQueue.popProcess(pid)
        blockedQueue.appendProcess(pid)

    @staticmethod
    def terminateProcess(pid: int, memory, processTable, runningQueue):

        runningQueue.popProcess(pid)
        memory.popProcess(pid)
        processTable.popProcess(pid)

    @staticmethod
    def forkProcess(pid: int, howManyLines: int, initialTime: int, memory, processTable, readyQueue):

        processTable.increasePC(pid)
        processTable.increaseCPUTime(pid)

        readyQueue.appendProcess(pid+1)
        processTable.fork(pid, howManyLines, initialTime)

    @staticmethod
    def replaceProcessImage(pid: int, newFileNumber: int, memory, processTable):

        processTable.increasePC(pid)
        processTable.increaseCPUTime(pid)

        processTable.replaceTextSection(pid, newFileNumber)
