
import pygame, math
from RayCasting import cast_all
import numpy as np

WIN = pygame.display.set_mode((900*2, 900))
pygame.display.set_caption('2d -> 3d | Raycasting')

castings = 30**2



lines = [
    ((0, 0), (900, 0)),
    ((0, 0), (0, 900)),
    ((900, 900), (900, 0)),
    ((900, 900), (0, 900)),

    ((20, 70), (40, 10)),
    ((800, 20), (500, 84)),
    ((100, 139), (282, 329))
]

pos = [900//2, 900//2]
r = 0

speed = 5
while True:
    WIN.fill((0, 0, 0))

    for line in lines:
        pygame.draw.line(WIN, (255, 0, 0), line[0], line[1], 1)

    casts = cast_all(WIN, lines, pos, pov=90, rot=r, casts=castings) + [pos]
    try: pygame.draw.polygon(WIN, (255, 255, 255), casts)
    except: pass
    pygame.draw.circle(WIN, (0, 0, 255), pos, 3)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        if pos[1]-speed >= 0:
            pos[1] -= speed
    if pressed[pygame.K_a]:
        if pos[0]-speed >= 0:
            pos[0] -= speed
    if pressed[pygame.K_s]:
        if pos[1]+speed <= 900:
            pos[1] += speed
    if pressed[pygame.K_d]:
        if pos[0]+speed <= 900:
            pos[0] += speed
    if pressed[pygame.K_q]:
        if r-1 <= 0:
            r = 360
        r -= 1
    if pressed[pygame.K_e]:
        if r+1 >= 360:
            r = 0
        r += 1


    for i, x in enumerate([x for x in np.arange(pygame.display.get_window_size()[0]/2, pygame.display.get_window_size()[0], (pygame.display.get_window_size()[0]/2)/castings)]):
        try:distance = math.sqrt((pos[0]-pos[1])**2 + (casts[i][0]-casts[i][1])**2)
        except IndexError: continue
        max_distance = pygame.display.get_window_size()[0]/2
        color = 255 - (distance / max_distance) * 255
        height = pygame.display.get_window_size()[1] - (distance / max_distance) * 300
        if color < 0: continue
        pygame.draw.line(WIN, (color, color, color), (x, height), (x, 900-height), int((pygame.display.get_window_size()[0]/2)/castings)+1)

    pygame.display.update()
