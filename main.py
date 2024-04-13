import pygame
from classes.custom_sprite import CustomSprite, Anchors
from vector.vector import Vector2
from components.rigid_body import RigidBodyComponent
from components.circle_collider import CircleCollider
from components.polygon_collider import PolygonCollider
import coordinate.conversions
import random
from input_handler import InputHandler
from world import World


SIZE = Vector2(800, 600)
FPS = 60

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE.toarray())
pygame.display.set_caption("Pygame Utils")
sprites = pygame.sprite.Group()
rects = pygame.sprite.Group()
colliders = []

handler = InputHandler()

world = World()

platform = CustomSprite.create_rectangular_sprite(Vector2(0, -280), Vector2(800, 40), (0, 100, 0), SIZE)
platform.add_component(RigidBodyComponent, 2, 0.7, Vector2(800, 40), RigidBodyComponent.TYPE_BOX, True)
colliders.append(platform.add_component(PolygonCollider, colliders))
world.add_body(platform)
sprites.add(platform)


running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            size = random.randrange(20, 40)
            pos = coordinate.conversions.pygame_to_cartesian(*e.pos, *SIZE.toarray())
            if e.button == 1:
                s = CustomSprite.create_rectangular_sprite(Vector2(*pos), Vector2(size, size), [
                    random.randrange(0, 255),
                    random.randrange(0, 255),
                    random.randrange(0, 255)
                ],
                SIZE, 0)
                colliders.append(s.add_component(PolygonCollider, colliders))
            elif e.button == 3:
                s = CustomSprite(Vector2(*pos), size//2, [
                    random.randrange(0, 255),
                    random.randrange(0, 255),
                    random.randrange(0, 255)
                ],
                SIZE, sprite_type=CustomSprite.TYPE_CIRCLE)
                colliders.append(s.add_component(CircleCollider, colliders, size//2))
            s.add_component(RigidBodyComponent, 2, 0.7, Vector2(size, size), RigidBodyComponent.TYPE_BOX, False)
            world.add_body(s)
            sprites.add(s)
        

    screen.fill((200, 200, 200))

    handler.update()

    world.tick(1/FPS)

    for sprite in sprites:
        if sprite.sprite_type == CustomSprite.TYPE_CIRCLE:
            pygame.draw.circle(screen, sprite.col, sprite.pos.toarray(), sprite.radius)
        else:
            pygame.draw.polygon(screen, sprite.col, sprite.true_vertices())

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()