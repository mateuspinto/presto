class Instruction(object):
    """
    One instruction to be emulated by the simulator.
    """

    @staticmethod
    def isOpcodeValid(opcode: str) -> bool:
        """
        Check if a opcode is valid
        """

        if opcode in ['N', 'D', 'V', 'A', 'S', 'B', 'T', 'F', 'R']:
            return True
        else:
            return False

    @staticmethod
    def doesOpcodeHaveN(opcode: str) -> bool:
        """
        Check if a opcode requires the N field
        """

        if opcode in ['B', 'T']:
            return False
        else:
            return True

    @staticmethod
    def doesOpcodeHaveX(opcode: str) -> bool:
        """
        Check if a opcode requires the X field
        """

        if opcode in ['B', 'T', 'N', 'D', 'F', 'R']:
            return False
        else:
            return True

    def __init__(self, opcode: str, n: int, x: int):
        """
        Object constructor. Check if the opcode is valid and if N is an unsigned int
        """

        if not Instruction.isOpcodeValid(opcode):
            raise NameError("Opcode is not valid!")

        if n < 0:
            raise NameError("N must be greater or equals to zero!")

        self.opcode = opcode
        self.n = n
        self.x = x

    def __str__(self):
        display: str = self.opcode

        if self.hasN():
            display += ' ' + str(self.n)

        if self.hasX():
            display += ' ' + str(self.x)

        return display

    def hasN(self) -> bool:
        """
        Check if the instruction requires the N field
        """

        return Instruction.doesOpcodeHaveN(self.opcode)

    def hasX(self) -> bool:
        """
        Check if the instruction requires the X field
        """

        return Instruction.doesOpcodeHaveX(self.opcode)
