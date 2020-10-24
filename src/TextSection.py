class TextSection(object):
    """
    The text section of a program. Contains a list of instructions.
    """

    def __read_file__(self, fileNumber: int, limit: bool = False, startLine: int = 0, endLine: int = 0):
        self.code = []
        self.fileNumber = fileNumber

        with open("programs/" + str(fileNumber) + ".txt") as file:

            if fileNumber < 0:
                raise NameError("fileNumber must be a unsigned int!")

            for line_number, line in enumerate(file, 1):

                if not limit or startLine <= line_number <= endLine:

                    try:
                        opcode = str(line.strip().split(' ')[0])
                    except:
                        raise NameError(
                            "Wrong syntax! Bad opcode! Error on line " + str(line_number))

                    try:
                        n = int(line.strip().split(' ')[1])
                    except:
                        n = 0

                    try:
                        x = int(line.strip().split(' ')[2])
                    except:
                        x = 0

                    try:
                        self.code.append(Instruction(opcode, n, x))
                    except:
                        raise NameError(
                            "Wrong syntax! Error on line = " + str(line_number))

    def __init__(self, fileNumber: int, limit: bool = False, startLine: int = 0, endLine: int = 0):
        self.__read_file__(fileNumber, limit, startLine, endLine)

    def __str__(self):
        display: str = ''

        for instruction in self.code:
            display += str(instruction) + '\n'

        return display[:-1]

    def replace(self, newFileNumber: int):
        self.__read_file__(newFileNumber)


class Instruction(object):
    """
    One instruction to be emulated by the simulator.
    """

    def __init__(self, opcode: str, n: int, x: int):

        if not (opcode == 'N' or opcode == 'D' or opcode == 'V' or opcode == 'A' or opcode == 'S' or opcode == 'B' or opcode == 'T' or opcode == 'F' or opcode == 'R'):
            raise NameError("Opcode is not valid!")

        if n < 0:
            raise NameError("N must be an unsigned int!")

        self.opcode = opcode
        self.n = n
        self.x = x

    def __str__(self):
        display: str = self.opcode

        if not (self.opcode == 'B' or self.opcode == 'T'):
            display += ' ' + str(self.n)

            if not (self.opcode == 'N' or self.opcode == 'D' or self.opcode == 'F' or self.opcode == 'R'):
                display += ' ' + str(self.x)

        return display
