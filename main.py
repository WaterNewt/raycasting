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
try:
    with open(config_file, 'r') as f:
        config = json.load(f)
    fps = config['fps']
    width, height = config['size']
    ray_length = config['ray_length']
    MAX_TRAIL_LENGTH = config['motion_blur']
except FileNotFoundError:
    fps = 60
    width, height = 1280, 720
    ray_length = 50
    MAX_TRAIL_LENGTH = 3
fpsClock = pygame.time.Clock()
flags = HWSURFACE | DOUBLEBUF | SCALED | SRCALPHA
screen = pygame.display.set_mode((width, height), flags)
boundaries = []
show = True
trail = []

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.sysfont.SysFont("helvetica", 50)


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
    for border in border_boundary:
        boundaries.append(Wall(border[0], border[1]))

    for _ in range(5):
        start = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        boundaries.append(Wall(start, end))


generate_boundaries()

while True:
    screen.fill(BLACK)
    text = font.render("FPS: {:.2f}".format(fpsClock.get_fps()), True, WHITE)
    screen.blit(text, (10, 10))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                show = not show
            if event.key == K_q:
                pygame.quit()
                sys.exit()

    trail.insert(0, pygame.mouse.get_pos())
    trail = trail[:MAX_TRAIL_LENGTH]

    for i, pos in enumerate(trail):
        alpha = int(255 * (1 - i / MAX_TRAIL_LENGTH))
        blur_surface = pygame.Surface((width, height), SRCALPHA)
        pygame.draw.circle(blur_surface, (*WHITE, alpha), pos, 30)
        screen.blit(blur_surface, (0, 0))

    if len(trail) > 1:
        pygame.draw.line(screen, WHITE, trail[0], trail[1], width=5)

    ray_start = pygame.mouse.get_pos()

    mouse_x, mouse_y = pygame.mouse.get_pos()
    for angle in range(0, 360, 10):
        angle_rad = math.radians(angle)
        dx = math.cos(angle_rad)
        dy = math.sin(angle_rad)

        ray_end = (ray_start[0] + dx * ray_length,
                   ray_start[1] + dy * ray_length)

        ray = Ray(ray_start, ray_end)
        closest = ray.cast(boundaries)

        if closest and show:
            pygame.draw.line(screen, WHITE, ray_start, closest)

    for boundary in boundaries:
        pygame.draw.line(screen, WHITE, boundary.start, boundary.end)

    pygame.display.flip()
    if fps is not None:
        fpsClock.tick(fps)
