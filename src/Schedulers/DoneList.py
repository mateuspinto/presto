from Schedulers.ProcessList import ProcessList

class DoneList(ProcessList):
    """
    Simple inheiritence to fix __str__
    """
    
    def __str__(self):
        display = "[Done list]"
        for pid in self.queue:
            display += "\n" + str(pid)

        return display