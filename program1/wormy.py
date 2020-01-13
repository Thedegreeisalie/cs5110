# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license
'''

Modified by Jer Moore for cs5110 program 1
01/13/2020 mm/dd/yyyy

'''

import random, pygame, sys,math
from pygame.locals import *

FPS = 5
WINDOWWIDTH = 1000
WINDOWHEIGHT = 700
CELLSIZE = 20
RADIUS = math.floor(CELLSIZE/2.5)
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
YELLOW = (255,255,0)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('ymrow')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()

# worm class
class worm:
    # Set a random self.start point.
    def __init__(self):
        self.startx = random.randint(5, CELLWIDTH - 6)
        self.starty = random.randint(5, CELLHEIGHT - 6)
        self.wormCoords = [{'x': self.startx,     'y': self.starty},
                      {'x': self.startx - 1, 'y': self.starty},
                       {'x': self.startx - 2, 'y': self.starty},
                       {'x': self.startx - 3, 'y': self.starty},
                       {'x': self.startx - 4, 'y': self.starty},
                       {'x': self.startx - 5, 'y': self.starty},
                       {'x': self.startx - 6, 'y': self.starty},
                       {'x': self.startx - 7, 'y': self.starty},
                       {'x': self.startx - 8, 'y': self.starty},
                       {'x': self.startx - 9, 'y': self.starty},
                       {'x': self.startx - 10, 'y': self.starty},
                      {'x': self.startx - 11, 'y': self.starty}]
        self.direction = RIGHT

    def update(self):
        # move the worm by adding a segment in the direction it is moving
        if self.direction == UP:
            newHead = {'x': self.wormCoords[HEAD]['x'], 'y': self.wormCoords[HEAD]['y'] - 1}
        elif self.direction == DOWN:
            newHead = {'x': self.wormCoords[HEAD]['x'], 'y': self.wormCoords[HEAD]['y'] + 1}
        elif self.direction == LEFT:
            newHead = {'x': self.wormCoords[HEAD]['x'] - 1, 'y': self.wormCoords[HEAD]['y']}
        elif self.direction == RIGHT:
            newHead = {'x': self.wormCoords[HEAD]['x'] + 1, 'y': self.wormCoords[HEAD]['y']}
        self.wormCoords.insert(0, newHead)   #have already removed the last segment

    def fire(self):
        if(len(self.wormCoords) > 2):
            del self.wormCoords[-1]  # remove wrm.s tail segment
            return True

class projectile:
    def __init__(self, direction, coord):
        self.direction = direction
        self.coords = [coord]
        if self.direction == UP:
            newHead = {'x': self.coords[HEAD]['x'], 'y': self.coords[HEAD]['y'] - 1}
        elif self.direction == DOWN:
            newHead = {'x': self.coords[HEAD]['x'], 'y': self.coords[HEAD]['y'] + 1}
        elif self.direction == LEFT:
            newHead = {'x': self.coords[HEAD]['x'] - 1, 'y': self.coords[HEAD]['y']}
        elif self.direction == RIGHT:
            newHead = {'x': self.coords[HEAD]['x'] + 1, 'y': self.coords[HEAD]['y']}
        self.coords.insert(0, newHead)   #have already removed the last segment
        del self.coords[-1]  # remove projectile's tail segment

    def update(self):
        if self.direction == UP:
            newHead = {'x': self.coords[HEAD]['x'], 'y': self.coords[HEAD]['y'] - 2}
        elif self.direction == DOWN:
            newHead = {'x': self.coords[HEAD]['x'], 'y': self.coords[HEAD]['y'] + 2}
        elif self.direction == LEFT:
            newHead = {'x': self.coords[HEAD]['x'] - 2, 'y': self.coords[HEAD]['y']}
        elif self.direction == RIGHT:
            newHead = {'x': self.coords[HEAD]['x'] + 2, 'y': self.coords[HEAD]['y']}
        self.coords.insert(0, newHead)   #have already removed the last segment
        del self.coords[-1]  # remove projectile's tail segment


def runGame():
    Worm1 = worm()
    Worm2 = worm()
    apple0 = getRandomLocation()
    apple1 = getRandomLocation()
    projectiles = []
    stones = []

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if(event.key in [K_KP2, K_KP4,  K_KP6, K_KP8]):
                    if (event.key == K_KP4) and Worm1.direction != RIGHT:
                        Worm1.direction = LEFT
                    elif (event.key == K_KP6) and Worm1.direction != LEFT:
                        Worm1.direction = RIGHT
                    elif (event.key == K_KP8) and Worm1.direction != DOWN:
                        Worm1.direction = UP
                    elif (event.key == K_KP2) and Worm1.direction != UP:
                        Worm1.direction = DOWN

                    if (event.key == K_KP4) and Worm2.direction != RIGHT:
                        Worm2.direction = LEFT
                    elif (event.key == K_KP6) and Worm2.direction != LEFT:
                        Worm2.direction = RIGHT
                    elif (event.key == K_KP8) and Worm2.direction != DOWN:
                        Worm2.direction = UP
                    elif (event.key == K_KP2) and Worm2.direction != UP:
                        Worm2.direction = DOWN
                else:
                    if (event.key == K_LEFT) and Worm1.direction != RIGHT:
                        Worm1.direction = LEFT
                    elif (event.key == K_RIGHT) and Worm1.direction != LEFT:
                        Worm1.direction = RIGHT
                    elif (event.key == K_UP) and Worm1.direction != DOWN:
                        Worm1.direction = UP
                    elif (event.key == K_DOWN) and Worm1.direction != UP:
                        Worm1.direction = DOWN
                    elif event.key == K_a and Worm2.direction != RIGHT:
                        Worm2.direction = LEFT
                    elif event.key == K_d and Worm2.direction != LEFT:
                        Worm2.direction = RIGHT
                    elif event.key == K_w and Worm2.direction != DOWN:
                        Worm2.direction = UP
                    elif event.key == K_s and Worm2.direction != UP:
                        Worm2.direction = DOWN
                    elif event.key == K_RETURN:
                        if(Worm1.fire()):
                            Bullet = projectile(Worm1.direction, Worm1.wormCoords[HEAD])
                            projectiles.append(Bullet)
                    elif event.key == K_SPACE:
                        if (Worm2.fire()):
                            Bullet = projectile(Worm2.direction, Worm2.wormCoords[HEAD])
                            projectiles.append(Bullet)
                    elif event.key == K_ESCAPE:
                        terminate()

        #update for projectiles
        for jectile in projectiles:
            # check if the projectile has hit itself or the edge
            if jectile.coords[HEAD]['x'] == -1 or jectile.coords[HEAD]['x'] == CELLWIDTH or jectile.coords[HEAD]['y'] == -1 or jectile.coords[HEAD]['y'] == CELLHEIGHT:
                projectiles.remove(jectile)
            for wrm in [Worm1, Worm2]:
                for wormCoordinate in wrm.wormCoords:
                    if jectile.coords[HEAD]['x'] == wormCoordinate['x'] and jectile.coords[HEAD]['y'] == wormCoordinate['y']:
                        projectiles.remove(jectile)
                        stones.extend(wrm.wormCoords[wrm.wormCoords.index(wormCoordinate):])
                        del wrm.wormCoords[wrm.wormCoords.index(wormCoordinate):]
            jectile.update()


        for wrm in [Worm1, Worm2]:
            # check if the worm has hit itself or the edge
            if wrm.wormCoords[HEAD]['x'] == -1 or wrm.wormCoords[HEAD]['x'] == CELLWIDTH or wrm.wormCoords[HEAD]['y'] == -1 or wrm.wormCoords[HEAD]['y'] == CELLHEIGHT:
                return  # game over
            for stone in stones:
                if stone['x'] == wrm.wormCoords[HEAD]['x'] and stone['y'] == wrm.wormCoords[HEAD]['y']:
                    return  # game over
            for wormBody in Worm2.wormCoords[1:]:
                if wormBody['x'] == wrm.wormCoords[HEAD]['x'] and wormBody['y'] == wrm.wormCoords[HEAD]['y']:
                    return  # game over
            for wormBody in Worm1.wormCoords[1:]:
                if wormBody['x'] == wrm.wormCoords[HEAD]['x'] and wormBody['y'] == wrm.wormCoords[HEAD]['y']:
                    return  # game over
            # check if worm has eaten apple0
            if (wrm.wormCoords[HEAD]['x'] == apple0['x'] and wrm.wormCoords[HEAD]['y'] == apple0['y']):
                # don't remove wrm.s tail segment
                apple0 = getRandomLocation()  # set a new apple0 somewhere
            elif (wrm.wormCoords[HEAD]['x'] == apple1['x'] and wrm.wormCoords[HEAD]['y'] == apple1['y']):
                # don't remove wrm.s tail segment
                apple1 = getRandomLocation()  # set a new apple0 somewhere
            else:
                del wrm.wormCoords[-1]  # remove wrm.s tail segment
            wrm.update()


        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(Worm1.wormCoords, YELLOW, GREEN)
        drawWorm(Worm2.wormCoords, DARKGREEN, RED)
        drawWorm(stones, DARKGRAY, WHITE)
        drawApple(apple0)
        drawApple(apple1)

        #draw projectiles
        for jectile in projectiles:
            drawApple(jectile.coords[HEAD])

        drawScore(len(Worm1.wormCoords) - 3, 120)
        drawScore(len(Worm2.wormCoords) - 3, WINDOWWIDTH/2)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, YELLOW)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Capitalism', True, YELLOW, WHITE)
    titleSurf2 = titleFont.render('Late Stage', True, DARKGRAY)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (math.floor(WINDOWWIDTH / 2), math.floor(WINDOWHEIGHT / 2))
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (math.floor(WINDOWWIDTH / 2), math.floor(WINDOWHEIGHT / 2))
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (math.floor(WINDOWWIDTH / 2), 10)
    overRect.midtop = (math.floor(WINDOWWIDTH / 2), gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score, offset):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - offset, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords, border, fill):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, border, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, fill, wormInnerSegmentRect)

def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    xcenter = coord['x'] * CELLSIZE + math.floor(CELLSIZE/2)
    ycenter = coord['y'] * CELLSIZE+ math.floor(CELLSIZE/2)
    #appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    #pygame.draw.rect(DISPLAYSURF, RED, apple0Rect)
    pygame.draw.circle(DISPLAYSURF, RED,(xcenter,ycenter),RADIUS)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()