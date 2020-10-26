class FirstInFirstOutScheduler(object):
    """
    A simple First-in First-out Scheduler for multicore CPUS
    """

    def __init__(self, numberOfCores: int):
        self.numberOfCores = numberOfCores

    @staticmethod
    def getOldestPID(readyQueue, processTable) -> int:
        # TODO: refactor function
        ready_pid_time = []

        for elem in readyQueue.queue:
            ready_pid_time.append((elem, processTable.getInitTime(elem)))

        return sorted(ready_pid_time, key=lambda tup: tup[1])[0][0]

    def run(self, runningQueue, readyQueue, processTable):

        while ((runningQueue.len()) < self.numberOfCores) and (not readyQueue.isEmpty()):

            pid_to_be_scheduled = FirstInFirstOutScheduler.getOldestPID(
                readyQueue, processTable)

            readyQueue.popProcess(pid_to_be_scheduled)
            runningQueue.appendProcess(pid_to_be_scheduled)
