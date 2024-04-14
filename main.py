import pygame
from classes.custom_sprite import CustomSprite, Anchors
from vector.vector import Vector2
from components.rigid_body import RigidBodyComponent
from components.circle_collider import CircleCollider
from components.polygon_collider import PolygonCollider
from components.destroy_offscreen import DestroyOffscreen
from components.character_controller import CharacterController
from components.animator import Animator
import coordinate.conversions
import random
from input_handler import InputHandler
from world import World
from camera import Camera, Background
from classes.aabb import AABB
from image import Spritesheet, image_from_file


SIZE = Vector2(800, 600)
FPS = 60

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE.toarray())
pygame.display.set_caption("Pygame Utils")
colliders = []

handler = InputHandler()

world = World()

backgrounds = [
    Background("images/background1.png", 50, SIZE.toarray()),
    Background("images/background3.png", 15),
    Background("images/background2.png", 5, (SIZE/3).toarray()),
]
camera = Camera(Vector2(0, 0), AABB(Vector2(-1000000000000000000000000000, 0), Vector2(1000000000000000000000000, 10000)), SIZE, 
            backgrounds)

platform = CustomSprite.create_rectangular_sprite(Vector2(0, -280), Vector2(20000, 40), (0, 100, 0), SIZE)
platform.add_component(RigidBodyComponent, 2, 0.7, Vector2(800, 40), RigidBodyComponent.TYPE_BOX, True)
colliders.append(platform.add_component(PolygonCollider, colliders))
world.add_body(platform)

player_sheet = Spritesheet.sheet_from_json_file("images/sheets/samplesheet_data.json")

player = CustomSprite.create_image_sprite(Vector2(0, 0), "idle", SIZE, sheet=player_sheet)
anim = player.add_component(Animator.from_json, "images/animators/player_animator.json")
rb = player.add_component(RigidBodyComponent, 1, 0, player.shape_AABB.size, RigidBodyComponent.TYPE_BOX, False)
rb.mass = 1
rb.inv_mass = 1
colliders.append(player.add_component(PolygonCollider, colliders))
player.add_component(CharacterController, 3, 7, 2)
world.add_body(player)

running = True
frame = 0
while running:
    handler.update()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        else:
            handler.register_key_event(e)

    screen.fill((0, 0, 100))
    camera.draw_backgrounds(screen)

    world.tick(1/FPS)
    camera.move_to(player.pos, 10)


    for sprite in world.bodies:
        sprite.draw(screen, camera)

    pygame.display.update()

    clock.tick(FPS)
    frame += 1

pygame.quit()