import os


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


def main_menu():
    display = "Bem vindo ao simulador de processos!\n"
    display += "Feito por Daniel, Leandro e Mateus.\n\n"

    display += "1 - Modo interativo;\n"
    display += "2 - Modo leitura de arquivos;\n"
    display += "3 - Configurações\n"

    display += "Por favor, digite uma opção: "

    return display


def main_invalid():
    display = "Bem vindo ao simulador de processos!\n"
    display += "Feito por Daniel, Leandro e Mateus.\n\n"

    display += "1 - Modo interativo;\n"
    display += "2 - Modo leitura de arquivos;\n"
    display += "3 - Configurações\n"

    display += "ERRO: Por favor, digite uma opção VÁLIDA: "

    return display


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def simulator_state(processor, processTable, memory, infMemory, scheduler, memoryManager, blockedByIOList, doneList, diagnostics):
    display = side_to_side_strings([str(processTable), str(processor), str(infMemory), str(doneList)], 2)
    display += "----------------------------------------------------------------------------------------------------------------------------------------------\n"
    display += side_to_side_strings([str(memory)]) + "\n"
    display += "----------------------------------------------------------------------------------------------------------------------------------------------\n"
    display += side_to_side_strings([str(scheduler), str(blockedByIOList), str(memoryManager)]) + "\n"
    display += "----------------------------------------------------------------------------------------------------------------------------------------------\n"
    display += side_to_side_strings([diagnostics.showInstructions(), str(diagnostics)])
    display += "----------------------------------------------------------------------------------------------------------------------------------------------\n"

    return display

def ask_key_interactive_mode():

    display = "U - Proximo tempo;\n"
    display += "L - Desbloqueia o próximo processo por IO;\n"
    display += "M - Sai do sistema.\n\n"

    display += "Digite uma opção válida: "

    return display


def ask_key_invalid():
    return "ERRO: Digite uma opção VÁLIDA: "