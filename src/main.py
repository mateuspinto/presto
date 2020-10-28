from ProcessTable import ProcessTable
from Processor import Processor, ProcessorEntry
from ProcessList import ProcessList
from Schedulers import FirstInFirstOutScheduler, ShortestJobFirstScheduler, ShortestRemainingTimeNextScheduler
from InfiniteMemory import InfiniteMemory

blockedIOList = ProcessList()
blockedMmList = ProcessList()
doneList = ProcessList()

processor = Processor(2)
processTable = ProcessTable()
infiniteMemory = InfiniteMemory()
scheduler = ShortestRemainingTimeNextScheduler()

# Colocando primeiro processo na tabela de processos e na fila de execução
processTable.appendProcess(-1, 0, 0, 0)
processor.appendProcess(0)

time = 0
while not scheduler.isEmpty() or not processor.isEmpty():
    time += 1

    processor.runInstructions(time, infiniteMemory, None, processTable, scheduler, blockedIOList, blockedMmList, doneList)
    scheduler.run(processor, processTable)

print(infiniteMemory)
print(processor)

print("[Blocked by IO List]")
print(blockedIOList)

print("[Done List]")
print(doneList)

print("total time = " + str(time))