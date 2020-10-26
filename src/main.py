from ProcessTable import ProcessTable
from VirtualMemory import VirtualMemory
from Processor import Processor
from ProcessQueue import ProcessQueue
from Schedulers import FirstInFirstOutScheduler

runingQueue = ProcessQueue()
blockedIOQueue = ProcessQueue()
blockedMmQueue = ProcessQueue()
readyQueue = ProcessQueue()
doneQueue = ProcessQueue()

processTable = ProcessTable()
memory = VirtualMemory()
scheduler = FirstInFirstOutScheduler()

# Colocando primeiro processo na tabela de processos e na fila de execução
processTable.appendProcess(-1, 0, 0, 0)
runingQueue.appendProcess(0)

time = 0
while not readyQueue.isEmpty() or not runingQueue.isEmpty():
    time += 1

    Processor.runInstruction(runingQueue.getNPID(), time, memory, None, processTable,
                             runingQueue, readyQueue, blockedIOQueue, blockedMmQueue, doneQueue)
    scheduler.run(runingQueue, readyQueue, processTable)

print(memory)
print(processTable)

print("[Runing Queue]")
print(runingQueue)

print("[Ready Queue]")
print(readyQueue)

print("[Blocked by IO Queue]")
print(blockedIOQueue)

print("[Done Queue]")
print(doneQueue)
