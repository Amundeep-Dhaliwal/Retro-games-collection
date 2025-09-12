from random import randrange

import pygame
from pygame.locals import *

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
TILE_LENGTH = 50
HALF_TILE_LENGTH = TILE_LENGTH // 2

random_x_start = randrange(HALF_TILE_LENGTH, WINDOW_WIDTH - HALF_TILE_LENGTH, TILE_LENGTH)
random_y_start = randrange(HALF_TILE_LENGTH, WINDOW_HEIGHT - HALF_TILE_LENGTH, TILE_LENGTH)

SNAKE_LENGTH = 1

pygame.init()
pygame.display.set_caption('Snake game')
screen_surface = pygame.display.set_mode(size = (WINDOW_WIDTH, WINDOW_HEIGHT))

SNAKE_RECTANGLE = pygame.rect.Rect([0, 0, TILE_LENGTH - 2, TILE_LENGTH -2])
SNAKE_RECTANGLE.center = (random_x_start, random_y_start)
SNAKE_LIST = [SNAKE_RECTANGLE.copy()]

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        event_type = event.type
        match event_type:
            case 404:
                pass
            case QUIT:
                pygame.quit()

    pygame.display.update()
