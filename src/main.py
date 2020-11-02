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
memory = InfiniteMemory()
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
        inputNumber = int(input("Digite um número de arquivo de entrada :"))
        read_file(int(inputNumber), processor, processTable, memory, InfiniteMemory,
                  scheduler, memoryManager, blockedIOList, doneList, diagnostics)
        exit(0)

    elif typed_option == "3":

        while True:
            clear_screen()
            print(config_menu(), end='')

            try:
                typed_option = input()
            except:
                typed_option = "X"

            if typed_option == "1":

                while True:
                    clear_screen()
                    try:
                        cores = int(
                            input("Digite o número de processadores: "))
                        processor = Processor(cores)
                        break
                    except:
                        pass

            elif typed_option == "2":

                while True:
                    clear_screen()
                    print(show_schedulers())

                    try:
                        scheduler_option = input()
                    except:
                        scheduler_option = "X"

                    if scheduler_option == "1":
                        scheduler = FirstInFirstOutScheduler()
                        break

                    elif scheduler_option == "2":
                        scheduler = LotteryScheduler()
                        break

                    elif scheduler_option == "3":
                        scheduler = MultipleQueuesScheduler(3)
                        break

                    elif scheduler_option == "4":
                        scheduler = OrwellLotteryScheduler()
                        break

                    elif scheduler_option == "5":
                        scheduler = PriorityScheduler()
                        break

                    elif scheduler_option == "6":
                        scheduler = RoundRobinScheduler()
                        break

                    elif scheduler_option == "7":
                        scheduler = ShortestJobFirstScheduler()
                        break

                    elif scheduler_option == "8":
                        scheduler = ShortestRemainingTimeNextScheduler()
                        break

                    else:
                        pass

            elif typed_option == "4":
                break

            else:
                pass

    elif typed_option == "4":
        break

    else:
        pass

print("Obrigado!\n")
