# Snake Game
# By Mateusz Grochala
# github.com/Mat-Gr/snake

import random, pygame, sys
from pygame.locals import *

WINWIDTH = 640
WINHEIGHT = 480
PIXSIZE = 10

#            R    G    B
GRAY     = (45, 45, 45)
WHITE    = (255, 255, 255)

BGCOLOR = GRAY

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('Snake')

    cords = [WINWIDTH/2, WINHEIGHT/2]
    prevPos = (cords[0], cords[1])
    snakeBody = [prevPos]
    direction = 'up'

    foodX = 0
    foodY = 0
    food = False

    FPS = 15

    while True:
        scoreFontObj = pygame.font.Font('freesansbold.ttf', 16)
        scoreTextSurfaceObj = scoreFontObj.render(score(snakeBody), True, WHITE)
        scoreTextRectObj = scoreTextSurfaceObj.get_rect()
        scoreTextRectObj.topleft = (10, 10)

        GOfontObj = pygame.font.Font('freesansbold.ttf', 35)
        GOtextSurfaceObj = GOfontObj.render('GAME OVER', True, WHITE)
        GOtextRectObj = GOtextSurfaceObj.get_rect()
        GOtextRectObj.center = (WINWIDTH/2, WINHEIGHT/2)

        DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(scoreTextSurfaceObj, scoreTextRectObj)

        # food
        if food == False:
            food_cords = generateFoodCords()
            foodX = food_cords[0]
            foodY = food_cords[1]
            food = True

        elif cords[0] == foodX and cords[1] == foodY:
            food = False
            snakeBody = eat(prevPos, snakeBody)
            FPS += 0.5

        # movement
        if direction == 'up':
            prevPos = (cords[0], cords[1])
            cords[1] -= PIXSIZE
            if cords[1] < 0:
                cords[1] = WINHEIGHT-PIXSIZE

        elif direction == 'right':
            prevPos = (cords[0], cords[1])
            cords[0] += PIXSIZE
            if cords[0] > WINWIDTH-PIXSIZE:
                cords[0] = 0

        elif direction == 'down':
            prevPos = (cords[0], cords[1])
            cords[1] += PIXSIZE
            if cords[1] > WINHEIGHT-PIXSIZE:
                cords[1] = 0

        elif direction == 'left':
            prevPos = (cords[0], cords[1])
            cords[0] -= PIXSIZE
            if cords[0] < 0:
                cords[0] = WINWIDTH-PIXSIZE

        # death
        if (cords[0], cords[1]) in snakeBody:
            DISPLAYSURF.blit(GOtextSurfaceObj, GOtextRectObj)
            pygame.display.update()
            pygame.time.wait(2000)
            snakeBody = [prevPos]
            FPS = 15

        # draw snake
        snakeBody = updateSnake(prevPos, snakeBody)
        drawSnake(cords, snakeBody)

        # draw food
        pygame.draw.rect(DISPLAYSURF, WHITE, (foodX, foodY, PIXSIZE, PIXSIZE), 1)

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # change direction
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    direction = 'up'
                elif event.key == K_RIGHT:
                    direction = 'right'
                elif event.key == K_DOWN:
                    direction = 'down'
                elif event.key == K_LEFT:
                    direction = 'left'

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def score(snakeBody):
    return 'Score: ' + str(len(snakeBody)-1)

def generateFoodCords():
    foodX = random.randrange(0, WINWIDTH, PIXSIZE)
    foodY = random.randrange(0, WINHEIGHT, PIXSIZE)
    return [foodX, foodY]

def updateSnake(prevPos, snakeBody):
    snakeBody.pop()
    snakeBody.insert(0, prevPos)
    return snakeBody

def eat(prevPos, snakeBody):
    snakeBody.insert(0, prevPos)
    return snakeBody

def drawSnake(cords, snakeBody):
    snakeHead = Rect(cords[0], cords[1], PIXSIZE, PIXSIZE)
    pygame.draw.rect(DISPLAYSURF, WHITE, snakeHead)
    for val in snakeBody:
            pygame.draw.rect(DISPLAYSURF, WHITE, (val, (PIXSIZE, PIXSIZE)))

if __name__ == '__main__':
    main()
