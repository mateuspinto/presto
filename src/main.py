from ProcessSimulator.Programs import *

a = TextSection(0)
print(a)

print("Fork da primeira instrução até a segunda")
a.fork(1,2)
print(a)

print("Replace por 1")
a.replace(1)
print(a)