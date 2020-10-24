from ProcessTable import ProcessTable

a = ProcessTable()
a.appendProcess(4, 0, 4, 3)

print("Tabela de processos:")
print(a)

print("Código do processo 0")
a.printTextSection(0)