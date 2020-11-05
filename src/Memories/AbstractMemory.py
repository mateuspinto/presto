import abc


class AbstractMemory(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def appendProcess(self, pid: int, numberOfVariables: int, processTable) -> int:
        """
        Append a new process and return the memory offset.
        """
        pass

    @abc.abstractmethod
    def name(self) -> str:
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        pass

    @abc.abstractmethod
    def popProcess(self, pid: int) -> None:
        pass

    @abc.abstractmethod
    def getValue(self, pid: int, variableNumber: int, processTable) -> int:
        pass

    @abc.abstractmethod
    def declare(self, pid: int, variableNumber: int, processTable) -> None:
        pass

    @abc.abstractmethod
    def setValue(self, pid: int, variableNumber: int, value: int, processTable) -> None:
        pass

    @abc.abstractmethod
    def moveToInfiniteMemory(self, pid: int, processTable, infiniteMemory) -> None:
        """
        Move all variables to virtual memory for final print
        """
        pass

    @abc.abstractmethod
    def haveMemoryAvailable(self, numberOfVariables: int) -> bool:
        pass
