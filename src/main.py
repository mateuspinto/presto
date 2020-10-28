from ProcessTable import ProcessTable
from Processor import Processor, ProcessorEntry
from ProcessList import ProcessList
from Schedulers import FirstInFirstOutScheduler, ShortestJobFirstScheduler, ShortestRemainingTimeNextScheduler, RoundRobinScheduler, PriorityScheduler, MultipleQueuesScheduler, LotteryScheduler, OrwellLotteryScheduler
from InfiniteMemory import InfiniteMemory
from Diagnostics import Diagnostics
from MemoryManager import MemoryManager
from PhysicalMemory import PhysicalMemory

blockedIOList = ProcessList()
memoryManager = MemoryManager()
doneList = ProcessList()

processor = Processor(3)
processTable = ProcessTable()
memory = PhysicalMemory()
InfiniteMemory = InfiniteMemory()
scheduler = MultipleQueuesScheduler()

diagnostics = Diagnostics()

# Colocando primeiro processo na tabela de processos e na fila de execução
processTable.appendProcess(-1, 0, 0, 0)
processor.appendProcess(0)

time = 0
while not scheduler.isEmpty() or not processor.isEmpty():
    time += 1

    processor.runInstructions(time, memory, InfiniteMemory, processTable, scheduler, blockedIOList, memoryManager, doneList, diagnostics)
    print(memory)
    print(processor)
    print(processTable)
    print(memoryManager)
    scheduler.run(processor, processTable, diagnostics)
    memoryManager.run(memory, processor, scheduler, processTable)

print(InfiniteMemory)
print(diagnostics)