import abc


class AbstractMemory(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def appendProcess(self, pid: int, numberOfVariables: int, processTable) -> int:
        """
        Append a new process and return the memory offset.
        """
        pass

    def name(self) -> str:
        pass

    def __str__(self) -> str:
        pass

    def popProcess(self, pid: int) -> None:
        pass

    def getValue(self, pid: int, variableNumber: int, processTable) -> int:
        pass

    def declare(self, pid: int, variableNumber: int, processTable) -> None:
        pass

    def setValue(self, pid: int, variableNumber: int, value: int, processTable) -> None:
        pass

    def moveToInfiniteMemory(self, pid: int, processTable, infiniteMemory) -> None:
        """
        Move all variables to virtual memory for final print
        """
        pass

    def haveMemoryAvailable(self, numberOfVariables: int) -> bool:
        pass
