class Diagnostics(object):
    """
    A class to store valuable information for the final print
    """

    def __init__(self):
        self.contextSwitch = 0
        self.processesAdded = 0
        self.rawResponseTime = 0
        self.priorityChange = 0
        self.instructions = 0

        self.mmAllocFailed = 0
        self.mmAllocSucess = 0

        self.N = 0
        self.D = 0
        self.V = 0
        self.A = 0
        self.S = 0
        self.B = 0
        self.T = 0
        self.F = 0
        self.R = 0

    def __str__(self):
        display = "[Final Report]\n"
        display += "Context switches: " + str(self.contextSwitch) + "\n"
        display += "Processes added: " + str(self.processesAdded) + "\n"
        display += "Response time: " + str(self.rawResponseTime/self.T) + "\n"
        display += "Priority changes: " + str(self.priorityChange) + "\n"
        display += "Instructions runned: " + str(self.instructions) + "\n"
        
        display += "\n[Memory info]\n"

        if self.mmAllocSucess == 0 and self.mmAllocFailed == 0:
            display += "Memory allocation failed ratio: 100%\n"
        else:
            display += "Memory allocation failed ratio: " + str(self.mmAllocFailed / (self.mmAllocFailed + self.mmAllocSucess)*100) + "%\n"

        display += "Memory allocation sucess: " + str(self.mmAllocSucess) + "\n"
        display += "Memory allocation failed: " + str(self.mmAllocFailed) + "\n"

        display += "\n[Instructions runned]\n"
        display += "N: " + str(self.N) + "\n"
        display += "D: " + str(self.D) + "\n"
        display += "V: " + str(self.V) + "\n"
        display += "A: " + str(self.A) + "\n"
        display += "S: " + str(self.S) + "\n"
        display += "B: " + str(self.B) + "\n"
        display += "T: " + str(self.T) + "\n"
        display += "F: " + str(self.F) + "\n"
        display += "R: " + str(self.R)

        return display
