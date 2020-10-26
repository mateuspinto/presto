from TextSection import TextSection


class ProcessTable(object):
    """
    Table containing processes
    """

    def __init__(self):
        self.table = []

    def appendProcess(self, fpid: int, fileNumber: int, priority: int, initTime: int, limit: bool = False, startLine: int = 0, endLine: int = 0):
        self.table.append(ProcessTableItem(fpid, fileNumber,
                                           priority, initTime, limit, startLine, endLine))

    def popProcess(self, pid: int):
        self.table.pop(pid)

    def __str__(self):
        display = "[Process Table]\n"
        display += "PID | FPID | PC  | VAR | PRI | INT | CPT\n"

        for pid, process in enumerate(self.table, 0):
            display += str(pid).zfill(3) + " | " + str(process) + "\n"

        return display[:-1]

    def printTextSection(self, pid: int):
        self.table[pid].printTextSection()

    def setVariables(self, pid: int, variables: int):
        self.table[pid].variables = variables

    def increaseCPUTime(self, pid: int):
        self.table[pid].cpuTime += 1

    def fork(self, pid: int, howManyLines: int, time: int):
        self.appendProcess(
            pid, self.table[pid].code.fileNumber, self.table[pid].priority, time, True, self.getPC(pid), self.getPC(pid) + howManyLines - 1)

        return len(self.table) - 1

    def replaceTextSection(self, pid: int, newFileNumber: int):
        self.table[pid].replaceTextSection(newFileNumber)

    def getPC(self, pid: int):
        return self.table[pid].pc

    def increasePC(self, pid: int, count: int = 1):
        self.table[pid].increasePC(count)

    def getInstruction(self, pid: int, line: int):
        return self.table[pid].getInstruction(line)

    def getInitTime(self, pid: int):
        return self.table[pid].getInitTime()

    def newPID(self):
        return len(self.table)

    def resetPC(self, pid: int):
        self.table[pid].resetPC()


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
        self.pc = 0

    def __str__(self):
        return str(self.fpid).zfill(4) + " | " + str(self.pc).zfill(3) + " | " + str(self.variables).zfill(3) + " | " + str(self.priority).zfill(3) + " | " + str(self.initTime).zfill(3) + " | " + str(self.cpuTime).zfill(3)

    def setVariables(self, variables: int):
        self.variables = variables

    def setPriority(self, priority: int):
        self.priority = priority

    def increaseCPUTime(self):
        self.cpuTime += 1

    def printTextSection(self):
        print(self.code)

    def replaceTextSection(self, newFileNumber: int):
        self.code.replace(newFileNumber)

    def getPC(self):
        return self.pc

    def increasePC(self, count: id = 1):
        self.pc += count

    def getInstruction(self, line: int):
        return self.code.getInstruction(line)

    def getInitTime(self):
        return self.initTime

    def resetPC(self):
        self.pc = 0
