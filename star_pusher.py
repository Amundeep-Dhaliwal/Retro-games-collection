import random, sys, pygame, copy, os
from pygame.locals import *

# A Sokoban clone

FPS = 30
WINWID = 800
WINHEI = 600
HALF_WINWID = int(WINWID/2)
HALF_WINHEI = int(WINHEI/2)

TILEWID = 50
TILEHEI = 85
TILEFLOORHEI = 45

CAM_MOVE_SPEED = 5

OUTSIDE_DECORATION_PCT = 20

BRIGHTBLUE = (0,170,255)
WHITE =      (255,255,255)

BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK, DISPLAYSURF, IMAGESDICT, TILEMAPPING, OUTSIDEDECOMAPPING, BASICFONT, PLAYERIMAGES, currentImage

    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((WINWID,WINHEI))

    pygame.display.set_caption('Star Pusher')
    BASICFONT = pygame.font.SysFont('freesansbold', 34)

    IMAGESDICT ={ 
        'uncovered goal': pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\RedSelector.png'),
        'covered goal': pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\Selector.png'),
        'star':pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\Star.png'),
        'corner': pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\Wall_Block_Tall.png'),
        'wall':pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\Wood_Block_Tall.png'),
        'inside floor':pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\Plain_Block.png'),
        'outside floor':pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\Grass_Block.png'),
        'title':pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\star_title.png'),
        'solved':pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\star_solved.png'),
        'princess':pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\princess.png'),
        'boy':pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\boy.png'),
        'catgirl':pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\catgirl.png'),
        'horngirl':pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\horngirl.png'),
        'pinkgirl':pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\pinkgirl.png'),
        'rock':pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\Rock.png'),
        'short tree':pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\Tree_Short.png'),
        'tall tree':pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\Tree_Tall.png'),
        'ugly tree':pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\Tree_Ugly.png'),
    }

    TILEMAPPING = {
        'x':IMAGESDICT['corner'],
        '#':IMAGESDICT['wall'],
        'o':IMAGESDICT['inside floor'],
        ' ':IMAGESDICT['outside floor'],
    }

    OUTSIDEDECOMAPPING = {
        '1': IMAGESDICT['rock'],
        '2': IMAGESDICT['short tree'],
        '3': IMAGESDICT['tall tree'], 
        '4': IMAGESDICT['ugly tree'],
    }

    currentImage = 0
    PLAYERIMAGES = [
        IMAGESDICT['princess'],
        IMAGESDICT['boy'],
        IMAGESDICT['catgirl'],
        IMAGESDICT['horngirl'],
        IMAGESDICT['pinkgirl'],
    ]

    startScreen()

    levels = readLevelsFile('starPusherLevels.txt')
    currentLevelIndex = 0
    
    while True:
        result = runLevel(levels, currentLevelIndex)
        if result in ('solved', 'next'):
            #print('incrementing')
            currentLevelIndex = (currentLevelIndex + 1) % len(levels)
        elif result == 'back':
            currentLevelIndex = (currentLevelIndex -1) % len(levels)
        elif result == 'reset':
            pass

def runLevel(levels, levelNum):
    global currentImage
    levelObj = levels[levelNum] # !
    mapObj = decorateMap(levelObj['mapObj'], levelObj['startState']['player'])
    gameStateObj = copy.deepcopy(levelObj['startState']) # a deep copy is required for the player to make changes
    
    mapNeedsRedraw = bool(1) # call drawMap()
    totalNumOfLevels = len(levels)
    levelSurf = BASICFONT.render(f'Level {levelNum + 1} of {totalNumOfLevels}', 1, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.bottomleft = (20,WINHEI - 35)

    mapWidth = len(mapObj) * TILEWID
    mapHeight = (len(mapObj[0]) - 1) * (TILEHEI - TILEFLOORHEI) + TILEHEI

    MAX_CAM_X_PAN = abs(HALF_WINHEI - int(mapHeight/2)) + TILEWID
    MAX_CAM_Y_PAN = abs(HALF_WINWID - int(mapWidth/2)) + TILEHEI

    levelIsComplete = False

    cameraOffsetX = 0
    cameraOffsetY = 0

    cameraUp = False 
    cameraDown = False
    cameraRight = False
    cameraLeft = False 

    while True:
        playerMoveTo = None
        keyPressed = bool(0)
        
        for event in pygame.event.get(): 
            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                keyPressed = bool(1)
                if event.key ==  K_s:
                    playerMoveTo = LEFT
                elif event.key == K_f:
                    playerMoveTo = RIGHT
                elif event.key ==  K_e:
                    playerMoveTo = UP
                elif event.key == K_d:
                    playerMoveTo = DOWN
                
                elif event.key == K_RIGHT:
                    cameraRight = bool(1)
                elif event.key == K_LEFT:
                    cameraLeft = bool(1)
                elif event.key == K_UP:
                    cameraUp = bool(1)
                elif event.key == K_DOWN:
                    cameraDown = bool(1)
            
                elif event.key == K_n:
                    return 'next'
                elif event.key == K_b:
                    return 'back'

                elif event.key == K_SPACE and not levelIsComplete:
                    return 'reset'
                elif event.key == K_p:
                    currentImage = (currentImage + 1) % len(PLAYERIMAGES)
                    mapNeedsRedraw = bool(1)
            
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_LEFT:
                    cameraLeft = bool(0)
                elif event.key == K_DOWN:
                    cameraDown = bool(0)
                elif event.key == K_UP:
                    cameraUp = bool(0)
                elif event.key == K_RIGHT:
                    cameraRight = bool(0)

        if playerMoveTo != None and not levelIsComplete:
            moved = makeMove(mapObj, gameStateObj, playerMoveTo)
            if moved:
                gameStateObj['stepCounter'] += 1
                mapNeedsRedraw = bool(1)
            
            if isLevelFinished(levelObj, gameStateObj):
                levelIsComplete = bool(1)
                keyPressed = bool(0)
        
        DISPLAYSURF.fill(BGCOLOR)

        if mapNeedsRedraw:
            mapSurf = drawMap(mapObj, gameStateObj, levelObj['goals'])
            mapNeedsRedraw = bool(0)
        
        if cameraUp and cameraOffsetY < MAX_CAM_X_PAN:
            cameraOffsetY += CAM_MOVE_SPEED
        elif cameraDown and cameraOffsetY > -MAX_CAM_X_PAN:
            cameraOffsetY -= CAM_MOVE_SPEED
        
        if cameraLeft and cameraOffsetX < MAX_CAM_Y_PAN:
            cameraOffsetX += CAM_MOVE_SPEED
        elif cameraRight and cameraOffsetX > -MAX_CAM_Y_PAN:
            cameraOffsetX -= CAM_MOVE_SPEED
        
        mapSurfRect = mapSurf.get_rect()
        mapSurfRect.center = (HALF_WINWID + cameraOffsetX, HALF_WINHEI + cameraOffsetY)

        DISPLAYSURF.blit(mapSurf, mapSurfRect)

        DISPLAYSURF.blit(levelSurf, levelRect)
        stepSurf = BASICFONT.render(f'Steps: {gameStateObj["stepCounter"]}', True, TEXTCOLOR)
        stepRect = stepSurf.get_rect()
        stepRect.bottomleft = (20, WINHEI - 10)
        DISPLAYSURF.blit(stepSurf, stepRect)

        if levelIsComplete:
            solvedRect = IMAGESDICT['solved'].get_rect()
            solvedRect.center = (HALF_WINWID, HALF_WINHEI)
            DISPLAYSURF.blit(IMAGESDICT['solved'], solvedRect)

            if keyPressed:
                return 'solved'

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isWall(mapObj, x, y):
    if x < 0 or x >= len(mapObj) or y < 0 or y >= len(mapObj[x]):
    #if (0 < x <= len(mapObj)) or (0 < y <= len(mapObj[x])):
        return False # x and y are not on the map
    elif mapObj[x][y] in ('#', 'x'):
        return True
    return False

def decorateMap(mapObj, startxy):
    # walls that are corners are turned into corner pieces
    # outside/inside tile distinction is made
    # random tree/rock decorations are placed on the outside tiles
    startx, starty = startxy
    
    mapObjCopy = copy.deepcopy(mapObj)
    # Remove all the non-wall characters
    for x in range(len(mapObjCopy)):
        for y in range(len(mapObjCopy[0])):
            if mapObjCopy[x][y] in ('$', '.', '@', '+', '*'):
                mapObjCopy[x][y] = ' '
    
    # flood fill to determine the inside/outside floor tiles
    floodFill(mapObjCopy, startx, starty, ' ', 'o')

    # convert the adjoined walls into corner tiles
    for x in range(len(mapObjCopy)):
        for y in range(len(mapObjCopy[0])):

            if mapObjCopy[x][y] == '#':
                if (isWall(mapObjCopy, x, y-1) and isWall(mapObjCopy, x + 1, y)) or \
                   (isWall(mapObjCopy, x+1, y) and isWall(mapObjCopy, x, y+1)) or \
                   (isWall(mapObjCopy, x, y-1) and isWall(mapObjCopy, x - 1, y)) or \
                   (isWall(mapObjCopy, x-1, y) and isWall(mapObjCopy, x , y+1)):
                   # |_ F _| ¬ 
                   mapObjCopy[x][y] = 'x'
            elif mapObjCopy[x][y] == ' ' and random.randint(0, 99) < OUTSIDE_DECORATION_PCT:
                mapObjCopy[x][y] = random.choice(list(OUTSIDEDECOMAPPING.keys()))
    return mapObjCopy

def isBlocked(mapObj, gameStateObj, x, y):
    if isWall(mapObj, x,y):
        return True
    elif x < 0 or x >= len(mapObj) or y < 0 or y >= len(mapObj[x]):
        return True # x and y are not on the map
    elif (x, y) in gameStateObj['stars']: # if the route is blocked by a star 
        return True
    return False
                
def makeMove(mapObj, gameStateObj, playerMoveTo):
    playerx, playery = gameStateObj['player']
    stars = gameStateObj['stars']
    #print(type(stars))
    if playerMoveTo == UP:
        xOffset = 0
        yOffset = -1
    elif playerMoveTo == RIGHT:
        xOffset = 1
        yOffset = 0
    elif playerMoveTo == LEFT:
        xOffset = -1
        yOffset = 0
    elif playerMoveTo == DOWN:
        xOffset = 0
        yOffset = 1
    
    if isWall(mapObj, playerx + xOffset , playery + yOffset): # no move into a wall
        return False
    else:
        if (playerx + xOffset,playery+yOffset) in stars:
            if not isBlocked(mapObj, gameStateObj, playerx + (xOffset*2), playery + (yOffset*2)):
                # move the star
                ind = stars.index((playerx + xOffset, playery + yOffset))
                stars[ind] = (stars[ind][0] + xOffset, stars[ind][1] + yOffset)
            else:
                return False
        gameStateObj['player'] = (playerx + xOffset, playery + yOffset)
        return True

def startScreen():
    titleRect = IMAGESDICT['title'].get_rect()
    topCoord = 50
    titleRect.top = topCoord
    titleRect.centerx = HALF_WINWID
    topCoord += titleRect.height

    instructionText = ['Push the stars over the marks.', 
                       'ESDF to move, arrow keys for camera control, P to change character.',
                       'Space to reset level, Esc to quit.',
                       'N for next level, B for the previous level.' 
                        ]

    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(IMAGESDICT['title'], titleRect)
    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        topCoord += 10
        instRect.top = topCoord
        instRect.centerx = HALF_WINWID
        topCoord += instRect.height
        DISPLAYSURF.blit(instSurf, instRect)
    
    while True: 
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            else:
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        terminate()
                    return
    
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def readLevelsFile(filename):
    assert os.path.exists(filename), f'Cannot find the {filename} file'
    
    with open(filename, 'r') as mapFile: # open defaults to read mode
        content = mapFile.readlines() + [os.linesep] # Each level must end with a blank line
    
    levels = []
    levelNum = 0
    mapTextLines = []
    mapObj = []
    for lineNum in range(len(content)):
        line = content[lineNum].rstrip('\r\n')
        if ';' in line:
            line = line[:line.find(';')]
        if line != '':
            # this line is part of the map
            mapTextLines.append(line)
        elif line == '' and len(mapTextLines) > 0:
            
            maxWidth = -1
            for i in range(len(mapTextLines)): # find the longest row in the map
                if len(mapTextLines[i]) > maxWidth:
                    maxWidth = len(mapTextLines[i])

            for i in range(len(mapTextLines)): # add spaces to the ends of the shorter rows to ensure the map is rectangular
                mapTextLines[i] += ' ' * (maxWidth - len(mapTextLines[i]))

            # convert mapTextLines to a map object 
            for x in range(len(mapTextLines[0])): 
                mapObj.append([])
            for y in range(len(mapTextLines)):
                for x in range(maxWidth):
                    mapObj[x].append(mapTextLines[y][x])
            
            startx = None
            starty = None
            goals = []
            stars = []
            for x in range(maxWidth):
                for y in range(len(mapObj[x])):
                    if mapObj[x][y] in ('@','+'):
                        # @ is the player and + is the player & goal
                        startx = x
                        starty = y
                    if mapObj[x][y] in ('.', '+', '*'):
                        # . is goal and * is star & goal
                        goals.append((x, y))
                    if mapObj[x][y] in ('$', '*'):
                        # $ is star
                        stars.append((x,y))
            assert startx != None and starty != None, f'Level {levelNum + 1} (around line {lineNum}) in {filename} is missing a "@" or "+" to mark the start point.'
            assert len(goals) > 0, f'Level {levelNum + 1} (around line {lineNum}) in {filename} must have at least one goal.'
            assert len(stars) >= len(goals), f'Level {levelNum + 1} (around line {lineNum}) in {filename} has {len(goals)} goals but only {len(stars)} stars.'

            gameStateObj = {'player':(startx, starty),
                            'stepCounter':0, 
                            'stars':stars}
            levelObj = {'width':maxWidth, 
                        'height':len(mapObj), 
                        'mapObj':mapObj, 
                        'goals':goals,
                        'startState':gameStateObj}
            
            levels.append(levelObj)

            mapTextLines = []
            mapObj = []
            gameStateObj = {}
            levelNum += 1
    return levels

def floodFill(mapObj, x, y, oldCharacter, newCharacter):
    if mapObj[x][y] == oldCharacter:
        mapObj[x][y] = newCharacter
    
    if x < len(mapObj) - 1 and mapObj[x+1][y] == oldCharacter:
        floodFill(mapObj, x+ 1, y, oldCharacter, newCharacter) # call right
    if x > 0 and mapObj[x-1][y] == oldCharacter:
        floodFill(mapObj, x - 1, y, oldCharacter, newCharacter) # call left
    if y < len(mapObj[x]) - 1 and mapObj[x][y + 1] == oldCharacter:
        floodFill(mapObj, x, y + 1, oldCharacter, newCharacter) # call down 
    if y > 0 and mapObj[x][y - 1] == oldCharacter:
        floodFill(mapObj, x, y - 1, oldCharacter, newCharacter) # call up

def drawMap(mapObj, gameStateObj, goals):
    mapSurfWidth = len(mapObj)*TILEWID
    mapSurfHeight = (len(mapObj[0]) - 1) * (TILEHEI - TILEFLOORHEI) + TILEHEI
    mapSurf = pygame.Surface((mapSurfWidth, mapSurfHeight))
    mapSurf.fill(BGCOLOR)

    for x in range(len(mapObj)):
        for y in range(len(mapObj[x])):
            spaceRect = pygame.Rect((x * TILEWID, y * (TILEHEI - TILEFLOORHEI), TILEWID, TILEHEI))
            if mapObj[x][y] in TILEMAPPING:
                baseTile = TILEMAPPING[mapObj[x][y]]
            elif mapObj[x][y] in OUTSIDEDECOMAPPING:
                baseTile = TILEMAPPING[' ']

            mapSurf.blit(baseTile, spaceRect)

            if mapObj[x][y] in OUTSIDEDECOMAPPING:
                mapSurf.blit(OUTSIDEDECOMAPPING[mapObj[x][y]], spaceRect)                
            elif (x,y) in gameStateObj['stars']:
                if (x, y) in goals:
                    mapSurf.blit(IMAGESDICT['covered goal'], spaceRect)
                mapSurf.blit(IMAGESDICT['star'], spaceRect)
            elif (x, y) in goals:
                mapSurf.blit(IMAGESDICT['uncovered goal'], spaceRect)
            if (x, y) == gameStateObj['player']:
                mapSurf.blit(PLAYERIMAGES[currentImage], spaceRect)

    return mapSurf

def isLevelFinished(levelObj, gameStateObj):
    for goal in levelObj['goals']:
        if goal not in gameStateObj['stars']:
            return False
    return True

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()


