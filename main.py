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
from camera import Camera
from classes.aabb import AABB


SIZE = Vector2(800, 600)
FPS = 60

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE.toarray())
pygame.display.set_caption("Pygame Utils")
colliders = []

handler = InputHandler()

world = World()
camera = Camera(Vector2(0, 0), AABB(Vector2(-1000000000000000000000000000, 0), Vector2(1000000000000000000000000, 10000)), SIZE)

platform = CustomSprite.create_rectangular_sprite(Vector2(0, -280), Vector2(800, 40), (0, 100, 0), SIZE)
platform.add_component(RigidBodyComponent, 2, 0.7, Vector2(800, 40), RigidBodyComponent.TYPE_BOX, True)
colliders.append(platform.add_component(PolygonCollider, colliders))
world.add_body(platform)

player = CustomSprite.create_image_sprite(Vector2(0, 0), "images/sample.png", SIZE, 90)
rb = player.add_component(RigidBodyComponent, 1, 0, player.shape_AABB.size, RigidBodyComponent.TYPE_BOX, False)
rb.mass = 1
rb.inv_mass = 1
colliders.append(player.add_component(PolygonCollider, colliders))
world.add_body(player)

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                rb.add_force(Vector2(0, 5))


    screen.fill((200, 200, 200))

    world.tick(1/FPS)
    handler.update()
    camera.move_to(player.pos, 10)


    rb.linear_velocity.x = 3 * handler.get_axis_x()

    for sprite in world.bodies:
        sprite.draw(screen, camera)

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()