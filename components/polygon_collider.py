from components.collider import Collider
from components.circle_collider import CircleCollider
from vector.vector import Vector2


class PolygonCollider(Collider):
    def __init__(self, parent, colliders_to_check, offset = Vector2(0, 0)):
        super().__init__(parent, colliders_to_check, offset)
    
    def check_colliding(self, other):
        if type(other) == PolygonCollider:
            depth = 1000000000000000000000000000000
            normal = Vector2(0, 0)
            for axis in self.parent.edge_normals:
                axis = axis.normalized
                cur_depth = self.get_new_collision_depth(other.parent.cartesian_vertices, axis)

                if cur_depth is None:
                    return
                elif cur_depth < depth:
                    depth = cur_depth
                    normal = axis
            for axis in other.parent.edge_normals:
                axis = axis.normalized
                cur_depth = self.get_new_collision_depth(other.parent.cartesian_vertices, axis)

                if cur_depth is None:
                    return
                elif cur_depth < depth:
                    depth = cur_depth
                    normal = axis
        elif type(other) == CircleCollider:
            depth = 1000000000000000000000000000000
            normal = Vector2(0, 0)
            for axis in self.parent.edge_normals:
                minA, maxA = PolygonCollider.project_vertices(self.parent.cartesian_vertices, axis)
                minB, maxB = PolygonCollider.project_circle(other.parent.radius, other.parent.cartesian_pos, axis)

                if(minA >= maxB or minB >= maxA):
                    return None
                
                cur_depth = min(maxA - minB, maxB - minA)

                if cur_depth < depth:
                    depth = cur_depth
                    normal = axis

        depth = depth * (1/normal.magnitude)

        centers = other.parent.cartesian_pos - self.parent.cartesian_pos
        if normal.dot(centers) < 0:
            normal = -normal

        return normal.normalized, depth

    def collides_with_line(self, source, direction, length):
        verts = [source, source + (direction*length)]
        normals = [*self.parent.edge_normals, Vector2(direction.y, -direction.x)]
        for axis in normals:
            depth = self.get_new_collision_depth(verts, axis)
            if depth is None:
                return False
        
        return True

    def get_new_collision_depth(self, other_verts, axis):
        minA, maxA = PolygonCollider.project_vertices(self.parent.cartesian_vertices, axis)
        minB, maxB = PolygonCollider.project_vertices(other_verts, axis)

        if(minA >= maxB or minB >= maxA):
            return None
        
        return min(maxA - minB, maxB - minA)
        
    @staticmethod
    def project_circle(radius, center, axis):
        normal = axis.normalized
        offset = normal * radius

        pointA = center + offset
        pointB = center - offset

        return PolygonCollider.project_vertices([pointA, pointB], axis)

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
