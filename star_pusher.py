import random, sys, pygame, copy, os
from pygame.locals import *

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

BRIGHTBLUE =    (0,170,255)
WHITE =         (255,255,255)
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
    BASICFONT = pygame.font.sysfont('freesansbold', 18)

    IMAGESDICT ={ 
        'uncovered goal': pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\RedSelector.png'),
        'covered goal': pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\Selector.png'),
        'star':pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\Star.png'),
        'corner': pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\Wall Block Tall.png'),
        'wall':pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\Wood Block Tall.png'),
        'inside floor':pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\Plain Block.png'),
        'outside floor':pygame.image.load(r'C:\Users\Amundeep\Pictures\Camera Roll\Grass Block.png'),
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
            currentLevelIndex += 1
            if currentLevelIndex >= len(levels):
                currentLevelIndex = 0
        elif result == 'back':
            currentLevelIndex -=1
            if currentLevelIndex < 0:
                currentLevelIndex = len(levels) - 1
        elif result == 'reset':
            pass

def runLevel(levels, levelNum):
    global currentImage
    levelObj = levels[levelNum] # !
    mapObj = decorateMap(levelObj['mapObj'], levelObj['startState']['player'])
    gameStateObj = copy.deepcopy(levelObj['startState'])
    mapNeedsRedraw = bool(1) # call drawMap()
    levelSurf = BASICFONT.render(f'Level {levelObj['levelNum']+1} of {totalNumOfLevels}', 1, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.bottomleft = (20,WINHEI - 35)
    mapWidth = len(mapObj[0]) * TILEWIDTH
    mapHeight = (len(mapObj) - 1) * (TILEHEIGHT - TILEFLOORHEIGHT) + TILEHEIGHT
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
        
