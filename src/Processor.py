class Processor(object):
    """
    A simple processor for the simulated language.
    """

    def __init__(self, numberOfCores: int = 1):
        self.numberOfCores = numberOfCores
        self.threads = []

    def getNumberOfCores(self):
        return self.numberOfCores

    def getNumberOfProcess(self):
        return len(self.threads)

    def __str__(self):
        display = "[Processor]\n"
        display += "Core count = " + str(self.numberOfCores) + "\n"

        display += "PID | TIM"
        for i in self.threads:
            display += "\n" + str(i)

        return display

    def isFull(self):
        return self.numberOfCores == len(self.threads)

    def isEmpty(self):
        return len(self.threads) == 0

    def appendProcess(self, pid: int):
        self.threads.append(ProcessorEntry(pid))

    def removeProcess(self, pid: int):
        self.threads.remove(pid)

    def getQuantum(self, pid: int):
        return self.threads[self.threads.index(pid)].getQuantum()

    def increaseQuantum(self, pid: int, quantum: int = 1):
        return self.threads[self.threads.index(pid)].increaseQuantum(quantum)

    def runInstructions(self, time: int, memory, infiniteMemory, processTable, scheduler, blockedIOList, blockedMmList, doneList):
        for thread in self.threads:

            self.increaseQuantum(thread.getPID())
            self.runInstruction(thread.getPID(), time, memory, infiniteMemory,
                                processTable, scheduler, blockedIOList, blockedMmList, doneList)

    def allocMemory(self, pid: int, numberOfVariables: int, memory, processTable, scheduler, blockedMmList):
        """
        Alloc some memory for the process.
        """

        memory_index = memory.appendProcess(pid, numberOfVariables)

        if memory_index < 0:  # Index -1 means the memory allocation failed

            self.blockProcessByMemory(
                pid, processTable, scheduler, blockedMmList)
        else:

            processTable.increasePC(pid)
            processTable.increaseCPUTime(pid)

            processTable.setVariables(pid, memory_index)

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
        """
        Set the value from a variable
        """

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

    def blockProcessByIO(self, pid: int, memory, processTable, scheduler, blockedIOList):

        processTable.increasePC(pid)
        processTable.increaseCPUTime(pid)

        self.removeProcess(pid)
        blockedIOList.appendProcess(pid)
        scheduler.changePriorityBlockedProcess(pid)

    def blockProcessByMemory(self, pid: int, processTable, scheduler, blockedMmList):
        """
        Exception handler for non allocated memory
        """

        self.removeProcess(pid)
        blockedMmList.appendProcess(pid)
        scheduler.changePriorityBlockedProcess(pid)

    def terminateProcess(self, pid: int, memory, infiniteMemory, processTable, doneList):

        self.removeProcess(pid)
        doneList.appendProcess(pid)

        memory.moveToInfiniteMemory(pid, infiniteMemory)

    @staticmethod
    def forkProcess(pid: int, howManyLines: int, initialTime: int, memory, processTable, scheduler):

        processTable.increasePC(pid, howManyLines+1)
        processTable.increaseCPUTime(pid)

        son_PID: int = processTable.fork(pid, howManyLines, initialTime)
        scheduler.addReadyProcess(son_PID)

    @staticmethod
    def replaceProcessImage(pid: int, newFileNumber: int, memory, processTable):

        processTable.increaseCPUTime(pid)

        processTable.replaceTextSection(pid, newFileNumber)
        processTable.resetPC(pid)

    def runSpecificInstruction(self, pid: int, line: int, time: int, memory, infiniteMemoy, processTable, scheduler, blockedIOList, blockedMmList, doneList):

        instruction = processTable.getInstruction(pid, line)
        opcode: str = instruction.opcode
        n: int = instruction.n
        x: int = instruction.x

        if opcode == "N":
            self.allocMemory(
                pid, n, memory, processTable, scheduler, blockedMmList)
        elif opcode == "D":
            Processor.declare(pid, n, memory, processTable)
        elif opcode == "V":
            Processor.setValue(pid, n, x, memory, processTable)
        elif opcode == "A":
            Processor.addValue(pid, n, x, memory, processTable)
        elif opcode == "S":
            Processor.subValue(pid, n, x, memory, processTable)
        elif opcode == "B":
            self.blockProcessByIO(
                pid, memory, processTable, scheduler, blockedIOList)
        elif opcode == "T":
            self.terminateProcess(
                pid, memory, infiniteMemoy, processTable, doneList)
        elif opcode == "F":
            Processor.forkProcess(pid, n, time, memory,
                                  processTable, scheduler)
        elif opcode == "R":
            Processor.replaceProcessImage(pid, n, memory, processTable)
        else:
            pass

    def runInstruction(self, pid: int, time: int, memory, infiniteMemory, processTable, scheduler, blockedIOList, blockedMmList, doneList):

        self.runSpecificInstruction(pid, processTable.getPC(
            pid), time, memory, infiniteMemory, processTable, scheduler, blockedIOList, blockedMmList, doneList)


class ProcessorEntry(object):
    """
    A processor entry contains one PID and the timne spent in that process
    """

    def __init__(self, pid: int):
        self.pid = pid
        self.quantum = 0

    def __str__(self):
        return str(self.pid).zfill(3) + " | " + str(self.quantum).zfill(3)

    def increaseQuantum(self, time: int = 1):
        self.quantum += time

    def getPID(self):
        return self.pid

    def getQuantum(self):
        return self.quantum

    def __eq__(self, pid: int):
        return self.pid == pid
