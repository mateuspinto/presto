class MemoryItem(object):
    """
    A generic item of memory. Contains the value (int) and the declared status (bool).
    """

    def __init__(self):
        self.value: int = 0
        self.declared: bool = False

    def declare(self):
        self.declared = True

    def getValue(self) -> int:
        if not self.declared:
            raise NameError("Variable not declared!")

        return self.value

    def setValue(self, value: int):
        if not self.declared:
            raise NameError("Variable not declared!")

        self.value = value

    def __str__(self):
        if self.declare:
            return "|" + str(self.value).zfill(3) + "|"
        else:
            return " " + str(self.value).zfill(3) + " "
