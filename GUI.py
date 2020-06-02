import pygame

from engine import *

# intialise pygame
pygame.init()
pygame.display.init()
pygame.display.list_modes()
# create the screen
dimX = 400
dimY = 450
screen = pygame.display.set_mode((dimX, dimY))
GAMEOVER = False
gameBegin = False
textX = 10
textY = 10
# creating the title and icon
pygame.display.set_caption("2048 Game")

def displayScore(score):
    x = 150
    y = 15
    font = pygame.font.SysFont("consolas", 30, True, False)
    tile = font.render(("Score: " + str(int(score))), True, (255, 255, 255))
    screen.blit(tile, (x, y))

def displayMatrix(mat):
    x = 50
    y = 90
    for row in mat:
        for col in row:
            if col != 0:
                num = int(col)
                if num > 1000:
                    font = pygame.font.SysFont("consolas", 36, True, False)
                    tile = font.render(str(num), True, (255, 255, 255))
                    screen.blit(tile, ((x - 15), (y + 9)))
                elif num > 100:
                    font = pygame.font.SysFont("consolas", 40, True, False)
                    tile = font.render(str(num), True, (255, 255, 255))
                    screen.blit(tile, ((x - 15), (y+5)))
                elif num > 10:
                    font = pygame.font.SysFont("consolas", 44, True, False)
                    tile = font.render(str(num), True, (255, 255, 255))
                    screen.blit(tile, ((x - 7), (y + 3)))
                else:
                    font = pygame.font.SysFont("consolas", 48, True, False)
                    tile = font.render(str(num), True, (255, 255, 255))
                    screen.blit(tile, (x, y))
            x += 90
        y += 90
        x = 50


def gameover(finalScore):
    print('GAME OVER')
    highestScore = updateHighest(finalScore)
    font = pygame.font.SysFont("consolas", 30, True, False)
    overfont = pygame.font.SysFont("consolas", 60, True, False)
    x = 20
    y = 220
    while True:
        screen.fill((40, 170, 255))
        pygame.draw.rect(screen, (170, 223, 255), [15, 65, 370, 370])
        text = overfont.render("GAME OVER", True, (255, 255, 255))
        screen.blit(text, (50, 150))

        score = "Score: " + str(int(finalScore))
        score.center(30)
        tile = font.render(score, True, (255, 255, 255))
        screen.blit(tile, (x, y))

        score = "Highest Score: " + str(int(highestScore))
        score.center(30)
        tile = font.render(score, True, (255, 255, 255))
        screen.blit(tile, (x, (y + 40)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        pygame.display.update()

def updateHighest(score):
    db = open('highest.txt', 'r+')
    db.seek(0)
    lines = db.readline()
    scoreText = lines.split('.')
    print(lines)
    highestScore = int(scoreText[0])
    print(highestScore)

    if score > highestScore:
        db.seek(0)
        db.write(str(score))
        highestScore = score
        db.close()

    return highestScore


def runGame():
    global GAMEOVER
    global gameBegin
    finalScore = 0
    # game loop
    while True:
        if not GAMEOVER:
            screen.fill((40, 170, 255))
            pygame.draw.rect(screen, (170, 223, 255), [15, 65, 370, 370])

            # ROW 1
            pygame.draw.rect(screen, (120, 220, 255), [25, 75, 80, 80])
            pygame.draw.rect(screen, (120, 220, 255), [115, 75, 80, 80])
            pygame.draw.rect(screen, (120, 220, 255), [205, 75, 80, 80])
            pygame.draw.rect(screen, (120, 220, 255), [295, 75, 80, 80])
            # ROW 2
            pygame.draw.rect(screen, (120, 220, 255), [25, 165, 80, 80])
            pygame.draw.rect(screen, (120, 220, 255), [115, 165, 80, 80])
            pygame.draw.rect(screen, (120, 220, 255), [205, 165, 80, 80])
            pygame.draw.rect(screen, (120, 220, 255), [295, 165, 80, 80])
            # ROW 3
            pygame.draw.rect(screen, (120, 220, 255), [25, 255, 80, 80])
            pygame.draw.rect(screen, (120, 220, 255), [115, 255, 80, 80])
            pygame.draw.rect(screen, (120, 220, 255), [205, 255, 80, 80])
            pygame.draw.rect(screen, (120, 220, 255), [295, 255, 80, 80])
            # ROW 4
            pygame.draw.rect(screen, (120, 220, 255), [25, 345, 80, 80])
            pygame.draw.rect(screen, (120, 220, 255), [115, 345, 80, 80])
            pygame.draw.rect(screen, (120, 220, 255), [205, 345, 80, 80])
            pygame.draw.rect(screen, (120, 220, 255), [295, 345, 80, 80])

        if not gameBegin:
            matrix = initialiseMatrix()
            gameBegin = True

        if checkGameOver(matrix):
            GAMEOVER = True
            gameover(finalScore)
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            # to check if key stroke is pressed and movt
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print("Left pressed")
                    score, changed = move(matrix, 'left')
                    finalScore += score
                    if changed:
                        generateNew(matrix)

                elif event.key == pygame.K_RIGHT:
                    print("Right pressed")
                    score, changed = move(matrix, 'right')
                    finalScore += score
                    if changed:
                        generateNew(matrix)

                elif event.key == pygame.K_UP:
                    print("Up pressed")
                    score, changed = move(matrix, 'up')
                    finalScore += score
                    if changed:
                        generateNew(matrix)

                elif event.key == pygame.K_DOWN:
                    print("Down pressed")
                    score, changed = move(matrix, 'down')
                    finalScore += score
                    if changed:
                        generateNew(matrix)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    print("Key released")
        displayScore(finalScore)
        displayMatrix(matrix)
        pygame.display.update()


if __name__ == "__main__":
    print("Game Begins")
    runGame()
