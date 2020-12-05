# All hail Al Sweigart
import pygame, sys, random, time

windowwidth, windowheight = 640, 480
boardwidth, boardheight = 4,4 # boardwidth = number of columns, boardheight = number of rows 
TILESIZE = 80
FPS = 30
TILESLIDES = 60

BLACK =         (0,0,0)
WHITE =         (255,255,255)
BRIGHTBLUE =    (0,50,255)
DARKTURQUOISE = (3,54,73)
GREEN =         (0,204,0)

background = DARKTURQUOISE
tilecolor = GREEN
textcolor = WHITE
fontsize = 40

xmargin = int((windowwidth - (TILESIZE * boardwidth + (boardwidth -1)))/2)
ymargin = int((windowheight - (TILESIZE * boardheight + (boardheight -1)))/2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK, screen, basicfont, reset_screen, reset_rect, new_screen, new_rect, solve_screen, solve_rect

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((windowwidth,windowheight))
    pygame.display.set_caption('Slide Master')
    basicfont = pygame.font.SysFont('freesansbold.ttf', fontsize)
    

    # Store the option buttons and their rectangles in options
    reset_screen, reset_rect = makeText('Reset', WHITE, GREEN, fontsize, windowheight -100) # makeText returns a pygame surface object and a pygame rect object
    new_screen, new_rect = makeText('New Game', WHITE, GREEN, fontsize, windowheight-70)
    solve_screen, solve_rect= makeText('Solve', WHITE, GREEN, fontsize, windowheight -40)

    mainBoard, solutionSeq = generateNewPuzzle(TILESLIDES,0) # 80 random slide moves performed on the ordered board
    solvedboard = getStartingBoard() # a solved board is the same as the board in a start state (ordered)
    allMoves = list() # list of moves made from the solved configuration
    start_time = time.time()
    #print(solutionSeq)
    while True:
        slideTo = None
        current_time = round(time.time() - start_time)
        msg = 'Click or press directional keys to slide'
        if mainBoard == solvedboard: # checking whether the two boards generated are the same
            msg = 'Solved!'
        
        drawBoard(mainBoard, msg)
        drawtime(current_time)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if(spotx, spoty) == (None, None):
                    # Check if the user clicked on a option button (reset/solve/new)
                    if reset_rect.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves, current_time)
                        allMoves = []
                    elif new_rect.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(80,current_time)
                        allMoves = []
                    elif solve_rect.collidepoint(event.pos):
                        if mainBoard != solvedboard:
                            resetAnimation(mainBoard, solutionSeq + allMoves, current_time) # undos all the moves made by the player (solution + player moves)
                            allMoves = []
                else:
                    # Check if the clicked tile wass adjacent to a blank spot

                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx -1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky +1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN
                    
            elif event.type == pygame.KEYUP:
                # check if the user pressed a key to slide the tile
                if event.key in (pygame.K_LEFT, pygame.K_a) and isValidMove(mainBoard, LEFT): # notice the 'in' instead of comparison
                    slideTo = LEFT
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (pygame.K_UP, pygame.K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (pygame.K_DOWN, pygame.K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN
        
        if slideTo:
            slideAnimation(mainBoard, slideTo, 'Moving',8,current_time) # Show slide on screen
            makeMove(mainBoard, slideTo) # updates the board data structure
            allMoves.append(slideTo) # the append 
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate(): # syntactic sugar
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            terminate()
        pygame.event.post(event) # put the other event objects back
        # prevents checkForQuit() consuming all the keyup events
        # pygame.event.post() can be used to add event objects to the event queue

def getStartingBoard():
    # returns a board structure with tiled in a solved state (boardheight == boardwidth == 4)
    # returns [[1,5,9,13], [2,6,10,14],[3,7,11,15], [4,8,12,None]] ?
    counter = 1
    board = [] 
    for _ in range(boardwidth):
        column = []
        for _ in range(boardheight):
            column.append(counter)
            counter += boardwidth
        board.append(column)
        counter -= boardwidth * (boardheight -1) + boardwidth - 1
    
    board[boardwidth - 1][boardheight - 1] = None
    return board

def getBlankPosition(board): # not tracking the blank position but checking where it is
    for x in range(boardwidth):
        for y in range(boardheight):
            if board[x][y] == None:
                return (x,y)

def makeMove(board, move): # directly manipulates the board
    # Does not check if a move is valid
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky+1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx -1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    
def isValidMove(board, move): # checks if there are tiles adjacent to the blank spot
    blankx, blanky = getBlankPosition(board)
    return  (move == UP and blanky != len(board[0]) -1) or \
            (move == DOWN and blanky != 0) or \
            (move == LEFT and blankx != len(board) -1) or \
            (move == RIGHT and blankx != 0)

def getRandomMove(board, lastMove = None): # prevents opposite pairs of random shuffling eg. left-right or down-up
    # Start with a full list of all four moves
    validMoves = [LEFT, RIGHT, UP, DOWN]

    # removes moves from the list if they are disqualified
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    # return a random move from the list of remaining moves
    return random.choice(validMoves)

def getLeftTopTile(tilex, tiley):
    left = xmargin + (tilex * TILESIZE) + (tilex - 1)
    top = ymargin + (tiley * TILESIZE) + (tiley - 1)
    return (left, top)

def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            left, top = getLeftTopTile(tilex, tiley)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tilex, tiley)
    return (None, None)

def drawTile(tilex, tiley, number, adjx = 0, adjy = 0):  # adjx and adjy will be useful for drawing tiles sliding
    # draw a tile at board coordinates tilex and tiley, optionally a few pixels over (determined by adjx, adjy)
    left, top = getLeftTopTile(tilex, tiley)
    pygame.draw.rect(screen, tilecolor, (left+adjx, top + adjy, TILESIZE, TILESIZE))
    textscreen = basicfont.render(str(number),1,textcolor)
    textRect = textscreen.get_rect()
    textRect.center = left + int(TILESIZE/2) + adjx, top + int(TILESIZE/2) + adjy
    screen.blit(textscreen, textRect)
    # notice how pygame.display.update() is not called, the caller of this function would draw multiple items

def makeText(text, color, bgcolor, top, left):
    # create the surface and Rect objects for some text
    textscreen = basicfont.render(text, 1, color, bgcolor)
    textRect = textscreen.get_rect()
    textRect.topleft = (top, left)
    return (textscreen, textRect)

def drawBoard(board, message):
    screen.fill(background)
    if message:
        textscreen, textRect = makeText(message, WHITE, background, 5, 5)
        screen.blit(textscreen, textRect)
    
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])
    
    left, top = getLeftTopTile(0,0) # get the left and the top coordinate of the first tile
    width = boardwidth * TILESIZE
    height = boardheight * TILESIZE
    pygame.draw.rect(screen, BRIGHTBLUE, (left - 5, top -5 , width+11, height+11 ), 4) # draws the outer boarder of the board

    screen.blit(reset_screen, reset_rect)
    screen.blit(new_screen, new_rect)
    screen.blit(solve_screen, solve_rect)
    # still not calling pygame.display.update()

def slideAnimation(board, direction, message, animationSpeed, deltatime):
    # Does not check whether a move is valid!

    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky +1
    elif direction == DOWN:
        movex = blankx
        movey = blanky -1
    elif direction == RIGHT:
        movex = blankx -1
        movey = blanky
    elif direction == LEFT:
        movex = blankx +1
        movey = blanky
    
    # Prepare the base surface
    drawBoard(board, message)
    basescreen = screen.copy()
    # draw a blank space over the moving tile on the basescreen
    moveLeft, moveTop = getLeftTopTile(movex, movey)
    pygame.draw.rect(basescreen, background, (moveLeft, moveTop, TILESIZE, TILESIZE)) # draws background on previous tile

    for i in range(0, TILESIZE, animationSpeed): # while the animation is happening, any events being created by the user are not being handled
        checkForQuit() # for this reason the program checks for any quit events
        screen.blit(basescreen, (0,0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey],0,i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)
        
        drawtime(deltatime)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def generateNewPuzzle(numSlides, deltatime):
    # from a starting configuration, make numSlides number of moves (and animate these moves)
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)
    lastMove = None
    for _ in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board,move, 'Generating new puzzle...', int(TILESIZE/3),deltatime)
        makeMove(board, move) # updates the board structure
        sequence.append(move) #appemds the random move made by the program
        lastMove = move # this variable ensures that the next random move generated does not undo the previous random move
    return (board, sequence) # list is importent for the program solving the puzzle

def resetAnimation(board, allMoves, deltatime):
    # makes all of the moves in allMoves in reverse
    revAllMoves = allMoves[:] # list slicing to make a copy of the list
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, 'Undoing all the moves', int(TILESIZE/2),deltatime)
        makeMove(board, oppositeMove)

def drawtime(deltatime):
    font = pygame.font.SysFont('freesansbold', 40)
    time_stamp = font.render('Time: '+format_time(deltatime), 1 ,WHITE)
    screen.blit(time_stamp, (windowwidth - 160, windowheight -50))

def format_time(secs):
    sec = secs%60
    minute = secs//60
    if len(str(minute)) == 1 and len(str(sec))==1:
        return '0'+ str(minute)+':0'+str(sec)
    elif len(str(minute)) == 1:
        return '0'+str(minute)+':'+str(sec)
    elif len(str(sec)) == 1:
        return str(minute)+':0'+str(sec)
    else:
        return str(minute)+':'+str(sec)

if __name__ == '__main__':
    main()