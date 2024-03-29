# Flippy (Othello/Reversi clone)
import os
import sys 
import time
import random 
import pygame 

FILE_NAME = os.path.splitext(os.path.basename(__file__))[0]
ASSETS_DIRECTORY = os.path.join(os.getcwd(), 'assets', FILE_NAME)

FPS = 10
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
SPACE_SIZE = 50 # width and height of each space on the board, in pixels
BOARD_WIDTH = 8 
BOARD_HEIGHT = 8

 # arbitrary but unique values
WHITE_TILE = 'WHITE_TILE'
BLACK_TILE = 'BLACK_TILE'
EMPTY_SPACE = 'EMPTY_SPACE'
HINT_TILE = 'HINT_TILE'

ANIMATION_SPEED = 25 # integer from 1 to 100, higher => faster animation

X_MARGIN = int((WINDOW_WIDTH - (BOARD_WIDTH * SPACE_SIZE)) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (BOARD_HEIGHT * SPACE_SIZE)) / 2)

WHITE =         (255, 255, 255)
BLACK =         (0, 0, 0)
GREEN =         (0, 155, 0)
BRIGHT_BLUE =   (0, 50, 255)
BROWN =         (174, 94, 0)

TEXT_BG_COLOR1 = BRIGHT_BLUE
TEXT_BG_COLOR2 = GREEN
GRID_LINE_COLOR = BLACK
TEXT_COLOR = WHITE
HINT_COLOR = BROWN

def main():
    global MAIN_CLOCK, DISPLAY_SURF, FONT, BIG_FONT, BG_IMAGE
    
    pygame.init()
    MAIN_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Flippy')
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    BIG_FONT = pygame.font.Font('freesansbold.ttf', 32)

    board_path = os.path.join(ASSETS_DIRECTORY, 'flippyboard.png')
    board_image = pygame.image.load(board_path)
    board_image_transform = pygame.transform.smoothscale(board_image, (BOARD_WIDTH * SPACE_SIZE, BOARD_HEIGHT * SPACE_SIZE))
    board_image_rect = board_image_transform.get_rect() 
    board_image_rect.topleft = (X_MARGIN, Y_MARGIN)

    background_path = os.path.join(ASSETS_DIRECTORY, 'flippybackground.png')
    background_image = pygame.image.load(background_path)
    BG_IMAGE = pygame.transform.smoothscale(background_image, (BOARD_WIDTH * SPACE_SIZE, BOARD_HEIGHT * SPACE_SIZE))
    BG_IMAGE.blit(board_image_transform, board_image_rect)


if __name__ == '__main__':
    main()