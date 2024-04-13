import pygame
from classes.custom_sprite import CustomSprite, Anchors
from vector.vector import Vector2
from components.rigid_body import RigidBodyComponent
from components.circle_collider import CircleCollider
from components.polygon_collider import PolygonCollider
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
rects = pygame.sprite.Group()
colliders = []

handler = InputHandler()

player = CustomSprite(Vector2(0, 0), 20, (0, 0, 100), SIZE, Anchors.CENTER_X|Anchors.CENTER_Y, CustomSprite.TYPE_CIRCLE)
rb = player.add_component(RigidBodyComponent, 2, 0, 1, RigidBodyComponent.TYPE_CIRCLE, False)
colliders.append(player.add_component(CircleCollider, colliders, 20))
sprites.add(player)

for _ in range(10):
    if random.random() > 0.5:
        s = CustomSprite.create_rectangular_sprite(Vector2(random.randrange(-350, 350), random.randrange(-250, 250)), Vector2(40, 40), [0, 100, 0], SIZE, random.randrange(0, 360))
        s.add_component(RigidBodyComponent, 2, 0, 1, RigidBodyComponent.TYPE_CIRCLE, False)
        colliders.append(s.add_component(PolygonCollider, colliders))
        sprites.add(s)
        rects.add(s)
    else:
        s = CustomSprite(Vector2(random.randrange(-350, 350), random.randrange(-250, 250)), 20, [0, 100, 0], SIZE, sprite_type=CustomSprite.TYPE_CIRCLE)
        s.add_component(RigidBodyComponent, 2, 0, 1, RigidBodyComponent.TYPE_CIRCLE, False)
        colliders.append(s.add_component(CircleCollider, colliders, 20))
        sprites.add(s)
        rects.add(s)


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
        if sprite.sprite_type == CustomSprite.TYPE_CIRCLE:
            pygame.draw.circle(screen, sprite.col, sprite.pos.toarray(), sprite.radius)
        else:
            pygame.draw.polygon(screen, sprite.col, sprite.true_vertices)

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()