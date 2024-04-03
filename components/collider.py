from components.component import Component


class Collider(Component):
    COMPONENT_INDEX = 1

    def __init__(self, parent, colliders_to_check):
        super().__init__(parent)
        self.colliders = colliders_to_check
        self.center = self.parent.cartesian_pos
        self.parent.pos_changed.append(self.on_parent_pos_change)
    
    def on_parent_pos_change(self):
        self.center = self.parent.cartesian_pos


    def is_colliding(self, other) -> bool:
        return True

    def check_all_collisions(self) -> bool:
        for collider in self.colliders:
            if self.is_colliding(collider):
                return True

        return False

    def late_tick(self):
        ...