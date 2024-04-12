import pygame
from classes.custom_sprite import CustomSprite, Anchors
from vector.vector import Vector2
from components.rigid_body import RigidBodyComponent
from components.circle_collider import CircleCollider
import coordinate.conversions
import random
from input_handler import InputHandler


SIZE = Vector2(800, 600)
FPS = 60

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE.toarray())
pygame.display.set_caption("Pygame Utils")
sprites = pygame.sprite.Group()
colliders = []

handler = InputHandler()

player = CustomSprite(Vector2(0, 0), Vector2(40, 40), (0, 0, 100), SIZE, Anchors.CENTER_X|Anchors.CENTER_Y)
rb = player.add_component(RigidBodyComponent, 2, 0, 1, RigidBodyComponent.TYPE_CIRCLE, False)
player.add_component(CircleCollider, colliders, 20)
sprites.add(player)

for _ in range(10):
    s = CustomSprite(Vector2(random.randrange(-350, 350), random.randrange(-250, 250)), Vector2(40, 40), [0, 100, 0], SIZE)
    s.add_component(RigidBodyComponent, 2, 0, 1, RigidBodyComponent.TYPE_CIRCLE, False)
    colliders.append(s.add_component(CircleCollider, colliders, 20))
    sprites.add(s)

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        

    screen.fill((0, 0, 0))

    handler.update()
    
    player.set_cartesian_pos(player.cartesian_pos + handler.get_normalized_axis() * 8)

    for sprite in sprites:
        sprite.tick()
        pygame.draw.circle(screen, sprite.col, sprite.rect.center, sprite.rect.height//2)

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()