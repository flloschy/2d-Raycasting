import json
import math
import random
import time

import numpy as np
import pygame
from PIL import Image


class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class line:
    def __init__(self, x1, y1, x2, y2, ):
        self.point1 = point(x1, y1)
        self.point2 = point(x2, y2)


class RayCasting:
    def ray(self, line: object, cast: tuple = ((0, 0), (0, 0))):
        # convert values into better named values
        x1, x2, y1, y2 = line.point1.x, line.point2.x, line.point1.y, line.point2.y
        x3, x4, y3, y4 = cast[0][0], cast[1][0], cast[0][1], cast[1][1]

        # \/\/\/\/ something from wikipedia/The Coding Train --> ( https://www.youtube.com/watch?v=TOEi6T2mtHo / https://en.wikipedia.org/wiki/Line–line_intersection ) \/\/\/\/
        den = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
        if den == 0:
            return False

        t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/den
        u = -((x1-x2)*(y1-y3)-(y1-y2)*(x1-x3))/den

        if 1 > t > 0 and u > 0:
            x5, y5 = x1+t*(x2-x1), y1+t*(y2-y1)
            return [x5, y5, math.sqrt((x5-x3)**2 + (y5-y3)**2)]

        return False

    def cast(self, lines: list, angle: float, pos: tuple = (0, 0)):  # raycast every line
        line_cast = self.create_cast(pos=pos, angle=angle)

        points = []
        lenght = []
        for line in lines:
            ray = self.ray(line, line_cast)  # raycast line
            if ray:
                lenght.append(ray.pop(-1))
                points.append(ray)
        if points == []:  # list empty = draw full line
            return line_cast[1]

        p = points[np.argmin(lenght)]  # get the closest colision point
        return p[0], p[1]  # convert it into tuple

    def create_cast(self, pos: tuple = (0, 0), angle: float = 0):  # create a line with a rotation
        x1, y1 = pos[0], pos[1]
        x2, y2 = pos[0]+1, pos[1]+1

        newX = (x2 - x1) * math.cos(90 - angle) - \
            (y2 - y1) * math.sin(90 - angle) + x1
        newY = (x2 - x1) * math.sin(90 - angle) + \
            (y2 - y1) * math.cos(90 - angle) + y1

        return (pos, (newX, newY))


class Visual:
    def __init__(self):
        settings = json.load(open("./v1/settings.json"))

        self.WIDTH, self.HEIGHT = settings["window"]["width"], settings["window"]["height"]
        self.CASTS = settings["ray casts"]
        self.WIN = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT))  # create window
        self.FPS = settings["fps"]
        self.RAYCASTING = RayCasting()

        self.create_lines()
        self.cast_from = (0, 0)
        self.cast = settings["show raycasts"]

        self.save = settings["save as image"]
        if self.save:
            self.IMAGE = Image.new("RGB", (self.WIDTH, self.HEIGHT))

    def create_lines(self):
        self.lines = [
            line(
                random.randint(5, self.WIDTH-5),
                random.randint(5, self.HEIGHT-5),
                random.randint(5, self.WIDTH-5),
                random.randint(5, self.HEIGHT-5)
            ) for _ in range(0, 7)]  # place lines on map

        self.lines += [
            line(self.WIDTH-2, self.HEIGHT, self.WIDTH-2, 0),
            line(self.WIDTH, self.HEIGHT-2, 0, self.HEIGHT-2),
            line(0, 0, self.WIDTH, 0),
            line(0, 0, 0, self.HEIGHT)
        ]  # place border lines on map

    def loop(self):
        while True:
            self.WIN.fill((0, 0, 0))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    if self.save:
                        self.IMAGE.save("./map.png")
                    exit(0)
                elif e.type == pygame.MOUSEMOTION:
                    self.cast_from = pygame.mouse.get_pos()  # update mouse position
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r:
                        self.create_lines()  # recreate lines

            self.draw()  # draw raycasted map

            pygame.draw.circle(self.WIN, (255, 255, 255),
                               self.cast_from, 6)  # draw mouse

            pygame.display.update()
            time.sleep(1/self.FPS)

    def draw(self):
        raycasts = self.ray_casting()
        if not self.cast:
            # draw a filled in polygon
            pygame.draw.polygon(self.WIN, (255, 255, 255), raycasts)

    def ray_casting(self):
        casts = []
        # go 360deg around the cursor
        for angle in np.arange(0, 6.285, 6.285/self.CASTS):
            cast = self.RAYCASTING.cast(
                self.lines, angle, self.cast_from)  # raycast
            casts.append(cast)
            if self.save:
                self.IMAGE.putpixel(
                    (int(cast[0]), int(cast[1])), (255, 255, 255))
            if self.cast:
                pygame.draw.line(self.WIN, (100, 100, 100),
                                 self.cast_from, cast, 1)

        return casts  # return all raycasted points
