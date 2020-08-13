import random, pygame, sys, time

FPS = 30
WINDOWWIDTH, WINDOWHEIGHT = 640, 480
FLASHSPEED, FLASHDELAY = 500, 200 # both in milliseconds
BUTTONSIZE = 200
BUTTONGAPSIZE = 20
TIMEOUT = 4 # seconds before game over if no button pushed

WHITE =        (255,255,255)
DARKGRAY =     (40,40,40)
BLACK =        (0,0,0)
BRIGHTRED =    (255,0,0)
RED =          (155,0,0)
BRIGHTGREEN =  (0,255,0)
GREEN =        (0,155,0)
BRIGHTBLUE =   (0,0,255)
BLUE =         (0,0,155)
BRIGHTYELLOW = (255,255,0)
YELLOW =       (155,155,0)
bgColor = BLACK

XMARGIN = int((WINDOWWIDTH - (2*BUTTONSIZE) - BUTTONGAPSIZE)/2)
YMARGIN = int((WINDOWHEIGHT- (2*BUTTONSIZE)- BUTTONGAPSIZE)/2)

YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT = pygame.Rect(XMARGIN+BUTTONSIZE+BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONGAPSIZE + BUTTONSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT = pygame.Rect(XMARGIN +BUTTONGAPSIZE + BUTTONSIZE, YMARGIN+BUTTONSIZE+BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)

def main():
    global FPSCLOCK, SCREEN, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4 # moves these variables from the local scope of the main function to global scope of the program
    # good to keep global variables as constants
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Simulate')

    BASICFONT = pygame.font.SysFont('freesansbold', 20)

    infoScreen = BASICFONT.render('Match the pattern by clicking on the button or using the Q, W, A, D, 1, 2, 4 and 5 keys.', True, DARKGRAY)
    infoRect = infoScreen.get_rect()
    infoRect.topleft = (10,WINDOWHEIGHT - 25)
    
    # load the sound files
    BEEP1 = pygame.mixer.Sound(r"C:\Users\Amundeep\Music\Program sounds\beep1.ogg")
    BEEP2 = pygame.mixer.Sound(r"C:\Users\Amundeep\Music\Program sounds\beep2.ogg")
    BEEP3 = pygame.mixer.Sound(r"C:\Users\Amundeep\Music\Program sounds\beep3.ogg")
    BEEP4 = pygame.mixer.Sound(r"C:\Users\Amundeep\Music\Program sounds\beep4.ogg")

    pattern = [] # stores the pattern of colors
    currentStep = 0 # the color the player must push next
    lastClickTime = 0 # timestamp of the player's last button push
    score = 0

    waitingForInput = False # when True, waiting for player input (False when pattern is playing)

    while True:
        clickedButton = None
        SCREEN.fill(bgColor)
        drawButtons()

        scoreScreen = BASICFONT.render(f'Score: {score}', True, WHITE)
        scoreRect = scoreScreen.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 100 , 10)
        SCREEN.blit(scoreScreen, scoreRect)

        SCREEN.blit(infoScreen, infoRect)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_KP4):
                    clickedButton = YELLOW
                elif event.key in (pygame.K_w, pygame.K_KP5):
                    clickedButton = BLUE
                elif event.key in (pygame.K_a, pygame.K_KP1):
                    clickedButton = RED
                elif event.key in (pygame.K_s, pygame.K_KP2):
                    clickedButton = GREEN
        
        if not waitingForInput:
            # play the pattern
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice((RED, BLUE, GREEN, YELLOW)))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitingForInput = True
        else:
            # wait for the player to enter buttons
            if clickedButton and clickedButton == pattern[currentStep]:
                # pushed the correct button
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = time.time() # returns the number of seconds since january the 1st 1970

                if currentStep == len(pattern):
                    # pushed the last button
                    changeBackgroundAnimation()
                    score += 1
                    waitingForInput = False # let the program play a new sequence 
                    currentStep = 0 # reset back to the first step
                
            elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - TIMEOUT > lastClickTime):
                # pushed the incorrect button or has timed out
                gameOverAnimation()
                # resets the variables for a new game
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)
                changeBackgroundAnimation()
            
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(pygame.QUIT):
        terminate()
    for event in pygame.event.get(pygame.KEYUP):
        if event.key == pygame.K_ESCAPE:
            terminate()
        pygame.event.post(event) # put the other pygame.KEYUP event objects back

def flashButtonAnimation(color, animationSpeed = 50):
    if color == YELLOW:
        sound = BEEP1
        flashColor = BRIGHTYELLOW
        rectangle = YELLOWRECT
    elif color == BLUE:
        sound = BEEP2
        flashColor = BRIGHTBLUE
        rectangle = BLUERECT
    elif color == RED:
        sound = BEEP3
        flashColor = BRIGHTRED
        rectangle = REDRECT
    elif color == GREEN:
        sound = BEEP4
        flashColor = BRIGHTGREEN
        rectangle = GREENRECT
    
    origScreen = SCREEN.copy()
    flashScreen = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
    flashScreen = flashScreen.convert_alpha() # alpha refers to transparency, 255 is opaque and 0 in invisible
    r, g, b = flashColor
    sound.play()
    # color transparency - call the .convert_alpha() method on and surface objects that have transparent colors painted on them
    for start, end, step in ((0,255,1), (255,0,-1)): # animation loop that achieves the brightening effect
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            SCREEN.blit(origScreen, (0,0))
            flashScreen.fill((r,g,b, alpha))
            SCREEN.blit(flashScreen, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    
    SCREEN.blit(origScreen, (0,0))

def drawButtons():
    pygame.draw.rect(SCREEN, YELLOW, YELLOWRECT)
    pygame.draw.rect(SCREEN, BLUE, BLUERECT)
    pygame.draw.rect(SCREEN, GREEN, GREENRECT)
    pygame.draw.rect(SCREEN, RED, REDRECT)


def changeBackgroundAnimation(animationSpeed= 40):
    global bgColor
    newBgColor= (random.randint(0,255), random.randint(0,255), random.randint(0, 255))
    r,g,b = newBgColor

    newBgScreen = pygame.Surface(SCREEN.get_size())
    newBgScreen = newBgScreen.convert_alpha()

    for alpha in range(0,255, animationSpeed):
        checkForQuit()
        SCREEN.fill(bgColor)

        newBgScreen.fill((r,g,b,alpha))
        SCREEN.blit(newBgScreen, (0,0))

        drawButtons() # redraw the buttons ontop of the tint

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    
    bgColor = newBgColor

def gameOverAnimation(color = WHITE, animationSpeed = 50):
    # play all the beeps at once and flash the background screen
    origScreen = SCREEN.copy()
    flashScreen = pygame.Surface(SCREEN.get_size())
    flashScreen = flashScreen.convert_alpha()
    BEEP1.play() # roughly at the same time
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()
    r,g,b = color
    for _ in range(3):
        for start, end, step in ((0,255,1), (255,0,-1)):
            for alpha in range(start, end, animationSpeed * step):
                # alpha refers to transparency, 255 is opaque and 0 in invisible
                checkForQuit()
                flashScreen.fill((r,g,b,alpha))
                SCREEN.blit(origScreen, (0,0))
                SCREEN.blit(flashScreen, (0,0))
                drawButtons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def getButtonClicked(x,y):
    if YELLOWRECT.collidepoint((x,y)):
        return YELLOW
    elif REDRECT.collidepoint((x,y)):
        return RED
    elif GREENRECT.collidepoint((x,y)):
        return GREEN
    elif BLUERECT.collidepoint((x,y)):
        return BLUE
    return None # Explicit is better than implicit - Python koans Tim Peters //import this

if __name__ == '__main__':
    main()