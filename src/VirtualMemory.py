from MemoryItem import MemoryItem


class VirtualMemory(object):
    """
    A simple virtual memory
    """

    def __init__(self):
        self.memory = {}

    def appendProcess(self, pid: int, numberOfVariables: int):
        self.memory[pid] = []

        for _i in range(numberOfVariables):
            self.memory[pid].append(MemoryItem())

    def __str__(self):
        display = ""
        for key in self.memory:
            display+= str(key) + " - "
            for item in self.memory[key]:
                display += str(item) + " "
            display+="\n"

        return display[:-1]

    def popProcess(self, pid: int):
        self.memory.pop(pid)

    def getValue(self, pid: int, variableNumber: int):
        return self.memory[pid][variableNumber].getValue()

    def declare(self, pid: int, variableNumber: int):
        self.memory[pid][variableNumber].declare()

    def setValue(self, pid: int, variableNumber: int, value: int):
        self.memory[pid][variableNumber].setValue(value)