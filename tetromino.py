import pygame, random, sys, time, os

FPS = 25
WINDOWWIDTH, WINDOWHEIGHT = 640, 480
BOXSIZE = 20
BOARDWIDTH, BOARDHEIGHT = 10, 20
BLANK = '.'

HORIZONTALMOTION = 0.15
VERTICALMOTION = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE)/ 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

WHITE       =   (255,255,255)
BLACK       =   (0,0,0)
RED       =     (155, 0, 0)
GREEN       =    (0, 155, 0)
BLUE       =   (0, 0, 155)
YELLOW      =   (155, 155, 0)
GRAY        =   (185, 185, 185)
LIGHTRED    =   (175, 0, 0)
LIGHTGREEN    = (20, 175, 20)
LIGHTBLUE    =  (20, 20, 175)
LIGHTYELLOW  =  (175, 175, 20)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOW = GRAY
COLORS = (BLUE, RED, GREEN, YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTRED, LIGHTGREEN, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS), 'Light colors not equal in size to colors'

TEMPLATEWIDTH, TEMPLATEHEIGHT = 5, 5

S_TEMPLATE = [['.....',
               '.....',
               '..OO.',
               '.OO..',
               '.....'],
              ['.....',
               '..O..',
               '..OO.',
               '...O.',
               '.....']]

Z_TEMPLATE = [['.....',
               '.....',
               '.OO..',
               '..OO.',
               '.....'],
              ['.....',
               '..O..',
               '.OO..',
               '.O...',
               '.....']]

I_TEMPLATE = [['..O..',
               '..O..',
               '..O..',
               '..O..',
               '.....'], 
              ['.....',
               '.....',
               'OOOO.',
               '.....',
               '.....']]

O_TEMPLATE = [['.....',
               '.....',
               '.OO..',
               '.OO..',
               '.....']]

J_TEMPLATE = [['.....',
               '.O...',
               '.OOO.',
               '.....',
               '.....'],
              ['.....',
               '..OO.',
               '..O..',
               '..O..',
               '.....'],
              ['.....',
               '.....',
               '.OOO.',
               '...O.',
               '.....'],
              ['.....',
               '..O..',
               '..O..',
               '.OO..',
               '.....']]

L_TEMPLATE = [['.....',
               '...O.',
               '.OOO.',
               '.....',
               '.....'],
              ['.....',
               '..O..',
               '..O..',
               '..OO.',
               '.....'],
              ['.....',
               '.....',
               '.OOO.',
               '.O...',
               '.....'],
              ['.....',
               '.OO..',
               '..O..',
               '..O..',
               '.....']]

T_TEMPLATE = [['.....',
               '..O..',
               '.OOO.',
               '.....',
               '.....'],
              ['.....',
               '..O..',
               '..OO.',
               '..O..',
               '.....'],
              ['.....',
               '.....',
               '.OOO.',
               '..O..',
               '.....'],
              ['.....',
               '..O..',
               '.OO..',
               '..O..',
               '.....']]

SHAPES = {'S': S_TEMPLATE,
          'Z': Z_TEMPLATE, 
          'J': J_TEMPLATE,
          'L': L_TEMPLATE,
          'I': I_TEMPLATE,
          'O': O_TEMPLATE,
          'T': T_TEMPLATE}

def main():
    global FPSCLOCK, SCREEN, BASICFONT, BIGFONT
    pygame.init()
    pygame.mixer.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    BASICFONT = pygame.font.SysFont('freesansbold', 18)
    BIGFONT = pygame.font.SysFont('freesansbold', 100)
    pygame.display.set_caption('Tetromino')

    showTextScreen('Tetromino')
    while True:
        if random.randint(0,1) == 0:
            print(os.getcwd())
            pygame.mixer.music.load(r"C:\Users\Amundeep\Music\Program sounds\tetrisb_online_converter.wav")
        else:
            pygame.mixer.music.load(r"C:\Users\Amundeep\Music\Program sounds\tetrisc_online_converter.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0)
        runGame()
        pygame.mixer.music.stop()
        showTextScreen('Game Over')

def runGame():
    # setup variables for the start of the game
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False # cannot moveup
    movingLeft = False
    movingRight = False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()

    while True: # main game loop
        if fallingPiece == None:
            # no falling piece in play, generate a new piece
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time() # reset lastFallTime

            if not isValidPosition(board, fallingPiece):
                return # game over
        
        checkForQuit()
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_p):
                    # pause the game
                    SCREEN.fill(BGCOLOR)
                    pygame.mixer.music.stop()
                    showTextScreen('Paused') # pause until key press
                    pygame.mixer.music.play(-1, 0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    movingLeft = False
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    movingRight = False
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    movingDown = False
            
            elif event.type == pygame.KEYDOWN:
                # horizontal movement
                if event.key in (pygame.K_a, pygame.K_LEFT) and isValidPosition(board, fallingPiece, adjX = -1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()
                elif event.key in (pygame.K_d, pygame.K_RIGHT) and isValidPosition(board, fallingPiece, adjX = 1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()
                
                elif event.key in (pygame.K_UP, pygame.K_w):
                    fallingPiece['rotation'] = (fallingPiece['rotation']+1) % len(SHAPES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] -1 ) % len(SHAPES[fallingPiece['shape']])
                
                elif event.key == pygame.K_q:
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(SHAPES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] +1 ) % len(SHAPES[fallingPiece['shape']])
                
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY = 1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()
                
                # move current block all the way down
                elif event.key == pygame.K_SPACE:
                    movingDown = False
                    movingRight = False
                    movingLeft = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY = i):
                            break
                    fallingPiece['y'] += i -1
        
        # handle moving the block because of the users input
        if (movingLeft or movingRight) and (time.time() -lastMoveSidewaysTime >HORIZONTALMOTION):
            if movingLeft and isValidPosition(board, fallingPiece, adjX =-1):
                fallingPiece['x'] -=1
            elif movingRight and isValidPosition(board, fallingPiece, adjX = 1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and (time.time() - lastMoveDownTime > VERTICALMOTION) and isValidPosition(board, fallingPiece, adjY = 1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()
        
        # let the piece fall if it is time to fall
        if (time.time() - lastFallTime) > fallFreq:
            # see if the piece has landed
            if not isValidPosition(board, fallingPiece, adjY =1):
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                # piece did not land and needs to be moved down
                fallingPiece['y'] += 1
                lastFallTime = time.time()
        
        SCREEN.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def terminate():
    pygame.quit()
    sys.exit()

def checkForKeyPress():
    # search for key up events
    # grab key down events and remove the from the queue
    checkForQuit()
    
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP]):
        if event.type == pygame.KEYDOWN:
            continue
        return event.key
    return None

def showTextScreen(text):
    # large text in the center until a key is pressed
    # draw the text drop shadow
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOW) 
    titleRect.center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2))
    SCREEN.blit(titleSurf, titleRect)

    # draw the text 
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center =(int(WINDOWWIDTH/2)-3, int(WINDOWHEIGHT/2)-3)
    SCREEN.blit(titleSurf, titleRect)

    # draw the additional "press key to play" text
    pressKeySurf, pressKeyRect = makeTextObjs("Press any key to play.", BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2)+100)
    SCREEN.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress == None:
        pygame.display.update()
        FPSCLOCK.tick(FPS) # what happens if we gave no arguements

def checkForQuit():
    for event in pygame.event.get(pygame.QUIT):
        terminate()
    for event in pygame.event.get(pygame.KEYUP):
        if event.key == pygame.K_ESCAPE:
            terminate()
        pygame.event.post(event) # put all the other key up events back

def calculateLevelAndFallFreq(score):
    # based on the score, return the level the player is on and
    # how many seconds have passed until a falling piece falls one space 
    level = int(score/10) +1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq

def getNewPiece():
    # returns a random piece in a random rotation and color
    shape = random.choice(list(SHAPES.keys())) # is the keys from a dictionary already a list?
    newPiece = {'shape':shape,
                'rotation':random.randint(0, len(SHAPES[shape])-1),
                'x':int(BOARDWIDTH/2)- int(TEMPLATEWIDTH/2), 
                'y':-2, 
                'color':random.randint(0, len(COLORS)-1)}
    return newPiece

def addToBoard(board, piece):
    # fill the board based on the piece's location, shape and rotation
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if SHAPES[piece['shape']][piece['rotation']][y][x] != BLANK: # BLANK is the string representation for a period
                board[x+piece['x']][y+piece['y']] = piece['color']

def getBlankBoard():
    # create and returns a new blank board data structure
    board = []
    for _ in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board

def isOnBoard(x,y):
    return (0 <= x < BOARDWIDTH) and y <BOARDHEIGHT

def isValidPosition(board, piece, adjX = 0, adjY = 0):
    # return True if the piece is within the board and not colliding
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or SHAPES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True

def isCompleteLine(board, y):
    # return true if the line is filled with boxes and there is no gaps
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False 
    return True

def removeCompleteLines(board):
    # remove any complete lines and move everything above them down
    # returns the number of complete lines
    numLinesRemoved = 0
    y = BOARDHEIGHT -1 # start y at the bottom of the board
    while y >= 0:
        if isCompleteLine(board, y):
            # remove the line and pull the boxes above down 
            for pullDownY in range(y,0 , -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY- 1]
            # set very top line to blank
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
            # note that on the next iteration of the loop y stays the same
            # ensures that if the line above is also complete, it too can be removed 
        else:
            y -= 1 # move on to check the next row up
    return numLinesRemoved

def convertToPixelCoords(boxx, boxy):
    # converts the board x y coordinates given to xy coordinates on the screen
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

def drawBox(boxx, boxy, color, pixelx = None, pixely = None):
    # draws a single tetromino box (each shape has 4 boxes) at a specified location on the board
    # or if pixelx and pixely (used for the next piece) 
    if color == BLANK:
        return
    if None in (pixelx, pixely):
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    
    pygame.draw.rect(SCREEN, COLORS[color], (pixelx +1, pixely +1, BOXSIZE-1, BOXSIZE-1))
    pygame.draw.rect(SCREEN, LIGHTCOLORS[color], (pixelx +1, pixely +1, BOXSIZE-4, BOXSIZE-4))

def drawBoard(board):
    # draw the border around the board
    pygame.draw.rect(SCREEN, BORDERCOLOR, (XMARGIN-3, TOPMARGIN-7, (BOARDWIDTH*BOXSIZE) +8, (BOARDHEIGHT*BOXSIZE)+8), 5)
    # fill the background of the board
    pygame.draw.rect(SCREEN, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE*BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    # draw individual boxes on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x,y, board[x][y])

def drawStatus(score, level):
    # draw the score text
    scoreRender = BASICFONT.render(f'Score: {score}', 1, TEXTCOLOR)
    scoreRect = scoreRender.get_rect()
    scoreRect.topleft = (WINDOWWIDTH -150,20)
    SCREEN.blit(scoreRender, scoreRect)

    # draw level text
    levelRender = BASICFONT.render(f'Level: {level}',1, TEXTCOLOR)
    levelRect = levelRender.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 50)
    SCREEN.blit(levelRender, levelRect)

def drawPiece(piece, pixelx= None, pixely=None):
    shapeToDraw = SHAPES[piece['shape']][piece['rotation']]
    if None in (pixelx,pixely):
        # use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])
    
    # draw each of the blocks to make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None,piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

def drawNextPiece(piece):
    # draw the next text
    nextRender = BASICFONT.render('Next:', 1 , TEXTCOLOR)
    nextRect = nextRender.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    SCREEN.blit(nextRender, nextRect)

    # draw the next piece
    drawPiece(piece, pixelx = WINDOWWIDTH -120, pixely = 100)

if __name__ == '__main__':
    main()