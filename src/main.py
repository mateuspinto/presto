from ProcessTable import ProcessTable
from Processor import Processor
from Diagnostics import Diagnostics
from Schedulers import *
from InterpretedLang import *
from Memories import *

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

    processor.runInstructions(time, memory, InfiniteMemory, processTable,
                              scheduler, blockedIOList, memoryManager, doneList, diagnostics)
    print(memory)
    print(processor)
    print(processTable)
    print(memoryManager)
    scheduler.run(processor, processTable, diagnostics)
    memoryManager.run(memory, processor, scheduler, processTable)

print(InfiniteMemory)
print(diagnostics)
