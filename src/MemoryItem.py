class MemoryItem(object):
    """
    A generic item of memory
    """

    def __init__(self):
        self.value = 0
        self.declared = False

    def declare(self):
        self.declared = True

    def getValue(self) -> int:
        return self.value

    def setValue(self, value: int):
        if not self.declared:
            raise NameError("Variable not declared!")

        self.value = value

    def __str__(self):
        return str(self.declared) + " " + str(self.value)
