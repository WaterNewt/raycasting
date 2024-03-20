import sys
import pygame
import math
import random
from pygame.locals import *
from ray import Ray
from walls import Wall
import json

pygame.init()

config_file = "config.json"
with open(config_file, 'r') as f:
    config = json.load(f)
fps = config['fps']
fpsClock = pygame.time.Clock()

width, height = config['size']
screen = pygame.display.set_mode((width, height), DOUBLEBUF | HWSURFACE)

boundaries = []
ray_length = config['ray_length']
show = True

MAX_TRAIL_LENGTH = config['motion_blur']
trail = []


def point_dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def generate_boundaries():
    global boundaries
    border_boundary = (
        ((0, 0), (width, 0)),
        ((width, 0), (width, height)),
        ((width, height), (0, height)),
        ((0, height), (0, 0))
    )
    for i in border_boundary:
        boundaries.append(Wall(i[0], i[1]))

    for _ in range(5):
        start = (random.randint(0, 1280), random.randint(0, 720))
        end = (random.randint(0, 1280), random.randint(0, 720))
        boundaries.append(Wall(start, end))


generate_boundaries()


while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            show = not show

    trail.insert(0, pygame.mouse.get_pos())
    trail = trail[:MAX_TRAIL_LENGTH]

    for i, pos in enumerate(trail):
        alpha = int(255 * (1 - i / MAX_TRAIL_LENGTH))
        blur_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.circle(blur_surface, (255, 255, 255, alpha), pos, 30)
        screen.blit(blur_surface, (0, 0))

    if len(trail) > 1:
        pygame.draw.line(screen, (255, 255, 255), trail[0], trail[1], width=5)

    ray_start = pygame.mouse.get_pos()

    mouse_x, mouse_y = pygame.mouse.get_pos()
    for angle in range(0, 360, 11):
        angle_rad = math.radians(angle)
        dx = math.cos(angle_rad)
        dy = math.sin(angle_rad)

        ray_end = (ray_start[0] + dx * ray_length,
                   ray_start[1] + dy * ray_length)

        ray = Ray(ray_start, ray_end)
        closest = ray.cast(boundaries)

        if closest and show:
            pygame.draw.line(screen, (255, 255, 255), ray_start, closest)

    for boundary in boundaries:
        pygame.draw.line(screen, (255, 255, 255), boundary.start, boundary.end)

    pygame.display.flip()
    fpsClock.tick(fps)
