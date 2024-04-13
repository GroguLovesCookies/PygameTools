import pygame
from classes.custom_sprite import CustomSprite, Anchors
from vector.vector import Vector2
from components.rigid_body import RigidBodyComponent
from components.circle_collider import CircleCollider
from components.polygon_collider import PolygonCollider
from components.destroy_offscreen import DestroyOffscreen
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
colliders = []

handler = InputHandler()

world = World()

platform = CustomSprite.create_rectangular_sprite(Vector2(0, -280), Vector2(800, 40), (0, 100, 0), SIZE)
platform.add_component(RigidBodyComponent, 2, 0.7, Vector2(800, 40), RigidBodyComponent.TYPE_BOX, True)
colliders.append(platform.add_component(PolygonCollider, colliders))
world.add_body(platform)

player = CustomSprite.create_image_sprite(Vector2(0, 0), "images/sample.png", SIZE)
player.add_component(RigidBodyComponent, 2, 0, player.shape_AABB.size, RigidBodyComponent.TYPE_BOX, False)
colliders.append(player.add_component(PolygonCollider, colliders))
world.add_body(player)

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    screen.fill((200, 200, 200))

    handler.update()

    world.tick(1/FPS)

    for sprite in world.bodies:
        sprite.draw(screen)

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()