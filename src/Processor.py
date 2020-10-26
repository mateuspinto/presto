class Processor(object):
    """
    A simple processor for the simulated language. Acts like a static class. There is no initializer or attributes.
    """

    @staticmethod
    def allocMemory(pid: int, numberOfVariables: int, memory, processTable):
        """
        Alloc some memory for the process.
        """

        processTable.increasePC(pid)
        processTable.increaseCPUTime(pid)

        memory_index = memory.appendProcess(pid, numberOfVariables)

        processTable.setVariables(pid, memory_index)

        print("Memory index = " + str(memory_index))

    @staticmethod
    def declare(pid: int, variableNumber: int, memory, processTable):
        """
        Declare a variable of the process, to be used later.
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
    def terminateProcess(pid: int, memory, processTable, runningQueue, doneQueue):

        runningQueue.popProcess(pid)
        doneQueue.appendProcess(pid)
        
        #memory.popProcess(pid)
        #processTable.popProcess(pid)

    @staticmethod
    def forkProcess(pid: int, howManyLines: int, initialTime: int, memory, processTable, readyQueue):

        processTable.increasePC(pid, howManyLines+1)
        processTable.increaseCPUTime(pid)

        son_PID:int = processTable.fork(pid, howManyLines, initialTime)
        readyQueue.appendProcess(son_PID)

    @staticmethod
    def replaceProcessImage(pid: int, newFileNumber: int, memory, processTable):

        processTable.increaseCPUTime(pid)

        processTable.replaceTextSection(pid, newFileNumber)
        processTable.resetPC(pid)

    @staticmethod
    def runSpecificInstruction(pid: int, line: int, time: int, memory, processTable, runningQueue, readyQueue, blockedQueue, doneQueue):

        instruction = processTable.getInstruction(pid, line)
        opcode: str = instruction.opcode
        n: int = instruction.n
        x: int = instruction.x

        if opcode == "N":
            Processor.allocMemory(pid, n, memory, processTable)
        elif opcode == "D":
            Processor.declare(pid, n, memory, processTable)
        elif opcode == "V":
            Processor.setValue(pid, n, x, memory, processTable)
        elif opcode == "A":
            Processor.addValue(pid, n, x, memory, processTable)
        elif opcode == "S":
            Processor.subValue(pid, n, x, memory, processTable)
        elif opcode == "B":
            Processor.blockProcess(pid, memory, processTable, runningQueue, blockedQueue)
        elif opcode == "T":
            Processor.terminateProcess(pid, memory, processTable, runningQueue, doneQueue)
        elif opcode == "F":
            Processor.forkProcess(pid, n, time, memory, processTable, readyQueue)
        elif opcode == "R":
            Processor.replaceProcessImage(pid, n, memory, processTable)
        else:
            pass

    @staticmethod
    def runInstruction(pid: int, time: int, memory, processTable, runningQueue, readyQueue, blockedQueue, doneQueue):
        
        Processor.runSpecificInstruction(pid, processTable.getPC(pid), time, memory, processTable, runningQueue, readyQueue, blockedQueue, doneQueue)