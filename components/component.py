class Component:
    COMPONENT_INDEX = 0
    TOTAL = 0

    
    def __init__(self, parent):
        self.parent = parent
        self.id = Component.TOTAL
        Component.TOTAL += 1

    def tick(self):
        ...

    def late_tick(self):
        ...