from TextSection import TextSection


class ProcessTable(object):
    """
    Table containing processes
    """
    def __init__(self):
        self.table = []

    def appendProcess(self, fpid: int, fileNumber: int, priority: int, initTime: int, limit: bool = False, startLine: int = 0, endLine: int = 0):
        self.table.append(ProcessTableItem(fpid, fileNumber, priority, initTime, limit, startLine, endLine))

    def dropProcess(self, pid: int):
        self.table.pop(pid)

    def __str__(self):
        display = "PID | FPID | VAR | PRI | INT | CPT\n"
        for pid, process in enumerate(self.table, 1):
            display += str(pid).zfill(3) + " | " + str(process) + "\n"

        return display[:-1]

    def printTextSection(self, pid: int):
        self.table[pid].printTextSection()


class ProcessTableItem(object):
    """
    A entry in process table :3
    """

    def __init__(self, fpid: int, fileNumber: int, priority: int, initTime: int, limit: bool = False, startLine: int = 0, endLine: int = 0):
        self.fpid = fpid
        self.variables = -1
        self.code = TextSection(fileNumber, limit, startLine, endLine)
        self.priority = priority
        self.initTime = initTime
        self.cpuTime = 0

    def __str__(self):
        return str(self.fpid).zfill(4) + " | " + str(self.variables).zfill(3) + " | " + str(self.priority).zfill(3) + " | " + str(self.initTime).zfill(3) + " | " + str(self.cpuTime).zfill(3)

    def setVariables(self, variables: int):
        self.variables = variables

    def setPriority(self, priority: int):
        self.priority = priority

    def increaseCPUTime(self, cpuTimeElapsed: int):
        self.cpuTime += cpuTimeElapsed

    def printTextSection(self):
        print(self.code)