from Memories.MemoryItem import MemoryItem
from Memories.AbstractMemory import AbstractMemory


class InfiniteMemory(AbstractMemory):
    """
    A simple virtual memory implemented with a dict of lists. Each dict entry is a process.
    Each variable of the vectors are variables of the processes.
    """

    def __init__(self):
        self.memory = {}

    def appendProcess(self, pid: int, numberOfVariables: int, processTable, diagnostics) -> int:
        """
        Append a new process and return the memory offset (always zero).
        """
        self.memory[pid] = []

        for _i in range(numberOfVariables):
            self.memory[pid].append(MemoryItem())

        return 0

    def name(self) -> str:
        return "Infinite Memory"

    def __str__(self) -> str:
        display = "[" + self.name() + "]\n"

        for key in sorted(self.memory):
            display += "PID = " + str(key).zfill(3) + " >>> "
            for item in self.memory[key]:
                display += str(item) + " "
            display += "\n"

        return display[:-1]

    def popProcess(self, pid: int) -> None:
        self.memory.pop(pid)

    def getValue(self, pid: int, variableNumber: int, processTable) -> int:
        return self.memory[pid][variableNumber].getValue()

    def declare(self, pid: int, variableNumber: int, processTable) -> None:
        self.memory[pid][variableNumber].declare()

    def setValue(self, pid: int, variableNumber: int, value: int, processTable) -> None:
        self.memory[pid][variableNumber].setValue(value)

    def moveToInfiniteMemory(self, pid: int, processTable, infiniteMemory) -> None:
        """
        Move all variables to virtual memory for final print
        """
        pass

    def haveMemoryAvailable(self, numberOfVariables: int) -> bool:
        return True
