import pygame, sys, random, time

FPS = 30
width, height = 640, 480
reveal_speed = 8
boxsize = 40
gapsize = 10
boardwidth = 10
boardheight = 7
assert (boardwidth * boardheight)%2 == 0, 'Board needs to have an even number of boxes for pairs of matches'

xmargin = int((width - (boardwidth * (boxsize + gapsize))) /2)
ymargin = int((height-(boardheight * (boxsize + gapsize))) /2)

GRAY = (100,100,100)
NAVYBLUE = (60,60,100)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,128,0)
PURPLE = (255,0,255)
CYAN = (0,255,255)
colors = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)

background = NAVYBLUE
lightbgcolor = GRAY
boxcolor = WHITE
highlightcolor = BLUE

donut = 'donut'
square = 'square'
diamond = 'diamond'
lines = 'lines'
oval = 'oval'
shapes = (donut, square, diamond, lines, oval)

assert len(colors) * len(shapes) * 2 >= boardwidth * boardheight, 'Board is too big for the number of shapes/ colors defined.'

def main():
    global FPSCLOCK, screen
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    screen.fill(background)
    start_time = time.time()

    mousex = 0
    mousey = 0
    pygame.display.set_caption('Memory Game')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstselection = None

    startGameAnimation(mainBoard)

    while True:
        play_time = round(time.time() - start_time)
        mouseClicked = False
        screen.fill(background)

        drawBoard(mainBoard, revealedBoxes)
        draw_time(play_time)

        for event in pygame.event.get(): # event handling loop (contained within the game loop), iterates over 
            # a list of pygame.Event objects returned by the pygame.event.get() call
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        
        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            if not revealedBoxes[boxx][boxy]: # handles the highlighting
                drawHighlightBox(boxx, boxy)
            
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True # data structure that tracks the game state has been updated
                # prevents box being immediately covered up once revealed

                if firstselection == None:
                    firstselection = (boxx, boxy)
                else:
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstselection[0], firstselection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx,boxy)

                    if icon1shape != icon2shape or icon1color != icon2color:
                        pygame.time.wait(1000)
                        coverBoxesAnimation(mainBoard, [(firstselection[0], firstselection[1]),(boxx,boxy)])
                        revealedBoxes[firstselection[0]][firstselection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    
                    elif hasWon(revealedBoxes): # check if all matches are found
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)

                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        # show the fully unrevealed board for 1 second
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        startGameAnimation(mainBoard)
                    
                    firstselection = None # Reset the firstselection variable
        
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def generateRevealedBoxesData(boolean):
    revealedBoxes = []
    for _ in range(boardwidth):
        revealedBoxes.append([boolean]*boardheight)
    return revealedBoxes

def getRandomizedBoard():
    icons = []
    for color in colors:
        for shape in shapes:
            icons.append((shape,color))
    
    random.shuffle(icons) # shuffle the order of the icons list
    numIconUsed = int(boardwidth * boardheight / 2) # calculate how many icons are needed
    icons = icons[:numIconUsed] * 2 # multiple by two because we need two matching icons in a pair
    random.shuffle(icons) # since the first half of the list is the same as the last half shuffling is done again

    # creates a board with randomly placed icons 
    board = []
    for _ in range(boardwidth):
        column = []
        for _ in range(boardheight):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board

def splitIntoGroupsOf(groupSize, theList):
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize]) # list slicing out of bounds does not raise a index error!
    return result # 2d (multidimensional) list

def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (boxsize + gapsize) + xmargin
    top = boxy * (boxsize + gapsize) + ymargin
    return (left, top)

def getBoxAtPixel(x, y):
    for boxx in range(boardwidth):
        for boxy in range(boardheight):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, boxsize, boxsize)
            if boxRect.collidepoint(x,y):   # Rect objects have a .collidepoint(x,y) method that can be used for collision
                return (boxx, boxy)
    return (None, None)

def drawIcon(shape, color, boxx, boxy):
    quarter = int(boxsize * 0.25) # syntactic sugar
    half = int(boxsize * 0.5) # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy)

    if shape == donut:
        pygame.draw.circle(screen, color, (left + half, top + half), half -5)
        pygame.draw.circle(screen, background, (left+half, top + half), quarter -5)
    elif shape == square:
        pygame.draw.rect(screen, color, (left + quarter, top+quarter, boxsize - half, boxsize -half))
    elif shape == diamond:
        pygame.draw.polygon(screen, color, ((left+half, top), (left + boxsize -1, top+half), (left + half, top + boxsize -1), (left, top+half)))
    elif shape == lines:
        for i in range(0, boxsize, 4):
            pygame.draw.line(screen, color, (left, top +i), (left+i, top))
            pygame.draw.line(screen, color, (left + i, top + boxsize -1), (left + boxsize - 1, top + i))
    elif shape == oval:
        pygame.draw.ellipse(screen, color, (left, top + quarter, boxsize, half))

def getShapeAndColor(board, boxx, boxy):
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawBoxCovers(board, boxes, coverage): # boxes is a list of 2 item lists describing the x and y coords of a box
    # draws boxes being covered/ revealed
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(screen, background, (left, top , boxsize,boxsize))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage >0:
            pygame.draw.rect(screen, boxcolor, (left, top, coverage, boxsize))
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def revealBoxesAnimation(board, boxesToReveal):
    for coverage in range(boxsize, (-reveal_speed) -1, -reveal_speed):
        drawBoxCovers(board, boxesToReveal, coverage)

def coverBoxesAnimation(board, boxesToCover):
    for coverage in range(0,boxsize + reveal_speed, reveal_speed):
        drawBoxCovers(board, boxesToCover, coverage)

def drawBoard(board, revealed):
    # draws all of the boxes in ther covered or revealed state
    for boxx in range(boardwidth):
        for boxy in range(boardheight):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]: # draw the covered box
                pygame.draw.rect(screen, boxcolor, (left, top, boxsize,boxsize))
            else: # draw the revealed icon
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)

def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(screen, highlightcolor, (left - 5, top- 5, boxsize +10, boxsize +10), 5)

def startGameAnimation(board):
    # randomly reveal the boxes 8 at a time
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(boardwidth):
        for y in range(boardheight):
            boxes.append((x,y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(10, boxes) # all the icons are shown to the player at start 

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)
    
def gameWonAnimation(board):
    # Flash the background colour when the player has won
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = lightbgcolor
    color2 = background

    for _ in range(13):
        color1, color2 = color2, color1
        screen.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)

def hasWon(revealedBoxes):
    # returns True if all the boxes have been revealed, otherwise False
    for i in revealedBoxes:
        if False in i:
            return False
    return True

def draw_time(deltatime):
    font = pygame.font.SysFont('freesansbold', 30)
    time_stamp = font.render('Time: '+format_time(deltatime), 1 ,WHITE)
    screen.blit(time_stamp, (width - 150, height -50))

def format_time(secs):
    sec = secs%60
    minute = secs//60
    if len(str(minute)) == 1 and len(str(sec))==1:
        return '0'+ str(minute)+':0'+str(sec)
    elif len(str(minute)) == 1:
        return '0'+str(minute)+':'+str(sec)
    else:
        return ' '+str(minute)+':'+str(sec)

if __name__ == '__main__':
    main()