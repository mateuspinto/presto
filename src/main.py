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

# Fingindo executar algumas instruções dele
Processor.allocMemory(0, 3, memoria, tabela_de_processos)
Processor.declare(0, 0, memoria, tabela_de_processos)
Processor.setValue(0, 0, 15, memoria, tabela_de_processos)

# Forkeandro processo 0
Processor.forkProcess(0, 3, 5, memoria, tabela_de_processos, readyQueue)

# Bloqueando processo 0
Processor.blockProcess(0, memoria, tabela_de_processos,
                       runingQueue, blockedQueue)

# Retirando processo 1 de pronto e colocando em rodando
readyQueue.popProcess(1)
runingQueue.appendProcess(1)

# Rodando replace no processo 1
Processor.replaceProcessImage(1, 1, memoria, tabela_de_processos)

print(tabela_de_processos)
print(memoria)

print("bloqueado")
print(blockedQueue)

print("rodando")
print(runingQueue)

print("pronto")
print(readyQueue)

tabela_de_processos.printTextSection(1)
