from components.collider import Collider
from vector.vector import Vector2


class PolygonCollider(Collider):
    def __init__(self, parent, colliders_to_check, offset = Vector2(0, 0)):
        super().__init__(parent, colliders_to_check, offset)
    
    def is_colliding(self, other):
        if type(other) == PolygonCollider:
            for axis in self.parent.edge_normals:
                minA, maxA = PolygonCollider.project_vertices(self.parent.cartesian_vertices, axis)
                minB, maxB = PolygonCollider.project_vertices(other.parent.cartesian_vertices, axis)

                if(minA >= maxB or minB >= maxA):
                    return None
        return True, True
            
            

    @staticmethod
    def project_vertices(verts, axis):
        min_ = 1000000000000000000000000000000
        max_ = -1000000000000000000000000000000

        for vert in verts:
            proj = vert.dot(axis)
            
            if proj < min_:
                min_ = proj
            if proj > max_:
                max_ = proj

        return min_, max_
