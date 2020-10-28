from ProcessTable import ProcessTable
from Processor import Processor, ProcessorEntry
from ProcessList import ProcessList
from Schedulers import FirstInFirstOutScheduler, ShortestJobFirstScheduler, ShortestRemainingTimeNextScheduler, RoundRobinScheduler, PriorityScheduler, LotteryScheduler, OrwellLotteryScheduler
from InfiniteMemory import InfiniteMemory
from Diagnostics import Diagnostics

blockedIOList = ProcessList()
blockedMmList = ProcessList()
doneList = ProcessList()

processor = Processor()
processTable = ProcessTable()
infiniteMemory = InfiniteMemory()
scheduler = OrwellLotteryScheduler()

diagnostics = Diagnostics()

# Colocando primeiro processo na tabela de processos e na fila de execução
processTable.appendProcess(-1, 0, 0, 0)
processor.appendProcess(0)

time = 0
while not scheduler.isEmpty() or not processor.isEmpty():
    time += 1

    processor.runInstructions(time, infiniteMemory, None, processTable, scheduler, blockedIOList, blockedMmList, doneList, diagnostics)
    scheduler.run(processor, processTable, diagnostics)

print(diagnostics)