from MemoryItem import MemoryItem


class PhysicalMemory(object):
    """
    A simple physical memory
    """

    def __init__(self, size: int = 20):
        self.memory = []
        self.size = size

        for _i in range(self.size):
            self.memory.append(PhysicalMemoryItem())

    def firstFit(self, numberOfVariables: int) -> int:
        free_contiguous = 0
        i = 0

        while free_contiguous != numberOfVariables and i < self.size:
            if self.memory[i].isAllocated():
                free_contiguous = 0
            else:
                free_contiguous += 1
            i += 1

        if free_contiguous == numberOfVariables:
            return i - numberOfVariables
        else:
            return -1

    def appendProcess(self, pid: int, numberOfVariables: int, processTable) -> int:
        """
        Append a new process and return the memory offset.
        """

        offset = self.firstFit(numberOfVariables)

        if offset < 0:
            return -1
        else:
            for i in range(offset, offset + numberOfVariables):
                self.memory[i].alloc()

            return offset

    def __str__(self):
        display = "[Physical Memory]\n"

        for item in self.memory:
            display += str(item).zfill(3) + " "

        return display

    def popProcess(self, pid: int, processTable):
        for position in range(processTable.getVariablesOffset(pid), processTable.getVariablesOffset(pid) + processTable.getMemorySize(pid)):
            self.memory[position].unalloc()

    def getValue(self, pid: int, variableNumber: int, processTable):
        return self.memory[processTable.getVariablesOffset(pid) + variableNumber].getValue()

    def declare(self, pid: int, variableNumber: int, processTable):
        self.memory[processTable.getVariablesOffset(
            pid) + variableNumber].declare()

    def setValue(self, pid: int, variableNumber: int, value: int, processTable):
        self.memory[processTable.getVariablesOffset(
            pid) + variableNumber].setValue(value)

    def moveToInfiniteMemory(self, pid: int, processTable, infiniteMemory):
        number_of_variables = processTable.getMemorySize(pid)

        infiniteMemory.appendProcess(pid, number_of_variables, processTable)

        for variable in range(number_of_variables):
            infiniteMemory.declare(pid, variable, processTable)
            infiniteMemory.setValue(pid, variable, self.getValue(
                pid, variable, processTable), processTable)

        self.popProcess(pid, processTable)

    def haveMemoryAvailable(self, numberOfVariables: int) -> bool:
        if self.firstFit(numberOfVariables) < 0:
            return False
        else:
            return True


class PhysicalMemoryItem(MemoryItem):

    def __init__(self):
        self.declared = False
        self.allocated = False
        self.value = 0

    def __str__(self):
        if self.allocated:
            return MemoryItem.__str__(self)
        else:
            return " XXX "

    def alloc(self):
        self.allocated = True

    def unalloc(self):
        self.declared = False
        self.allocated = False
        self.value = 0

    def getValue(self) -> int:
        if not self.declared:
            raise NameError("Variable not declared!")

        if not self.allocated:
            raise NameError("Variable not allocated!")

        return self.value

    def setValue(self, value: int):
        if not self.declared:
            raise NameError("Variable not declared!")

        if not self.allocated:
            raise NameError("Variable not allocated!")

        self.value = value

    def isAllocated(self):
        return self.allocated
