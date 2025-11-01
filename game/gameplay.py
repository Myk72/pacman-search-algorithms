import pygame
from config import *
from .entities import displayPacman, displayGhost, displayFood, Ghost
from .minimax import minimax_decision, availablePath
# from .utils import manhattan, neighbors
import random

def minimaxMode(gridmap, screen, font):
    currentPos = gridmap.startPoint
    colors = [ghostColor, ghostColor2, ghostColor3, ghostColor4]
    personalities = ['Blinky', 'Pinky', 'Inky', 'Clyde']
    
    ghosts = []
    for idx, val in enumerate(gridmap.ghosts):
        g = Ghost(val, colors[idx], personality=personalities[idx])
        ghosts.append(g)

    # food
    pellets = set(gridmap.food)
    powerPellets = set(gridmap.power)

    clock = pygame.time.Clock()
    lost, win = False, False
    ghostTimer = 0
    scaredTimer = 0.0
    ghostScared = False
    lives = max_lives
    status = "Minimax mode"

    while True:
        dt = clock.tick(fps) / 1000.0
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return

            if e.type == pygame.KEYDOWN:
                if e.key in [pygame.K_ESCAPE, pygame.K_r]:
                    return

                if not lost:
                    x, y = currentPos
                    move = None
                    if e.key == pygame.K_UP:
                        move = (x-1, y)
                    elif e.key == pygame.K_DOWN:
                        move = (x+1, y)
                    elif e.key == pygame.K_LEFT:
                        move = (x, y-1)
                    elif e.key == pygame.K_RIGHT:
                        move = (x, y+1)

                    if move and gridmap.isClear(move):
                        currentPos = move
                        if currentPos in pellets:
                            pellets.remove(currentPos)
                        if currentPos in powerPellets:
                            powerPellets.remove(currentPos)
                            ghostScared = True
                            scaredTimer = powerDuration
                            for g in ghosts:
                                g.scared = True
                                g.state = 'scared'
                                
                        
                        if not pellets and not powerPellets:
                            lost, win = True, True
                            status = "You Win!"


        if ghostScared:
            scaredTimer -= dt
            if scaredTimer <= 0:
                ghostScared = False
                for g in ghosts:
                    if g.state == 'scared':
                        g.scared = False
                        g.state = 'normal'

        # ghost movement handling
        if not lost:
            ghostTimer += 1
            if ghostTimer >= ghostMoveInterval:
                ghostTimer = 0
                for g in ghosts:

                    # Dead ghosts
                    if g.state == 'dead':
                        box = gridmap.ghostsHome or g.startPos
                        # print('ghost home', box,gridmap.ghostsHome,g.startPos)
                        valid = availablePath(gridmap, g.pos)
                        if valid:
                            # print(valid, 'bets move')
                            g.pos = random.choice(valid)
                            
                        if g.pos == box:
                            print("Here inside the box")
                            g.state = 'normal'
                            g.scared = False
                        continue

                    # Scared ghosts: flee
                    if g.state == 'scared' or g.scared:
                        valid = availablePath(gridmap, g.pos)
                        # since it's checking it's neighbors their distance to pacman is the same
                        g.pos = random.choice(valid)
                        continue

                    
                    if pellets or powerPellets:
                        g.pos = minimax_decision(gridmap, g.pos, currentPos, pellets.union(powerPellets), depth=minimaxDepth)

        # collisions
        for g in ghosts:
            if g.pos == currentPos:
                if g.state == 'scared':
                    g.state = 'dead'
                    g.scared = False
                elif g.state == 'dead':
                    continue
                else:
                    lives -= 1
                    if lives <= 0:
                        lost, win = True, False
                        status = "Game Over!"
                    else:
                        currentPos = gridmap.startPoint
                        for gg in ghosts:
                            gg.pos = gg.startPos
                            gg.scared = False
                            if gg.state != 'dead':
                                gg.state = 'normal'
                        ghostScared = False
                        scaredTimer = 0
                        status = f"You were caught! Lives remaining: {lives}"


        screen.fill(backgroundColor )
        gridmap.displayGrid(screen)
        displayFood(screen, pellets, powerPellets)

        for g in ghosts:
            color = g.color
            if g.state == 'scared':
                color = scaredGhostColor
            elif g.state == 'dead':
                color = deadGhostColor
            displayGhost(screen, g.pos, color)

        displayPacman(screen, currentPos)
        pygame.draw.rect(screen, (20,20,20), (0, gridRows*cellSize, windowWidth, statusHeight))
        status_line = status + f"   Lives: {lives}   Pellets: {len(pellets)+len(powerPellets)}"
        txt = font.render(status_line, True, textColor)
        screen.blit(txt, (10, gridRows*cellSize + 10))
        pygame.display.flip()
