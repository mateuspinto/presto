from MemoryItem import MemoryItem


class VirtualMemory(object):
    """
    A simple virtual memory implemented with a dict of lists. Each dict entry is a process.
    Each variable of the vectors are variable of the processes
    """

    def __init__(self):
        self.memory = {}

    def appendProcess(self, pid: int, numberOfVariables: int) -> int:
        self.memory[pid] = []

        for _i in range(numberOfVariables):
            self.memory[pid].append(MemoryItem())

        return 0

    def __str__(self):
        display = "[Virtual Memory]\n"

        for key in self.memory:
            display += "PID = " + str(key).zfill(3) + " >>> | "
            for item in self.memory[key]:
                display += str(item) + " | "
            display += "\n"

        return display[:-1]

    def popProcess(self, pid: int):
        self.memory.pop(pid)

    def getValue(self, pid: int, variableNumber: int):
        return self.memory[pid][variableNumber].getValue()

    def declare(self, pid: int, variableNumber: int):
        self.memory[pid][variableNumber].declare()

    def setValue(self, pid: int, variableNumber: int, value: int):
        self.memory[pid][variableNumber].setValue(value)
