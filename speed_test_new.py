import pygame, sys, time, random, os
from pprint import pprint

FILE_NAME = os.path.splitext(os.path.basename(__file__))[0]
ASSETS_DIRECTORY = os.path.join(os.getcwd(), 'assets', FILE_NAME)

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 500
FRAMES_PER_SECOND = 30

HEADING_SIZE = 80
TEXT_SIZE = 28

HEADING_COLOR =  (255,213,102)
BOX_OUTLINE_COLOR = (255,192,25)
TEXT_COLOR = (240,240,240)
RESULT_COLOR = (255,70,70)

class Typing:
    def __init__(self, screen, background):
        self.screen = screen
        self.background = background
        self.typing_mode = True
        self.results_string = 'Time: {} Accuracy: {} % Words per minute: {}'.format
        self.FPS_CLOCK = pygame.time.Clock()
    
    def run(self):
        self.reset_game()

        while True:


            self.FPS_CLOCK.tick(FRAMES_PER_SECOND)
            pygame.display.update()
    


    def reset_game(self):
        self.typing_mode = True
        self.results_string = 'Time: {} Accuracy: {} % Words per minute: {}'.format
        self.time_start = time.time()
        
        line_string = self.get_line()
        self.screen.blit(self.background, (0,0))
        
        # draw heading and line to type
        self.draw_text('Typing speed analyzer', HEADING_SIZE, HEADING_COLOR)
        self.draw_text(line_string, TEXT_SIZE, TEXT_COLOR)

        # Draw typing box
        box_rectangle = (50,250,650,50)
        pygame.draw.rect(self.screen,BOX_OUTLINE_COLOR, box_rectangle, width = 2)

        return line_string

    def draw_text(self, text, y_value, color, size = FONTSIZE):
        text_font = pygame.font.SysFont('freesansbold', size)
        text_render = text_font.render(text, antialias = True, color = color)
        text_rect = text_render.get_rect(center = (SCREEN_WIDTH//2, y_value))
        self.screen.blit(text_render,text_rect)

    def get_line(self):
        phrases_path = os.path.join(ASSETS_DIRECTORY, FILE_NAME + '.txt')
        lines = []
        with open(phrases_path) as phrases:
            lines = [line.strip() for line in phrases.readlines()]
    
        return random.choice(lines)
    

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image = pygame.image.load(os.path.join(ASSETS_DIRECTORY, 'black_wood.jpg'))
    background_scaled = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Speed Typing Game')

    Typing(screen, background_scaled)
