from Schedulers.ProcessList import ProcessList

class BlockedByIOList(ProcessList):
    """
    Simple inheiritence to fix __str__
    """
    
    def __str__(self):
        display = "[Blocked by IO]"
        for pid in self.queue:
            display += "\n" + str(pid)

        return display