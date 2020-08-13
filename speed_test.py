import pygame, sys, time, random

class Game(object):
    def __init__(self):
        self.width = 750
        self.height = 500
        self.reset = True
        self.active = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time: 0 Accuracy: 0 % Words per minute: 0'
        self.wpm = 0
        self.end = False
        self.HEAD_C = (255,213,102)
        self.TEXT_C = (240,240,240)
        self.RESULT_C = (255,70,70)

        pygame.init()
        self.open_img  = pygame.transform.scale(pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\type-speed-open.png"), (self.width, self.height))

        self.background = pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\wood_background.png")
        self.background = pygame.transform.scale(self.background, (self.width,self.height))
        self.SCREEN = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Typing speed test')

    def drawText(self, SCREEN, msg, y, fontsize, color):
        textFont = pygame.font.SysFont('freesansbold', fontsize)
        textRender = textFont.render(msg, True, color)
        textRect = textRender.get_rect(center = (self.width/2, y))
        SCREEN.blit(textRender,textRect)
        pygame.display.update()
    
    def getSentence(self):
        file = open(r"C:\Users\Amundeep\Documents\Amundeep Singh Dhaliwal\Coding\Useful programs\Incomplete\The_Ultimate_Games_Collection\speed_phrases.txt").read()
        sentences = file.split('\n')
        return random.choice(sentences)
    
    def showResult(self, SCREEN):
        if not self.end:
            # Time
            self.total_time = time.time() - self.time_start

            # Accuracy
            count = 0
            for index, character in enumerate(self.word):
                if self.input_text[index] == character:
                    count += 1
            self.accuracy = (count/len(self.word)) * 100

            # Words per minute 
            self.wpm = len(self.input_text)*60/ (5*self.total_time)
            self.end= True
            print(self.total_time)

            self.results = 'Time: ' + str(round(self.total_time)) + ' seconds. Accuracy: '+ str(round(self.accuracy))+ '%, Words per minute: '+ str(round(self.wpm))

            self.time_img = pygame.transform.scale(pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\icon.png"), (150,150))
            SCREEN.blit(self.time_img, (self.width/2 - 75, self.height - 140))
            self.drawText(SCREEN, "Reset", self.height-70, 26,(100,100,100))

            print(self.results)
            pygame.display.update()
    
    def run(self):
        self.resetGame()
        self.running = True
        FPSCLOCK = pygame.time.Clock()
        while (self.running):
            rectangleTyping = pygame.Rect(50,250,650,50)
            self.SCREEN.fill((0,0,0), rectangleTyping)
            pygame.draw.rect(self.SCREEN, self.HEAD_C, rectangleTyping, 2)

            # Update user input
            self.drawText(self.SCREEN, self.input_text, 274, 26, (250,250,250))
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONUP:
                    xpos, ypos = event.pos
                    if rectangleTyping.collidepoint(xpos,ypos):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time()
                    elif (310<=xpos<=510 and 390 <= ypos and self.end):
                        self.resetGame()
                        xpos, ypos = pygame.mouse.get_pos()
                
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.showResult(self.SCREEN)
                            print(self.results)
                            self.drawText(self.SCREEN, self.results, 350, 28, self.RESULT_C)
                            self.end = True
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass
            FPSCLOCK.tick(60)
            pygame.display.update()
        
    def resetGame(self):
        self.SCREEN.blit(self.open_img, (0,0))

        self.reset = False
        self.end = False
        self.input_text = '' 
        self.time_start, self.total_time, self.wpm = 0,0,0

        self.word = self.getSentence()
        if not self.word:
            self.resetGame()
        # Heading 
        self.SCREEN.fill((0,0,0))
        self.SCREEN.blit(self.background, (0,0))
        msg = 'Typing speed test'
        self.drawText(self.SCREEN, msg, 80, 80, self.HEAD_C)
        # Draw a rectangle for the input box
        pygame.draw.rect(self.SCREEN,(255,192,25), (50,250,650,50),2)

        # Draw the sentence string
        self.drawText(self.SCREEN, self.word, 200, 28, self.TEXT_C)

        pygame.display.update()

Game().run()
