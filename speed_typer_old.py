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
        self.typing_mode = False
        self.finished_typing = False
        self.input_text = ''
        self.FPS_CLOCK = pygame.time.Clock()
    
    def run(self):

        while True:
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.KEYDOWN:
                    if self.typing_mode:
                        if len(text_string) == len(self.input_string):
                            self.typing_mode = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                            self.typing_errors += 1
                        else:
                            # try:
                            self.input_text += event.unicode
                            # except an error
                        
                    else:
                        if event.key == pygame.K_RETURN:
                            text_string = self.reset_game()
                            statistics_string = None
                        
                        elif self.finished_typing:
                            time_score = round(time.time() - self.time_start, 1)
                            
                            correct_characters = 0
                            for index, character in enumerate(text_string):
                                if self.input_text[index] == character:
                                    correct_characters += 1
                            
                            accuracy_score = ((correct_characters / len(text_string)) * 100)

                            wpm_score = (len(text_string) * 60) / (5 * time_score)

                            statistics_string = self.results_string(time_score, accuracy_score, wpm_score)
                            reset_string = 'Reset by pressing enter'
                            
                            self.draw_text(statistics_string, 100, RESULT_COLOR)
                            self.draw_text(reset_string, 110, RESULT_COLOR)
                            
                            self.finished_typing = False
            


            self.FPS_CLOCK.tick(FRAMES_PER_SECOND)
            pygame.display.update()
    


    def reset_game(self):
        self.typing_mode = True
        self.results_string = 'Time: {} Accuracy: {} % Words per minute: {}'.format
        self.time_start = time.time()
        

        self.typing_errors = 0
        
        line_string = self.get_line()
        self.screen.blit(self.background, (0,0))
        
        # draw heading and line to type
        self.draw_text('Typing speed analyzer', HEADING_SIZE, HEADING_COLOR)
        self.draw_text(line_string, TEXT_SIZE, TEXT_COLOR)

        # Draw typing box
        box_rectangle = (50,250,650,50) # this should be based on the number of characters in the line
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

    game = Typing(screen, background_scaled)
    game.run()

if __name__ == '__main__':
    main()
