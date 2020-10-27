from ProcessTable import ProcessTable
from Processor import Processor
from ProcessList import ProcessList
from Schedulers import FirstInFirstOutScheduler
from InfinityMemory import InfinityMemory

runingList = ProcessList()
blockedIOList = ProcessList()
blockedMmList = ProcessList()
readyList = ProcessList()
doneList = ProcessList()

processTable = ProcessTable()
memory = InfinityMemory()
scheduler = FirstInFirstOutScheduler()

# Colocando primeiro processo na tabela de processos e na fila de execução
processTable.appendProcess(-1, 0, 0, 0)
runingList.appendProcess(0)

time = 0
while not readyList.isEmpty() or not runingList.isEmpty():
    time += 1

    Processor.runInstruction(runingList.getNPID(), time, memory, None, processTable,
                             runingList, readyList, blockedIOList, blockedMmList, doneList)
    scheduler.run(runingList, readyList, processTable)

print(memory)
print(processTable)

print("[Runing List]")
print(runingList)

print("[Ready List]")
print(readyList)

print("[Blocked by IO List]")
print(blockedIOList)

print("[Done List]")
print(doneList)
