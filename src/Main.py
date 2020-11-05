import os
from simple_term_menu import TerminalMenu
from ProcessTable import ProcessTable
from Processor import Processor
from Diagnostics import Diagnostics
from Schedulers import *
from InterpretedLang import Instruction
from Memories import *


def clear_screen():
    os.system('clear')


def side_to_side_strings(strings, spacesBetween: int = 1):
    line_sizes = []
    summed_string = ""
    how_many_lines = max(len(i.split("\n")) for i in strings)

    for string in strings:
        max_count = 0
        actual_count = 0

        for char in string:
            if char == '\n':
                max_count = max([actual_count, max_count])
                actual_count = 0
            else:
                actual_count += 1

        max_count = max(actual_count, max_count)
        line_sizes.append(max_count)

    for i in range(how_many_lines):
        for string_number, string in enumerate(strings, 0):
            partial = ""

            try:
                partial += string.split('\n')[i]
            except:
                pass

            for _space in range(line_sizes[string_number] - len(partial) + spacesBetween):
                partial += " "

            partial += "|"

            for _space in range(spacesBetween):
                partial += " "

            summed_string += partial

        summed_string += "\n"

    return summed_string


def ask_key_interactive_mode():

    display = "U or Enter - Next time quantum;\n"
    display += "L - Unlock next process from blocked by IO list;\n"
    display += "M - Quit.\n\n"

    display += "Type an option: "

    return display


def simulator_state(processor, processTable, memory, infMemory, scheduler, memoryManager, blockedByIOList, doneList, diagnostics, time):
    display = side_to_side_strings(
        [str(processTable), str(processor), str(infMemory)], 2)
    display += "---------------------------------------------------------------------------------------------------------------------\n"
    display += side_to_side_strings([str(memory)]) + "\n"
    display += "---------------------------------------------------------------------------------------------------------------------\n"
    display += side_to_side_strings([str(scheduler),
                                     str(blockedByIOList), str(memoryManager),  str(doneList)]) + "\n"
    display += "---------------------------------------------------------------------------------------------------------------------\n"
    display += side_to_side_strings(
        [diagnostics.showInstructions(), str(diagnostics), "[Time]\nTime spent: " + str(time)])
    display += "---------------------------------------------------------------------------------------------------------------------\n"

    return display


def interactiveMode(time, processor, processTable, memory, InfiniteMemory, scheduler, memoryManager, blockedIOList, doneList, diagnostics):
    while True:
        clear_screen()
        print(simulator_state(processor, processTable, memory, InfiniteMemory,
                              scheduler, memoryManager, blockedIOList, doneList, diagnostics, time))
        print(ask_key_interactive_mode(), end='')

        try:
            typed_option = input()
        except:
            typed_option = "X"

        if typed_option == "U" or typed_option == "":
            time += 1
            processor.runInstructions(time, memory, InfiniteMemory, processTable,
                                      scheduler, blockedIOList, memoryManager, doneList, diagnostics)
            scheduler.run(processor, processTable, diagnostics)
            memoryManager.run(memory, processor, scheduler, processTable)

        elif typed_option == "L":
            try:
                pid = blockedIOList.unqueue()
                scheduler.addReadyProcess(pid, processTable)
            except:
                pass

        elif typed_option == "M":
            break

        else:
            pass


def runFile(time, processor, processTable, memory, InfiniteMemory, scheduler, memoryManager, blockedIOList, doneList, diagnostics):
    while True:
        try:
            inputNumber = int(input("Type a filenumber: "))
            file = open("input/" + str(inputNumber) + ".txt")
        except:
            inputNumber = -1
        if inputNumber >= 0:

            for raw_line in file:

                line = raw_line.strip()

                if line == "U":
                    time += 1
                    processor.runInstructions(time, memory, InfiniteMemory, processTable,
                                              scheduler, blockedIOList, memoryManager, doneList, diagnostics)
                    scheduler.run(processor, processTable, diagnostics)
                    memoryManager.run(memory, processor,
                                      scheduler, processTable)

                elif line == "L":
                    pid = blockedIOList.unqueue()
                    scheduler.addReadyProcess(pid, processTable)

                elif line == "I":
                    clear_screen()
                    print(simulator_state(processor, processTable, memory, InfiniteMemory,
                                          scheduler, memoryManager, blockedIOList, doneList, diagnostics, time))

                elif line == "M":
                    input("Press enter to continue; ")
                    return 0


def setNumberOfProcessors(processor):
    while True:
        inputNumber = int(
            input("Type how many processors do you want (n>0): "))
        if inputNumber > 0:
            processor.numberOfCores = inputNumber
            break


def setSchedulers(cursor, cursor_style, style):
    scheduler_menu_title = "  Select the scheduler\n"
    scheduler_menu_items = ["FIFO",
                            "Lottery", "Multiple Queues", "Orwell Lottery",
                            "Priority Scheduler",
                            "Round Robin",
                            "Shortest Job First",
                            "Shortestest remaining time next"]
    scheduler_menu = TerminalMenu(scheduler_menu_items,
                                  scheduler_menu_title,
                                  cursor,
                                  cursor_style,
                                  style,
                                  cycle_cursor=True,
                                  clear_screen=True)

    scheduler_sel = scheduler_menu.show()
    if scheduler_sel == 0:
        scheduler = FirstInFirstOutScheduler()
    elif scheduler_sel == 1:
        scheduler = LotteryScheduler()
    elif scheduler_sel == 2:
        while True:
            howManyQueues = int(
                input("How many queues do you want (n>0): "))
            if howManyQueues > 0:
                scheduler = MultipleQueuesScheduler(howManyQueues)
                break
    elif scheduler_sel == 3:
        scheduler = OrwellLotteryScheduler()
    elif scheduler_sel == 4:
        scheduler = PriorityScheduler()
    elif scheduler_sel == 5:
        while True:
            quantumSize = int(input("Type the quantum size (n>0): "))
            if quantumSize > 0:
                scheduler = RoundRobinScheduler(quantumSize)
                break
    elif scheduler_sel == 6:
        scheduler = ShortestJobFirstScheduler()
    elif scheduler_sel == 7:
        scheduler = ShortestRemainingTimeNextScheduler()

    return scheduler


def setAlgorithmFromPhysical(cursor, cursor_style, style):
    algorithm_menu_title = "  Select the Physical memory algorithm\n"
    algorithm_menu_items = ["First fit", "Best fit", "Worst fit", "Next fit"]
    algorithm_menu = TerminalMenu(algorithm_menu_items,
                                  algorithm_menu_title,
                                  cursor,
                                  cursor_style,
                                  style,
                                  cycle_cursor=True,
                                  clear_screen=True)

    return algorithm_menu.show()


def setMemory(cursor, cursor_style, style):
    memory_menu_title = "  Select the memory\n"
    memory_menu_items = ["Infinite Memory", "Physical Memory"]
    memory_menu = TerminalMenu(memory_menu_items,
                               memory_menu_title,
                               cursor,
                               cursor_style,
                               style,
                               cycle_cursor=True,
                               clear_screen=True)

    memory_sel = memory_menu.show()
    if memory_sel == 0:
        memory = InfiniteMemory()
    elif memory_sel == 1:
        while True:
            sizeMem = int(
                input("Input size of physical memory in int variables (n>0): "))
            if sizeMem > 0:
                clear_screen()
                break

        alg = setAlgorithmFromPhysical(cursor, cursor_style, style)
        memory = PhysicalMemory(sizeMem, alg)

    return memory


def SimulatorStatus(processor, memory, scheduler):
    display = "Using:\n"
    display += "- " + processor.name() + "\n"
    display += "- " + scheduler.name() + "\n"
    display += "- " + memory.name() + "\n"

    return display


def main(time, processor, processTable, memory, InfiniteMemory, scheduler, memoryManager, blockedIOList, doneList, diagnostics):
    while True:
        main_menu_title = "*** Simple process simulator Mk II ***\n"
        main_menu_title += "By Daniel, Leandro and Mateus\n\n"
        main_menu_title += ">>> Main Menu\n\n"
        main_menu_title += SimulatorStatus(processor, memory, scheduler)
        main_menu_items = ["Interactive Mode", "Run file", "Config", "Quit"]
        main_menu_cursor = "> "
        main_menu_cursor_style = ("fg_red", "bold")
        main_menu_style = ("bg_red", "fg_yellow")

        main_menu = TerminalMenu(menu_entries=main_menu_items,
                                 title=main_menu_title,
                                 menu_cursor=main_menu_cursor,
                                 menu_cursor_style=main_menu_cursor_style,
                                 menu_highlight_style=main_menu_style,
                                 cycle_cursor=True,
                                 clear_screen=True)
        main_sel = main_menu.show()

        if main_sel == 0:
            interactiveMode(time, processor, processTable, memory, InfiniteMemory,
                            scheduler, memoryManager, blockedIOList, doneList, diagnostics)
            return 0
        elif main_sel == 1:
            runFile(time, processor, processTable, memory, InfiniteMemory,
                    scheduler, memoryManager, blockedIOList, doneList, diagnostics)
            return 0
        elif main_sel == 2:
            config_menu_back = False
            while not config_menu_back:
                config_menu_title = ">>> Config menu\n\n"
                config_menu_title += SimulatorStatus(
                    processor, memory, scheduler)
                config_menu_items = ["Set number of processors",
                                     "Set process scheduler", "Set memory type", "Back to Main Menu"]
                config_menu = TerminalMenu(config_menu_items,
                                           config_menu_title,
                                           main_menu_cursor,
                                           main_menu_cursor_style,
                                           main_menu_style,
                                           cycle_cursor=True,
                                           clear_screen=True)
                config_sel = config_menu.show()
                if config_sel == 0:
                    setNumberOfProcessors(processor)
                elif config_sel == 1:
                    scheduler = setSchedulers(main_menu_cursor,
                                              main_menu_cursor_style, main_menu_style)
                elif config_sel == 2:
                    memory = setMemory(
                        main_menu_cursor, main_menu_cursor_style, main_menu_style)
                elif config_sel == 3:
                    config_menu_back = True
                    print("Back Selected")
        elif main_sel == 3:
            return 0


if __name__ == "__main__":
    blockedIOList = BlockedByIOList()
    memoryManager = MemoryManager()
    doneList = DoneList()

    processTable = ProcessTable()
    diagnostics = Diagnostics()

    processor = Processor(3)
    memory = InfiniteMemory()
    InfiniteMemory = InfiniteMemory()
    scheduler = MultipleQueuesScheduler()

    # Putting first process in processTable and processor (running list)
    processTable.appendProcess(-1, 0, 0, 0)
    processor.appendProcess(0)

    time: int = 0

    main(time, processor, processTable, memory, InfiniteMemory,
         scheduler, memoryManager, blockedIOList, doneList, diagnostics)

    print("Quit Selected. Thank u <3")
