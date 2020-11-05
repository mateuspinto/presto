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

    def name(self):
        return str(self.numberOfCores) + "-Core Processor"

    def __str__(self):
        display = "[" + self.name() + "]\n"

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

    def appendPreferencialProcess(self, pid: int):
        self.threads.insert(0, ProcessorEntry(pid))

    def removeProcess(self, pid: int):
        self.threads.remove(pid)

    def getQuantum(self, pid: int):
        return self.threads[self.threads.index(pid)].getQuantum()

    def increaseQuantum(self, pid: int, quantum: int = 1):
        return self.threads[self.threads.index(pid)].increaseQuantum(quantum)

    def runInstructions(self, time: int, memory, infiniteMemory, processTable, scheduler, blockedIOList, memoryManager, doneList, diagnostics):
        for thread in self.threads:

            self.increaseQuantum(thread.getPID())
            self.runInstruction(thread.getPID(), time, memory, infiniteMemory,
                                processTable, scheduler, blockedIOList, memoryManager, doneList, diagnostics)

    def getEmptyThreads(self):
        return self.getNumberOfCores() - self.getNumberOfProcess()

    def allocMemory(self, pid: int, numberOfVariables: int, memory, processTable, scheduler, memoryManager, diagnostics):
        """
        Alloc some memory for the process.
        """

        memory_index = memory.appendProcess(
            pid, numberOfVariables, processTable, diagnostics)

        if memory_index < 0:  # Index -1 means the memory allocation failed

            self.blockProcessByMemory(
                pid, numberOfVariables, processTable, scheduler, memoryManager)
            diagnostics.mmAllocFailed += 1

        else:

            processTable.increasePC(pid)
            processTable.increaseCPUTime(pid)

            processTable.setVariablesOffset(pid, memory_index)
            processTable.setMemorySize(pid, numberOfVariables)
            diagnostics.mmAllocSucess += 1

    @staticmethod
    def declare(pid: int, variableNumber: int, memory, processTable):
        """
        Declare a variable of the process, to be used later.
        """

        processTable.increasePC(pid)
        processTable.increaseCPUTime(pid)

        memory.declare(pid, variableNumber, processTable)

    @staticmethod
    def setValue(pid: int, variableNumber: int, x: int, memory, processTable):
        """
        Set the value from a variable
        """

        processTable.increasePC(pid)
        processTable.increaseCPUTime(pid)

        memory.setValue(pid, variableNumber, x, processTable)

    @staticmethod
    def addValue(pid: int, variableNumber: int, x: int, memory, processTable):

        processTable.increasePC(pid)
        processTable.increaseCPUTime(pid)

        memory.setValue(pid, variableNumber, memory.getValue(
            pid, variableNumber, processTable) + x, processTable)

    @staticmethod
    def subValue(pid: int, variableNumber: int, x: int, memory, processTable):

        processTable.increasePC(pid)
        processTable.increaseCPUTime(pid)

        memory.setValue(pid, variableNumber, memory.getValue(
            pid, variableNumber, processTable) - x, processTable)

    def blockProcessByIO(self, pid: int, memory, processTable, scheduler, blockedIOList):

        processTable.increasePC(pid)
        processTable.increaseCPUTime(pid)

        self.removeProcess(pid)
        blockedIOList.appendProcess(pid)
        scheduler.changePriorityBlockedProcess(pid, processTable)

    def blockProcessByMemory(self, pid: int, numberOfVariables: int, processTable, scheduler, memoryManager):
        """
        Exception handler for non allocated memory
        """

        self.removeProcess(pid)
        memoryManager.addBlockedProcess(pid, numberOfVariables)
        scheduler.changePriorityBlockedProcess(pid, processTable)

    def terminateProcess(self, pid: int, memory, infiniteMemory, processTable, doneList):

        self.removeProcess(pid)
        doneList.appendProcess(pid)

        memory.moveToInfiniteMemory(pid, processTable, infiniteMemory)

    @staticmethod
    def forkProcess(pid: int, howManyLines: int, initialTime: int, memory, processTable, scheduler):

        processTable.increasePC(pid, howManyLines+1)
        processTable.increaseCPUTime(pid)

        son_PID: int = processTable.fork(pid, howManyLines, initialTime)
        scheduler.addReadyProcess(son_PID, processTable)

    @staticmethod
    def replaceProcessImage(pid: int, newFileNumber: int, memory, processTable):

        processTable.increaseCPUTime(pid)

        processTable.replaceTextSection(pid, newFileNumber)
        processTable.resetPC(pid)

    def runSpecificInstruction(self, pid: int, line: int, time: int, memory, infiniteMemoy, processTable, scheduler, blockedIOList, memoryManager, doneList, diagnostics):

        instruction = processTable.getInstruction(pid, line)
        opcode: str = instruction.opcode
        n: int = instruction.n
        x: int = instruction.x

        diagnostics.instructions += 1

        if opcode == "N":
            self.allocMemory(
                pid, n, memory, processTable, scheduler, memoryManager, diagnostics)
            diagnostics.N += 1
        elif opcode == "D":
            Processor.declare(pid, n, memory, processTable)
            diagnostics.D += 1
        elif opcode == "V":
            Processor.setValue(pid, n, x, memory, processTable)
            diagnostics.V += 1
        elif opcode == "A":
            Processor.addValue(pid, n, x, memory, processTable)
            diagnostics.A += 1
        elif opcode == "S":
            Processor.subValue(pid, n, x, memory, processTable)
            diagnostics.S += 1
        elif opcode == "B":
            self.blockProcessByIO(
                pid, memory, processTable, scheduler, blockedIOList)
            diagnostics.B += 1
        elif opcode == "T":
            self.terminateProcess(
                pid, memory, infiniteMemoy, processTable, doneList)
            diagnostics.T += 1
            diagnostics.rawResponseTime += time
        elif opcode == "F":
            Processor.forkProcess(pid, n, time, memory,
                                  processTable, scheduler)
            diagnostics.F += 1
        elif opcode == "R":
            Processor.replaceProcessImage(pid, n, memory, processTable)
            diagnostics.R += 1
        else:
            pass

    def runInstruction(self, pid: int, time: int, memory, infiniteMemory, processTable, scheduler, blockedIOList, memoryManager, doneList, diagnostics):

        self.runSpecificInstruction(pid, processTable.getPC(
            pid), time, memory, infiniteMemory, processTable, scheduler, blockedIOList, memoryManager, doneList, diagnostics)


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
