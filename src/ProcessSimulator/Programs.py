class ProgramList(object):
    """
    docstring
    """
    pass


class TextSection(object):
    """
    The text section of a program. Contains a list of instructions
    """
    pass


class Instruction(object):
    """
    One instruction to be emulated by the simulator.
    """

    def __init__(self, opcode: str, n: int, x: int):

        if not (opcode == ('N' or 'D' or 'V' or 'A' or 'S' or 'B' or 'T' or 'F' or 'R')) or n < 0:
            raise NameError("Opcode is not valid!")

        self.opcode = opcode
        self.n = n
        self.x = x
