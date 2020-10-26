class FirstInFirstOutScheduler(object):
    """
    A simple First-in First-out Scheduler for multicore CPUS
    """

    def __init__(self, numberOfCores: int = 1):
        self.numberOfCores = numberOfCores

    @staticmethod
    def getOldestPID(readyQueue, processTable) -> int:
        ready_pid_time = []

        # Creating tuples on the form (PID, Init Time)
        for elem in readyQueue.queue:
            ready_pid_time.append((elem, processTable.getInitTime(elem)))

        # Return the PID (first element of the tuple) from the tuple that has the minimal
        # value of Init Time
        return min(ready_pid_time, key=lambda tup: tup[1])[0]

    def run(self, runningQueue, readyQueue, processTable):

        # While there is threads that can be executed and free processors
        while (len(runningQueue) < self.numberOfCores) and (not readyQueue.isEmpty()):
            pid_to_be_scheduled = FirstInFirstOutScheduler.getOldestPID(
                readyQueue, processTable)

            readyQueue.popProcess(pid_to_be_scheduled)
            runningQueue.appendProcess(pid_to_be_scheduled)
