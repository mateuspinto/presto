# -*- coding: utf-8 -*-
from ProcessTable import ProcessTable
from VirtualMemory import VirtualMemory
from Processor import Processor
from ProcessQueue import ProcessQueue
from Schedulers import FirstInFirstOutScheduler

runingQueue = ProcessQueue()
blockedQueue = ProcessQueue()
readyQueue = ProcessQueue()
doneQueue = ProcessQueue()


tabela_de_processos = ProcessTable()
memoria = VirtualMemory()
escalonador = FirstInFirstOutScheduler(1)


# Colocando primeiro processo na tabela de processos e na fila de execução
tabela_de_processos.appendProcess(-1, 0, 0, 0)
runingQueue.appendProcess(0)

time = 0

while not readyQueue.isEmpty() or not runingQueue.isEmpty():
    time += 1

    print(memoria)
    print(tabela_de_processos)

    print("[Runing Queue]")
    print(runingQueue)

    print("[Ready Queue]")
    print(readyQueue)

    print("[Blocked Queue]")
    print(blockedQueue)

    print("[Done Queue]")
    print(doneQueue)

    Processor.runInstruction(runingQueue.getFirstPID(), time, memoria, tabela_de_processos, runingQueue, readyQueue, blockedQueue, doneQueue)
    escalonador.run(runingQueue, readyQueue, tabela_de_processos)

print(memoria)
print(tabela_de_processos)

print("[Runing Queue]")
print(runingQueue)

print("[Ready Queue]")
print(readyQueue)

print("[Blocked Queue]")
print(blockedQueue)

print("[Done Queue]")
print(doneQueue)
