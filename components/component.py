class Component:
    COMPONENT_INDEX = 0

    
    def __init__(self, parent):
        self.parent = parent

    def tick(self):
        ...

    def late_tick(self):
        ...