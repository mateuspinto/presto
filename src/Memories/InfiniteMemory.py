from Memories.MemoryItem import MemoryItem


class InfiniteMemory(object):
    """
    A simple virtual memory implemented with a dict of lists. Each dict entry is a process.
    Each variable of the vectors are variables of the processes.
    """

    def __init__(self):
        self.memory = {}

    def appendProcess(self, pid: int, numberOfVariables: int, processTable) -> int:
        """
        Append a new process and return the memory offset (always zero).
        """
        self.memory[pid] = []

        for _i in range(numberOfVariables):
            self.memory[pid].append(MemoryItem())

        return 0

    def __str__(self):
        display = "[Infinite Memory]\n"

        for key in sorted(self.memory):
            display += "PID = " + str(key).zfill(3) + " >>> "
            for item in self.memory[key]:
                display += str(item) + " "
            display += "\n"

        return display[:-1]

    def popProcess(self, pid: int):
        self.memory.pop(pid)

    def getValue(self, pid: int, variableNumber: int, processTable):
        return self.memory[pid][variableNumber].getValue()

    def declare(self, pid: int, variableNumber: int, processTable):
        self.memory[pid][variableNumber].declare()

    def setValue(self, pid: int, variableNumber: int, value: int, processTable):
        self.memory[pid][variableNumber].setValue(value)

    def moveToInfiniteMemory(self, pid: int, processTable, infiniteMemory):
        """
        Move all variables to virtual memory for final print
        """
        pass

    def haveMemoryAvailable(self, numberOfVariables: int):
        return True
