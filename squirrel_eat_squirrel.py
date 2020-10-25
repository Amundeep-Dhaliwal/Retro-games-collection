import random, sys, time, math, pygame
from pygame.locals import *
FPS = 30
WINWID = 640
WINHEI= 480
HALF_WINWID = int(WINWID/2)
HALF_WINHEI = int(WINHEI)

GRASSCOLOUR = (24, 255, 0)
WHITE = (255,255,255)
RED = (255,0,0)
CAMERASLACK = 90 
MOVERATE = 9
BOUNCERATE = 6
BOUNCEHEIGHT = 30
STARTSIZE = 25
WINSIZE = 300 # how big the player needs to be before winning
INVULNTIME = 2 # seconds the player is invulnerable after being hit
GAMEOVERTIME = 4 # how long the gameover screen remains on screen 
MAXHEALTH = 3

NUMGRASS = 80
NUMSQUIRRELS = 30
SQUIRRELMINSPEED = 3
SQUIRRELMAXSPEED = 7
DIRCHANGEFREQ = 2 # percentage chance of direction change per frame
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, L_SQUIR_IMG, R_SQUIR_IMG, GRASSIMAGES
    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_icon(pygame.image_load(r"C:\Users\Amundeep\Pictures\Camera Roll\gameicon.png"))
    DISPLAYSURF = pygame.display.set_mode((WINWID,WINHEI))
    pygame.display.set_caption('Squirrel Eat Squirrel')
    BASICFONT = pygame.font.SysFont('freesansbold', 32)
    
    L_SQUIR_IMG = pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\squirrel.png")
    R_SQUIR_IMG = pygame.transform.flip(L_SQUIR_IMG, True,False)
    GRASSIMAGES = []

    for i in range(1,5):
        GRASSIMAGES.append(pygame.image.load(f"C:\\Users\\Amundeep\\Pictures\\Camera Roll\\grass{i}.png"))
    
    while True:
        runGame()

def runGame():
    invulnerableMode = False
    invulnerableStartTime = 0
    gameOverMode = False
    gameOverStartTime = 0
    winMode = False

    gameOverSurf = BASICFONT.render('Game Over', True, WHITE)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.center = (HALF_WINWID, HALF_WINHEI)

    winSurf = BASICFONT.render('You have achieved Omega status!', True, WHITE)
    winRect = winSurf.get_rect()
    winRect.center = (HALF_WINWID, HALF_WINHEI)

    winSurf2 = BASICFONT.render('(Press "r" to restart.)', True, WHITE)
    winRect2 = winSurf2.get_rect()
    winRect2.center = (HALF_WINWID, HALF_WINHEI+ 30)

    cameraX = 0
    cameraY = 0

    grassObjs = []
    squirrelObjs =[]
    playerObj = {'surface':pygame.transform.scale(L_SQUIR_IMG,(STARTSIZE,STARTSIZE)),
                 'facing':LEFT,
                 'size':STARTSIZE,
                 'x':HALF_WINWID,
                 'y':HALF_WINHEI,
                 'bounce':0,
                 'health':MAXHEALTH}

    moveLeft = False
    moveRight = False
    moveUp = False
    moveDown = False

    # random grass images on the screen
    for i in range(10):
        grassObjs.append(makeNewGrass(cameraX, cameraY))
        grassObjs[i]['x'] = random.randint(0, WINWID)
        grassObjs[i]['y'] = random.randint(0, WINHEI)
    
    while True:
        if invulnerableMode and time.time() - invulnerableStartTime > INVULNTIME:
            invulnerableMode = False
        
        # move all the squirrels
        for sObj in squirrelObjs:
            sObj['x'] += sObj['moveX']
            sObj['y'] += sObj['moveY']
            sObj['bounce'] += 1
            if sObj['bounce'] > sObj['bounceRate']:
                sObj['bounce'] = 0 # reset the bounce amount
            
            # random chance they change direction
            if random.randint(0,99) < DIRCHANGEFREQ:
                sObj['moveX'] = getRandomVelocity()
                sObj['moveY'] = getRandomVelocity()
                if sObj['moveX'] > 0: # faces right 
                    sObj['surface'] = pygame.transform.scale(R_SQUIR_IMG, (sObj['width'], sObj['height']))
                else: # faces left
                    sObj['surface']  = pygame.transform.scale(L_SQUIR_IMG, (sObj['width'],sObj['height']))
            
            # go through all the objects and see if they need to be deleted
            for i in range(len(grassObjs)- 1, -1,-1):
                if isOutsideActiveArea(cameraX, cameraY, grassObjs[i]):
                    del grassObjs[i]
            for i in range(len(squirrelObjs)-1,-1, -1):
                if isOutsideActiveArea(cameraX, cameraY, squirrelObjs[i]):
                    del squirrelObjs[i]
            
            while len(grassObjs) < NUMGRASS:
                grassObjs.append(makeNewGrass(cameraX,cameraY))
            while len(squirrelObjs) < NUMSQUIRRELS:
                squirrelObjs.append(makeNewSquirrel(cameraX, cameraY))

            playerCenterX = playerObj['x'] + int(playerObj['size']/2)
            playerCenterY = playerObj['x'] + int(playerObj['size']/2)
            if (cameraX  + HALF_WINWID) - playerCenterX > CAMERASLACK:
                cameraX = playerCenterX + CAMERASLACK - HALF_WINWID
            elif playerCenterX - (cameraX + HALF_WINWID) > CAMERASLACK:
                cameraX = playerCenterX - CAMERASLACK - HALF_WINWID
            if (cameraY + HALF_WINHEI) - playerCenterY > CAMERASLACK:
                cameraY = playerCenterY + CAMERASLACK - HALF_WINHEI
            elif playerCenterY - (cameraY + HALF_WINHEI) > CAMERASLACK:
                cameraY = playerCenterY - CAMERASLACK - HALF_WINHEI
            
            # draw the green background
            DISPLAYSURF.fill(GRASSCOLOUR)

            # draw all the grass objects on the screen
            for gObj in grassObjs:
                gRect = pygame.Rect((gObj['x'] -cameraX,
                                     gObj['y']- cameraY,
                                     gObj['width'], 
                                     gObj['height']))
                DISPLAYSURF.blit(GRASSIMAGES[gObj['grassImage']], gRect)
            
            # draw the other squirrels 
            for sObj in squirrelObjs:
                sObj['rect'] = pygame.Rect( (sObj['x'] - cameraX, 
                                             sObj['y'] - cameraY - getBounceAmount(sObj['bounce'], sObj['bounceRate'], sObj['bounceHeight']),
                                             sObj['width'],
                                             sObj['height']))
                DISPLAYSURF.blit(sObj['surface'], sObj['rect'])
            
            # draw the player squirrel
            flashIsOn = round(time.time(), 1) * 10 % 2 == 1
            if not gameOverMode and not (invulnerableMode and flashIsOn):
                playerObj['rect'] = pygame.Rect((playerObj['x'] - cameraX, 
                                                 playerObj['y'] - cameraY - getBounceAmount(playerObj['bounce'], BOUNCERATE, BOUNCEHEIGHT),
                                                 playerObj['size'], 
                                                 playerObj['size']))
                DISPLAYSURF.blit(playerObj['surface'], playerObj['rect'])
            
            # draw the health meter 
            drawHealthMeter(playerObj['health'])

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()

                elif event.type == KEYDOWN:
                    if event.key in (K_UP, K_e):
                        moveUp = True
                        moveDown = False
                    elif event.key in (K_DOWN, K_d):
                        moveDown = True
                        moveUp = False
                    elif event.key in (K_LEFT, K_s):
                        moveLeft = True 
                        moveRight = False
                        if playerObj['facing'] == RIGHT:
                            playerObj['surface'] = pygame.transform.scale(L_SQUIR_IMG, (playerObj['size'], playerObj['size']))
                            playerObj['facing'] = LEFT
                    elif event.key in (K_RIGHT, K_f):
                        moveRight = True
                        moveLeft = False
                        if playerObj['facing'] == LEFT:
                            playerObj['surface'] = pygame.transform.scale(R_SQUIR_IMG, (playerObj['size'], playerObj['size']))
                            playerObj['facing'] = RIGHT
                    elif winMode and event.key == K_r:
                        return

                elif event.type == KEYUP:
                    # stop moving the player's squirrel
                    if event.key in (K_LEFT, K_s):
                        moveLeft = False
                    elif event.key in (K_RIGHT, K_f):
                        moveRight = False
                    elif event.key in (K_UP, K_e):
                        moveUp = False
                    elif event.key in (K_DOWN, K_d):
                        moveDown = False

                    elif event.key == K_ESCAPE:
                        terminate()
                
            if not gameOverMode:
                if moveLeft:
                    playerObj['x'] -= MOVERATE
                if moveRight:
                    playerObj['x'] += MOVERATE
                if moveDown:
                    playerObj['y'] += MOVERATE
                if moveUp:
                    playerObj['y'] -= MOVERATE
                
                if (moveLeft or moveRight or moveUp or moveDown) or playerObj['bounce'] != 0:
                    playerObj['bounce'] += 1
                
                if playerObj['bounce'] > BOUNCERATE:
                    playerObj['bounce'] = 0 # reset the bounce amount

                # check if the player has collided with any other squirrels
                for i in range(len(squirrelObjs)-1, -1, -1):
                    sqObj = squirrelObjs[i]
                    if 'rect' in sqObj and playerObj['rect'].colliderect(sqObj['rect']):
                        # a player an squirrel collision has occured
                        if sqObj['width'] * sqObj['height'] <= playerObj['size']**2:
                            # player is larger and eats the squirrel
                            playerObj['size'] += int((sqObj['width']*sqObj['height'])**0.2) + 1 
                            del squirrelObjs[i] 
                            
                            # reflect the new size of the player squirrel
                            if playerObj['facing'] == LEFT:
                                playerObj['surface'] = pygame.transform.scale(L_SQUIR_IMG,(playerObj['size'], playerObj['size']))
                            if playerObj['facing'] == RIGHT:
                                playerObj['surface'] = pygame.transform.scale(R_SQUIR_IMG, (playerObj['size'], playerObj['size']))

                            if playerObj['size'] > WINSIZE: 
                                winMode = True
                        
                        elif not invulnerableMode:
                            # player is smaller and takes damage
                            invulnerableMode = True
                            invulnerableStartTime = time.time()
                            playerObj['health'] -= 1
                            if playerObj['health'] == 0:
                                gameOverMode = True
                                gameOverStartTime = time.time()
                    
            else:
                # gameOverMode == True
                DISPLAYSURF.blit(gameOverSurf, gameOverRect)
                if time.time() - gameOverStartTime > GAMEOVERTIME:
                    return # end of current game
                
                # check if the player has won
            if winMode:
                DISPLAYSURF.blit(winSurf, winRect)
                DISPLAYSURF.blit(winSurf2, winRect2)
                
            pygame.display.update()
            FPSCLOCK.tick(FPS)

def drawHealthMeter(currentHealth):
    for i in range(currentHealth): 
        pygame.draw.rect(DISPLAYSURF, RED, (15,5+ (10 * MAXHEALTH) - i * 10, 20 , 10))
    for i in range(MAXHEALTH):
        pygame.draw.rect(DISPLAYSURF, WHITE, (15,5 + (10 * MAXHEALTH) - i * 10, 20, 10), 1)

def terminate():
    pygame.quit()
    sys.exit()

def getBounceAmount(currentBounce, bounceRate, bounceHeight):
    # returns the number of pixels to offset based on the bounce
    # larger the bounceRate, slower the bounce
    # currentBounce will always be less than bounceRate
    return int(math.sin((math.pi/float(bounceRate))*currentBounce)*bounceHeight)

def getRandomVelocity():
    speed = random.randint(SQUIRRELMINSPEED, SQUIRRELMAXSPEED)
    if random.randint(0,1) == 0:
        return speed
    else:
        return -speed

def getRandomOffCameraPos(cameraX, cameraY, objWidth, objHeight):
    # Rect of the camera view
    cameraRect = pygame.Rect(cameraX, cameraY, WINWID, WINHEI)
    while True:
        x = random.randint(cameraX - WINWID, cameraX + (2*WINWID))
        y = random.randint(cameraY - WINHEI, cameraY + (2*WINHEI))
        # create a Rect object with the random coordinates and use colliderect()
        # to make sure the right edge isn't in the camera view
        objRect = pygame.Rect(x,y,objWidth, objHeight)
        if not objRect.colliderect(cameraRect):
            return x, y

def makeNewSquirrel(cameraX, cameraY):
    sq = {}
    generalSize = random.randint(5, 25)
    multiplier = random.randint(1,3)
    sq['width'] = (generalSize + random.randint(0,10)) * multiplier
    sq['height'] = (generalSize + random.randint(0,10)) * multiplier
    sq['x'], sq['y'] = getRandomOffCameraPos(cameraX, cameraY, sq['width'], sq['height'])
    sq['moveX'] = getRandomVelocity()
    sq['moveY'] = getRandomVelocity()
    if sq['moveX'] < 0:
        sq['surface'] = pygame.transform.scale(L_SQUIR_IMG, (sq['width'],sq['height']))
    else:
        sq['surface'] = pygame.transform.scale(R_SQUIR_IMG, (sq['width'], sq['height']))
    sq['bounce'] = 0
    sq['bounceRate'] = random.randint(10,18)
    sq['bounceHeight'] = random.randint(10,50)
    return sq

def makeNewGrass(cameraX, cameraY):
    gr = {} 
    gr['grassImage'] = random.randint(0, len(GRASSIMAGES)- 1 )
    gr['width'] = GRASSIMAGES[0].get_width()
    gr['height'] = GRASSIMAGES[0].get_height()
    gr['x'], gr['y'] = getRandomOffCameraPos(cameraX, cameraY, gr['width'], gr['height'])
    return gr

def isOutsideActiveArea(cameraX, cameraY, obj):
    # returns False if cameraX and cameraY are more than a half window away from the edge
    boundsLeftEdge = cameraX - WINWID
    boundsTopEdge = cameraY - WINHEI
    boundsRect = pygame.Rect(boundsLeftEdge, boundsTopEdge, WINWID*3, WINHEI*3)
    objRect = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
    return not boundsRect.colliderect(objRect)

if __name__ == '__main__':
    main()