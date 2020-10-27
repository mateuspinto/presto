class FirstInFirstOutScheduler(object):
    """
    A simple First-in First-out Scheduler for multicore CPUS
    """

    def __init__(self, numberOfCores: int = 1):
        self.numberOfCores = numberOfCores

    @staticmethod
    def getOldestPID(readyList, processTable) -> int:
        ready_pid_time = []

        # Creating tuples on the form (PID, Init Time)
        for elem in readyList.queue:
            ready_pid_time.append((elem, processTable.getInitTime(elem)))

        # Return the PID (first element of the tuple) from the tuple that has the minimal
        # value of Init Time
        return min(ready_pid_time, key=lambda tup: tup[1])[0]

    def run(self, runningList, readyList, processTable):

        # While there is threads that can be executed and free processors
        while (len(runningList) < self.numberOfCores) and (not readyList.isEmpty()):
            pid_to_be_scheduled = FirstInFirstOutScheduler.getOldestPID(
                readyList, processTable)

            readyList.removeProcess(pid_to_be_scheduled)
            runningList.appendProcess(pid_to_be_scheduled)
