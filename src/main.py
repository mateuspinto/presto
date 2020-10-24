from textSection import TextSection

a = TextSection(0)
print(a)

print("Fork da primeira instrução até a segunda")
b = a.fork(1,2)
print(b)

print("Replace por 1")
b.replace(1)
print(b)