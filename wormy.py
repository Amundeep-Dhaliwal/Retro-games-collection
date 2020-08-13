import pygame, sys, random

WINDOWWIDTH, WINDOWHEIGHT = 640, 480
FPS = 10

CELLSIZE = 20

assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."

CELLWIDTH = int(WINDOWWIDTH/ CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT/CELLSIZE)

WHITE =    (255,255,255)
BLACK =    (0,0,0)
RED =      (255,0,0)
DARKRED =  (155,0,0)
BLUE =     (0,0,255)
YELLOW =   (255,255,0)
ORANGE =   (255,128,0)
GREEN =    (0,255,0)
DARKGREEN= (0,155,0)
DARKGRAY = (40,40,40)
PURPLE =   (127,0,255)
LIGHTGRAY =(128,128,128)
BACKGROUND = BLACK


UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0

def main():
    global FPSCLOCK, SCREEN, BASICFONT, wormColor
    wormColor = GREEN
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Wormy")
    BASICFONT = pygame.font.SysFont("FreeSansBold", 20)

    showStartScreen()
    while True: # a loop to ensure the player can play again, only way to leave is through terminate()
        lastStats = runGame()
        showGameOverScreen(lastStats)

def runGame():
    startx = random.randint(10, CELLWIDTH - 11)
    starty = random.randint(10, CELLHEIGHT - 11)
    wormCoords = [{'x': startx, 'y':starty},
                  {'x':startx -1, 'y':starty},
                  {'x':startx -2, 'y':starty}]
    
    direction = random.choice((RIGHT, UP, DOWN))

    apple = getRandomLocation()
    wormColor = GREEN
    while True:
        for event in pygame.event.get(): # event handling loop
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_a, pygame.K_LEFT) and direction != RIGHT:
                    direction = LEFT
                elif event.key in (pygame.K_d, pygame.K_RIGHT) and direction != LEFT:
                    direction = RIGHT
                elif event.key in (pygame.K_w, pygame.K_UP) and direction != DOWN:
                    direction = UP
                elif event.key in (pygame.K_s, pygame.K_DOWN) and direction != UP:
                    direction = DOWN
        
        if wormCoords[HEAD]['x'] in (0, CELLWIDTH-1) or wormCoords[HEAD]['y'] in (0, CELLHEIGHT-1):
            return (wormCoords,apple, wormColor) # Game over: Wall collision
        
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return (wormCoords,apple, wormColor)# Game Over: Self collision
        
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']: # detecting apple collision
            apple = getRandomLocation()
            wormColor = getRandomColor()
        else:
            del wormCoords[-1] # remove the worms tail segment
        
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y':wormCoords[HEAD]['y']-1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y':wormCoords[HEAD]['y'] +1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x']-1, 'y':wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x']+1, 'y':wormCoords[HEAD]['y']}
        
        wormCoords.insert(0,newHead)
        SCREEN.fill(BACKGROUND)
        drawGrid()
        drawWorm(wormCoords, wormColor)
        drawApple(apple)
        drawScore(len(wormCoords)-3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeyScreen = BASICFONT.render('Press a key to play.', 1, DARKGRAY)
    pressKeyRect = pressKeyScreen.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH- 200, WINDOWHEIGHT -30)
    SCREEN.blit(pressKeyScreen, pressKeyRect)

def checkForKeyPress():
    if len(pygame.event.get(pygame.QUIT)) > 0:
        terminate()
    keyUpEvents = pygame.event.get(pygame.KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == pygame.K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def showStartScreen():
    titleFont = pygame.font.SysFont('freesansbold', 100)
    title1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    title2 = titleFont.render('Wormy!', True, GREEN)
    
    degrees1 = 0
    degrees2 =0
    while True:
        SCREEN.fill(BACKGROUND)
        rotatedTitle1 = pygame.transform.rotate(title1, degrees1)
        rotatedRect1 = rotatedTitle1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
        SCREEN.blit(rotatedTitle1, rotatedRect1)
        
        rotatedTitle2 = pygame.transform.rotate(title2, degrees2)
        rotatedRect2 = rotatedTitle2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
        SCREEN.blit(rotatedTitle2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear any events that have been accumalated whilst the start screen was playing 
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 -= 3
        degrees2 -= 7

def terminate():
    pygame.quit()
    sys.exit()

def getRandomLocation():
    return {'x': random.randint(1,CELLWIDTH-2), 'y':random.randint(1,CELLHEIGHT-2)}

def getRandomColor():
    randomColor = random.choice((WHITE, BLUE, GREEN,YELLOW, PURPLE, ORANGE ))
    while (randomColor == wormColor):
        randomColor = random.choice((WHITE, BLUE, GREEN,YELLOW, PURPLE, ORANGE ))
    return randomColor

def showGameOverScreen(lastStats):
    wormLength, lastApple, color = lastStats
    gameOverFont = pygame.font.Font('freesansbold.ttf', 100)
    gameOverText = gameOverFont.render('Game Over',1,getRandomColor())
    checkForKeyPress() # clear out any key presses in the event queue
    degrees1 = 0
    pygame.time.wait(200)
    while True:
        SCREEN.fill(BACKGROUND)
        drawGrid()
        drawWorm(wormLength, color)
        drawApple(lastApple)
        drawScore(len(wormLength) -3)
        rotatedGameOver = pygame.transform.rotate(gameOverText, degrees1)
        rotatedRect = rotatedGameOver.get_rect()
        rotatedRect.center = (WINDOWWIDTH/2 , WINDOWHEIGHT/2)
        SCREEN.blit(rotatedGameOver, rotatedRect)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()
            return None
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 -=1

    

def drawScore(score):
    scoreText = BASICFONT.render(f'Score: {score}', True, WHITE)
    scoreRect = scoreText.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    SCREEN.blit(scoreText, scoreRect)

def drawWorm(wormCoords, color):
    for coord in wormCoords:
        x = coord['x']*CELLSIZE
        y = coord['y'] *CELLSIZE
        wormSegmentRect = pygame.Rect(x,y,CELLSIZE, CELLSIZE)
        pygame.draw.rect(SCREEN, BLACK, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x+2, y+2, CELLSIZE-8, CELLSIZE-8)
        pygame.draw.rect(SCREEN, color, wormInnerSegmentRect)

def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    outerAppleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(SCREEN, DARKRED, outerAppleRect)
    innerAppleRect = pygame.Rect(x+4, y+4, CELLSIZE-8, CELLSIZE -8)
    pygame.draw.rect(SCREEN, RED, innerAppleRect)

def drawGrid():
    for x in range(0,WINDOWWIDTH, CELLSIZE): # draw the vertical lines 
        pygame.draw.line(SCREEN, DARKGRAY, (x,0), (x,WINDOWHEIGHT))
    for y in range(0,WINDOWHEIGHT, CELLSIZE): # draw the horizontal lines 
        pygame.draw.line(SCREEN, DARKGRAY, (0, y), (WINDOWWIDTH, y))

if __name__ == "__main__":
    main()