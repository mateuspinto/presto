from InterpretedLang.Instruction import Instruction

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