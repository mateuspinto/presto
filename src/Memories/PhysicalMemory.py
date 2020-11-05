from Memories.MemoryItem import MemoryItem
from Memories.AbstractMemory import AbstractMemory


class PhysicalMemory(AbstractMemory):
    """
    A simple physical memory
    """

    def __init__(self, size: int = 20, algorithm: int = 0):
        self.memory = []
        self.lastVisited = 0
        self.algorithm = algorithm

        for _i in range(size):
            self.memory.append(PhysicalMemoryItem())

    def getFreeSegments(self):
        fits_list = []

        free_contiguous = 0

        for i in range(len(self.memory)):
            if not self.memory[i].isAllocated():
                free_contiguous += 1
            else:
                if free_contiguous != 0:
                    fits_list.append((i-free_contiguous+1, free_contiguous))
                free_contiguous = 0

        if free_contiguous != 0:
            fits_list.append((i-free_contiguous+1, free_contiguous))

        return fits_list

    def haveMemoryAvailable(self, numberOfVariables: int) -> bool:
        if len(self.getFits(numberOfVariables)) > 0:
            return True
        else:
            return False

    def getFits(self, numberOfVariables: int):
        fits_list = self.getFreeSegments()

        for i in range(len(fits_list)):
            if fits_list[i][1] < numberOfVariables:
                fits_list.pop(i)

        return fits_list

    def firstFit(self, numberOfVariables: int) -> int:
        fits_list = self.getFits(numberOfVariables)

        if len(fits_list) > 0:
            return fits_list[0][0]
        else:
            return -1

    def bestFit(self, numberOfVariables: int) -> int:
        fits_list = self.getFits(numberOfVariables)

        if len(fits_list) > 0:
            return min(fits_list, key=lambda tup: tup[1])[0]
        else:
            return -1

    def worstFit(self, numberOfVariables: int) -> int:
        fits_list = self.getFits(numberOfVariables)

        if len(fits_list) > 0:
            return max(fits_list, key=lambda tup: tup[1])[0]
        else:
            return -1

    def nextFit(self, numberOfVariables: int) -> int:
        fits_list = self.getFits(numberOfVariables)

        if len(fits_list) > 0:
            for i in range(len(fits_list)):
                if fits_list[i][0] >= self.lastVisited:
                    self.lastVisited = fits_list[i][0]
                    return fits_list[i][0]

            # A memory turnaround
            self.lastVisited = fits_list[0][0]
            return fits_list[0][0]
        else:
            return -1

    def appendProcess(self, pid: int, numberOfVariables: int, processTable) -> int:
        """
        Append a new process and return the memory offset.
        """

        if self.algorithm == 0:
            offset = self.firstFit(numberOfVariables)
        elif self.algorithm == 1:
            offset = self.bestFit(numberOfVariables)
        elif self.algorithm == 2:
            offset = self.worstFit(numberOfVariables)
        else:
            offset = self.nextFit(numberOfVariables)

        if offset < 0:
            return -1
        else:
            for i in range(offset, offset + numberOfVariables):
                self.memory[i].alloc()

            return offset

    def name(self):
        display = "Physical Memory"
        display += " (size: " + str(len(self.memory)) + ") "

        if self.algorithm == 0:
            display += "(First fit)"
        elif self.algorithm == 1:
            display += "(Best fit)"
        elif self.algorithm == 2:
            display += "(Worst fit)"
        elif self.algorithm == 3:
            display += "(Next fit)"

        return display

    def __str__(self):
        display = "[" + self.name() + "]\n"

        for number, item in enumerate(self.memory, 1):
            if number == 20:
                display += "\n"

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
