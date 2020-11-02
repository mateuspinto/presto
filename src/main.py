from ProcessTable import ProcessTable
from Processor import Processor
from Diagnostics import Diagnostics
from Schedulers import *
from InterpretedLang import *
from Memories import *
from menuFunctions import *


blockedIOList = BlockedByIOList()
memoryManager = MemoryManager()
doneList = DoneList()

processTable = ProcessTable()
diagnostics = Diagnostics()

processor = Processor(3)
memory = PhysicalMemory()
InfiniteMemory = InfiniteMemory()
scheduler = MultipleQueuesScheduler()

# Colocando primeiro processo na tabela de processos e na fila de execução
processTable.appendProcess(-1, 0, 0, 0)
processor.appendProcess(0)

while True:
    clear_screen()
    print(main_menu(), end='')

    try:
        typed_option = input()
    except:
        typed_option = "X"

    if typed_option == "1":
        time = 0
        while True:

            clear_screen()
            print(simulator_state(processor, processTable, memory, InfiniteMemory,
                                  scheduler, memoryManager, blockedIOList, doneList, diagnostics))
            print(ask_key_interactive_mode(), end='')

            try:
                typed_option = input()
            except:
                typed_option = "X"

            if typed_option == "U":
                time += 1
                processor.runInstructions(time, memory, InfiniteMemory, processTable,
                                          scheduler, blockedIOList, memoryManager, doneList, diagnostics)
                scheduler.run(processor, processTable, diagnostics)
                memoryManager.run(memory, processor, scheduler, processTable)

            elif typed_option == "L":
                pid = blockedIOList.unqueue()
                scheduler.addReadyProcess(pid, processTable)

            elif typed_option == "M":
                exit(0)

            else:
                pass

    elif typed_option == "2":
        pass

    elif typed_option == "3":
        pass

    elif typed_option == "4":
        exit(0)

    else:
        pass


time = 0
while not scheduler.isEmpty() or not processor.isEmpty():
    time += 1

    processor.runInstructions(time, memory, InfiniteMemory, processTable,
                              scheduler, blockedIOList, memoryManager, doneList, diagnostics)
    print(side_to_side_strings([str(processTable), str(processor)], 3))
    scheduler.run(processor, processTable, diagnostics)
    memoryManager.run(memory, processor, scheduler, processTable)

print(InfiniteMemory)
print(diagnostics)
