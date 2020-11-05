import abc


class AbstractScheduler(metaclass=abc.ABCMeta):
    """
    An abstract scheduler
    """

    @abc.abstractmethod
    def name(self) -> str:
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        pass

    @abc.abstractmethod
    def addReadyProcess(self, pid: int, processTable) -> None:
        pass

    @abc.abstractmethod
    def changePriorityBlockedProcess(self, pid: int, processTable) -> None:
        pass

    @abc.abstractmethod
    def run(self, processor, processTable, diagnostics) -> None:
        pass
