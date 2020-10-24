class VirtualMemory(object):

    def __init__(self, size: int = 8000000000):
        self.item:VirtualMemoryItem = []*size


class VirtualMemoryItem(object):

    def __init__(self, instantiated: bool=0, last_use: int=0, data: int=0, secondary_memory:bool=0):
        self.instantiated=instantiated
        self.last_use=last_use
        self.data=data
        self.secondary_memory=secondary_memory

