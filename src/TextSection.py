class TextSection(object):
    """
    The text section of a program. Contains a list of instructions.
    """

    def __read_file__(self, fileNumber: int, limited: bool = False, startLine: int = 0, endLine: int = 0):
        self.code = []
        self.fileNumber = fileNumber

        with open("programs/" + str(fileNumber) + ".txt") as file:

            if fileNumber < 0:
                raise NameError(
                    "fileNumber must be an integer greater or equals to zero!")

            for line_number, line in enumerate(file, 1):

                if (not limited) or (startLine <= line_number <= endLine) or line.startswith('#'):

                    opcode = str(line.strip().split(' ')[0])
                    n = 0
                    x = 0

                    if not Instruction.isOpcodeValid(opcode):
                        raise NameError(
                            "Wrong syntax! Opcode invalid! Error on line " + str(line_number))

                    if Instruction.doesOpcodeHaveN(opcode):
                        try:
                            n = int(line.strip().split(' ')[1])
                        except:
                            raise NameError(
                                "Wrong syntax! Opcode " + opcode + " requires the argument N, that was not given! Error on line " + str(line_number))

                    if Instruction.doesOpcodeHaveX(opcode):
                        try:
                            x = int(line.strip().split(' ')[2])
                        except:
                            raise NameError(
                                "Wrong syntax! Opcode " + opcode + " requires the argument X, that was not given! Error on line " + str(line_number))

                    try:
                        self.code.append(Instruction(opcode, n, x))
                    except:
                        raise NameError(
                            "Wrong syntax! Error on line = " + str(line_number))

    def __init__(self, fileNumber: int, limited: bool = False, startLine: int = 0, endLine: int = 0):
        self.__read_file__(fileNumber, limited, startLine, endLine)

    def __str__(self):
        display: str = "[Text section]"

        for instruction in self.code:
            display += '\n' + str(instruction)

        return display

    def __len__(self):
        return len(self.code)

    def replace(self, newFileNumber: int):
        self.__read_file__(newFileNumber)

    def getInstruction(self, line: int):
        return self.code[line]


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
