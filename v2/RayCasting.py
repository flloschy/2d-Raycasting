import re
import numpy as np
import math, pygame, time


def ray(line:tuple=((0, 0),(0, 0)), cast: tuple = ((0, 0), (0, 0))):
    x1, x2, y1, y2 = line[0][0], line[1][0], line[0][1], line[1][1]
    x3, x4, y3, y4 = cast[0][0], cast[1][0], cast[0][1], cast[1][1]
    den = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
    if den == 0:
        return False
    t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/den
    u = -((x1-x2)*(y1-y3)-(y1-y2)*(x1-x3))/den
    if 1 > t > 0 and u > 0:
        x5, y5 = x1+t*(x2-x1), y1+t*(y2-y1)
        return [x5, y5], math.sqrt((x5-x3)**2 + (y5-y3)**2)
    return False

def cast(lines:list, cast):
    points = []
    lengths = []
    for line in lines:
        ray_ = ray(line, cast)
        if ray_:
            points.append(ray_[0])
            lengths.append(ray_[1])
    try: return points[np.argmin(lengths)]
    except: return False

def cast_all(WIN, lines:list, pos:tuple=(0, 0), pov:float=360, rot:float=0, casts:int=100):
    t = math.pi*2 - abs(((pov/360)-1)*(math.pi/180)*360)
    points = []
    for angle in np.arange(0, t, t/casts):
        angle += math.pi*2 - abs(((rot/360)-1)*(math.pi/180)*360)
        x1, y1 = pos[0], pos[1]
        x2, y2 = pos[0]+1, pos[1]+1
        line = (pos,
            ((x2 - x1) * math.cos(90 - angle) - (y2 - y1) * math.sin(90 - angle) + x1,
            (x2 - x1) * math.sin(90 - angle) + (y2 - y1) * math.cos(90 - angle) + y1))
        cased_point = cast(lines, line)
        if not cased_point: continue
        points.append(cased_point)
    return points