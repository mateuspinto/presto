from ProcessTable import ProcessTable
from VirtualMemory import VirtualMemory
from Processor import Processor
from ProcessQueue import ProcessQueue

runingQueue = ProcessQueue()
blockedQueue = ProcessQueue()
readyQueue = ProcessQueue()
tabela_de_processos = ProcessTable()
memoria = VirtualMemory()


# Colocando primeiro processo na tabela de processos e na fila de execução
tabela_de_processos.appendProcess(-1, 0, 0, 0)
runingQueue.appendProcess(0)

for time in range(9):
    Processor.runInstruction(0, time, memoria, tabela_de_processos, runingQueue, readyQueue, blockedQueue)

print(memoria)
print(tabela_de_processos)

print("[Runing Queue]")
print(runingQueue)

print("[Ready Queue]")
print(readyQueue)

print("[Blocked Queue]")
print(blockedQueue)